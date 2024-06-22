import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_to_csv(url, output_file):
    print("\033[92mScraping...\033[0m")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    
    with open(output_file, 'w', newline='', encoding='utf-8' ) as csv_file:
        writer = csv.writer(csv_file)
        for table in tables:
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
                links = [a['href'] for a in row.find_all('a')]
                row_data.extend(links)
                if len(row_data) >= 4:
                    if '/' in row_data[1]:
                        row_data[1] = row_data[1].replace('/', '.')
                    if '&' in row_data[1]:
                        row_data[1] = row_data[1].replace('&', 'and')
                    if ',' in row_data[1]:
                        row_data[1] = row_data[1].replace(',', '.')
                    if '|' in row_data[1]:
                        row_data[1] = row_data[1].replace('|', '.')
                    row_data_modified = [row_data[1], row_data[2], row_data[4]]
                    table_data.append(row_data_modified)
                
            writer.writerows(table_data)
            writer.writerow([])

    print(f"\033[93mTables scraped and saved to {output_file} \033[0m")

def scrape_each_url():
    with open('csv/Company_table.csv', 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) > 0:
                folder_name = name_decider_normal(row[0])
                filename = 'csv/' + folder_name + '.csv'
                with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    url = "https://results.channeli.in/" + row[2]
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tables = soup.find_all('table')
                    for table in tables:
                        table_data = []
                        branch_data = [(row[0], 0)]
                        for row in table.find_all('tr'):
                            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
                            if len(row_data) > 0:
                                found = False
                                for i, (branch, count) in enumerate(branch_data):
                                    row_data[3] = row_data[3].replace(',', '')
                                    if row_data[3] == branch:
                                        branch_data[i] = (branch, count + 1)
                                        found = True
                                        break
                                if not found:
                                    row_data[3] = row_data[3].replace(',', '')
                                    branch_data.append((row_data[3], 1))
                        table_data.append(branch_data)

                        writer.writerows(table_data)
                        writer.writerow([])

def clean_csvs():
    for filename in os.listdir('csv/'):
        if filename.endswith('.csv') and filename != 'Company_table.csv':
            with open('csv/' + filename, 'r', newline='', encoding='utf-8') as csv_file:
                print(f"\033[93mCleaning {filename}...\033[0m")
                reader = csv.reader(csv_file)
                rows = list(reader)
                new_rows = [['Company', 'CTC']]
                for row in rows:
                    if len(row) > 1:
                        [companyname, counter] = string_pair_splitter(row[0])
                        new_row = [companyname]
                        new_row.append(CTC_finder(companyname))
                        for i in range(1, len(row)):
                            [branch, count] = string_pair_splitter(row[i])
                            if branch not in new_rows[0]:
                                new_rows[0].append(branch)
                            branch_index = new_rows[0].index(branch)
                            if len(new_row) < branch_index + 1:
                                for _ in range(len(new_row), branch_index + 1):
                                    new_row.append(0)
                            new_row[branch_index] = count
                        new_rows.append(new_row)
                with open('csv/' + filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(new_rows)

def string_pair_splitter(str):
    str = str.replace('(', '').replace(')', '').replace("'", '')
    str = str.split(',')
    str = [x.strip() for x in str]
    return str

def CTC_finder(name):
    print(f"\033[92mFinding CTC for {name}\033[0m")
    name = name.lower()
    name = name.replace('(', '').replace(')', '').replace("'", '').replace(',', '').replace('|', '')
    queries = name.split()
    if len(queries) > 3:
        queries = queries[:3]
    url = "https://channeli.in/api/noticeboard/new/?keyword="
    for query in queries:
        url = url + query + "%20"
    response = requests.get(url)
    try:
            response = response.json()
    except:
        print("\033[91mNo CTC found\033[0m")
        return 'notfound'
    if response.get('results') == None:
        print("\033[91mNo CTC found\033[0m")
        return 'notfound'
    response = response.get('results')
    identity = []
    for result in response:
        if 'submission' in result.get('title').lower():
            identity.append(result.get('id'))
    print(identity)
    # final = []
    url_list = ""
    for id in identity:
        # site_url = "https://channeli.in/api/noticeboard/new/" + str(id)
        site_url = "https://channeli.in/noticeboard/notice/" + str(id) + " "
        url_list = url_list + site_url

    print(url_list)
    return url_list
        # response = requests.get(site_url)
        # try:
        #     response = response.json()
        # except:
        #     print("\033[91mNo CTC found\033[0m")
        #     return 'notfound'
        # response = response.get('content')
        # response = response.split('\n')

        
        
        # for line in response:
        #     line = BeautifulSoup(line, 'html.parser').get_text()
        #     if ('CTC' in line or 'package' in line or 'compensation' in line or 'INR' in line or 'LPA' in line) and any(char.isdigit() for char in line):
        #         ctc_index = line.lower().find('ctc')
        #         if ctc_index != -1:
        #             next_15_chars = line[ctc_index + 3:ctc_index + 18]
        #             final.append(next_15_chars)
        #         else:
        #             final.append(line)
                
    # if len(final) == 0:
    #     print("\033[91mNo CTC found\033[0m")
    #     return 'notfound'
    # else:
    #     print(final[0])
    #     return final[0]




# edit these lists to add more company types
def name_decider_normal(name):
    name = name.lower()
    PPO = ['ppo']
    SDE = ['software', 'SDE', 'developer', 'dev', 'lead']
    CONSULT = ['consult', 'management', 'business', 'strategy', 'bank', 'finance']
    DATA = ['data', 'anal', 'data science', 'machine learning', 'ai', 'artificial intelligence', 'big data', 'intelligence', 'ml']
    CORE = ['electrical', 'electronics', 'core', 'hardware', 'networking', 'embedded', 'vlsi', 'communication', 'tele', 'mech', 'elec', 'e&i', 'ece', 'civil', 'chem', 'meta', 'mining', 'geo', 'petro', 'auto', 'reliance', 'field', 'environment']
    EDU = ['education', 'edtech', 'teaching', 'vedantu', 'byju', 'unacademy', 'edureka', 'upgrad', 'edu', 'fiitjee', 'allen', 'institute']

    if any(word in name for word in PPO):
        return 'PPO'
    elif any(word in name for word in SDE):
        return 'SDE'
    elif any(word in name for word in CONSULT):
        return 'consult-finance'
    elif any(word in name for word in DATA):
        return 'data'
    elif any(word in name for word in CORE):
        return 'core'
    elif any(word in name for word in EDU):
        return 'education'
    else:
        return 'other'

if __name__ == "__main__":
    url = "https://results.channeli.in/2023/placement/company/"
    output_file = 'csv/Company_table.csv'
    if not os.path.exists('csv'):
            os.makedirs('csv')
    scrape_to_csv(url, output_file)
    print("\033[94mScraping complete. Now scraping each URL...\033[0m")
    scrape_each_url()
    print("\033[94mScraping complete. Now cleaning All CSVs...\033[0m")
    clean_csvs()
    print("\033[91mCleaning complete.\033[0m")




