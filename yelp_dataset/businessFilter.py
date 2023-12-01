import json

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def filter_business_by_review_ids(business_file_path, review_file_path, output_file_path):
    # Read review file and extract unique business_id values
    reviews = read_json_file(review_file_path)
    business_ids = set(review['business_id'] for review in reviews)

    # Read business file and filter based on business_id values
    businesses = read_json_file(business_file_path)
    filtered_businesses = [business for business in businesses if business['business_id'] in business_ids]

    # Write the filtered businesses to a new file
    write_json_file(output_file_path, filtered_businesses)

if __name__ == "__main__":
    business_file_path = "yelp_academic_dataset_business.json"
    review_file_path = "yelp_academic_dataset_review.json"
    output_file_path = "filtered_businesses.json"

    filter_business_by_review_ids(business_file_path, review_file_path, output_file_path)
    print(f"Filtered businesses saved to {output_file_path}")
