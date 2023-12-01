import json

def lazy_load_json(file_path, chunk_size=1000):
    with open(file_path, 'r') as file:
        data = []
        for i, line in enumerate(file):
            if i >= chunk_size:
                break
            data.append(json.loads(line))
    return data

def save_shortened_json(shortened_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(shortened_data, file)

if __name__ == "__main__":
    input_file_path = "yelp_academic_dataset_review.json"
    output_file_path = "shortened_yelp_reviews.json"
    data_chunk = lazy_load_json(input_file_path, chunk_size=1000)
    save_shortened_json(data_chunk, output_file_path)
