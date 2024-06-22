import requests
from bs4 import BeautifulSoup
import csv

def scrape_to_csv(url, output_file):
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
                        row_data[1] = row_data[1].replace('/', '|')
                    row_data_modified = [row_data[1], row_data[2], row_data[4]]
                    table_data.append(row_data_modified)
                
            writer.writerows(table_data)
            writer.writerow([])

    print(f"Tables scraped and saved to {output_file}")

def scrape_each_url():
    with open('csv/Company_table.csv', 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) > 0:
                filename = 'csv/' + row[0] + '.csv'
                with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    url = "https://results.channeli.in/" + row[2]
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tables = soup.find_all('table')
                    for table in tables:
                        table_data = []
                        branch_data = []
                        for row in table.find_all('tr'):
                            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
                            if len(row_data) > 0:
                                found = False
                                for i, (branch, count) in enumerate(branch_data):
                                    if row_data[3] == branch:
                                        branch_data[i] = (branch, count + 1)
                                        found = True
                                        break
                                if not found:
                                    branch_data.append((row_data[3], 1))

                        table_data.append(branch_data)

                        writer.writerows(table_data)
                        writer.writerow([])
    

if __name__ == "__main__":
    url = "https://results.channeli.in/2023/placement/company/"
    output_file = 'csv/Company_table.csv'
    scrape_to_csv(url, output_file)
    scrape_each_url()
