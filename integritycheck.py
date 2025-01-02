import os
import csv

def count_numbers_in_csv(file_path):
    total_count = 0
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                if item.isdigit():
                    total_count += int(item)
    return total_count

def main():
    directory = 'csv'
    excluded_file = 'Company_table.csv'
    total_sum = 0

    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename != excluded_file:
            file_path = os.path.join(directory, filename)
            total_sum += count_numbers_in_csv(file_path)

    print(f'Total sum of numbers in CSV files (excluding {excluded_file}): {total_sum}')

if __name__ == "__main__":
    main()