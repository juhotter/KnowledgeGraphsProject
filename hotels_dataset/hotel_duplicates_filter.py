import csv
from collections import defaultdict

def filter_duplicates(csv_file_path, output_csv_path):
    # Create a dictionary to store unique hotels based on address and city
    unique_hotels = defaultdict(list)

    # Open the CSV file and iterate through each row
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Create a unique identifier for each hotel based on address and city
            hotel_identifier = (row['address'], row['city'])

            # If the hotel is not in the dictionary, add it
            if hotel_identifier not in unique_hotels:
                unique_hotels[hotel_identifier].append(row)

    # Write the filtered hotels to a new CSV file
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as output_csv:
        fieldnames = ['address', 'categories', 'city', 'country', 'latitude', 'longitude', 'name',
                      'postalCode', 'province']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for hotels in unique_hotels.values():
            for hotel in hotels:
                # Write only the non-duplicate hotel columns to the output CSV
                csv_writer.writerow({key: value for key, value in hotel.items() if key in fieldnames})

if __name__ == "__main__":
    # Replace 'filtered_data_without_reviews.csv' with the path to the previous filtered CSV file
    csv_file_path = 'hotels_data_noReviews.csv'

    # Replace 'filtered_data_no_duplicates.csv' with the desired output CSV file path
    output_csv_path = 'hotels_data_filtered.csv'

    # Filter duplicates based on address and city and write to CSV
    filter_duplicates(csv_file_path, output_csv_path)
