import csv
from collections import defaultdict

def filter_reviews(csv_file_path, output_csv_path):
    
    unique_reviews = defaultdict(list)

    # read
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            hotel_identifier = (row['address'], row['city'])

            if hotel_identifier not in unique_reviews:
                unique_reviews[hotel_identifier].append(row)
            else:
                existing_reviews = unique_reviews[hotel_identifier]
                existing_texts = set(review['reviews.text'] for review in existing_reviews)
                current_review_text = row['reviews.text']

                if all(current_review_text != text for text in existing_texts):
                    unique_reviews[hotel_identifier].append(row)
    # outupt
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as output_csv:
        fieldnames = ['address', 'categories', 'city', 'country', 'latitude', 'longitude', 'name',
                      'postalCode', 'province']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for reviews in unique_reviews.values():
            for review in reviews:
                csv_writer.writerow({key: value for key, value in review.items() if key in fieldnames})

if __name__ == "__main__":
    csv_file_path = './hotels_dataset/hotels_data.csv'

    output_csv_path = './hotels_dataset/hotels_data_noReviews.csv'

    filter_reviews(csv_file_path, output_csv_path)
