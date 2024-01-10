import csv
from collections import defaultdict

def filter_duplicates(csv_file_path, output_csv_path):
    
    unique_hotels = defaultdict(list)

    #read
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # filter out when adress and city overlap (not address only since many streets are named the same)
            hotel_identifier = (row['address'], row['city'])

            if hotel_identifier not in unique_hotels:
                unique_hotels[hotel_identifier].append(row)
    # write output
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as output_csv:
        fieldnames = ['address', 'categories', 'city', 'country', 'latitude', 'longitude', 'name',
                      'postalCode', 'province']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for hotels in unique_hotels.values():
            for hotel in hotels:
                csv_writer.writerow({key: value for key, value in hotel.items() if key in fieldnames})

if __name__ == "__main__":

    csv_file_path = './hotels_dataset/hotels_data_noReviews.csv'

    output_csv_path = './hotels_dataset/hotels_data_filtered.csv'

    filter_duplicates(csv_file_path, output_csv_path)
