import csv
from collections import defaultdict

def filter_reviews(csv_file_path, output_csv_path):
    # Create a dictionary to store unique reviews for each hotel based on address and city
    unique_reviews = defaultdict(list)

    # Open the CSV file and iterate through each row
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Create a unique identifier for each hotel based on address and city
            hotel_identifier = (row['address'], row['city'])

            # If the hotel is not in the dictionary, add it with the current review
            if hotel_identifier not in unique_reviews:
                unique_reviews[hotel_identifier].append(row)
            else:
                # If the hotel is in the dictionary, only add the review if it doesn't already exist
                existing_reviews = unique_reviews[hotel_identifier]
                existing_texts = set(review['reviews.text'] for review in existing_reviews)
                current_review_text = row['reviews.text']

                # Check if the current review text is not in existing reviews
                if all(current_review_text != text for text in existing_texts):
                    unique_reviews[hotel_identifier].append(row)

    # Write the filtered reviews to a new CSV file without review-related columns
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as output_csv:
        fieldnames = ['address', 'categories', 'city', 'country', 'latitude', 'longitude', 'name',
                      'postalCode', 'province']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for reviews in unique_reviews.values():
            for review in reviews:
                # Write only the non-review columns to the output CSV
                csv_writer.writerow({key: value for key, value in review.items() if key in fieldnames})

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual path to your CSV file
    csv_file_path = 'hotels_data.csv'

    # Replace 'filtered_data_without_reviews.csv' with the desired output CSV file path
    output_csv_path = 'hotels_data_noReviews.csv'

    # Filter reviews and write to CSV without review-related columns
    filter_reviews(csv_file_path, output_csv_path)
