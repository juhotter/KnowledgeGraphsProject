import json

input_file_path = 'yelp_academic_dataset_review.json'
output_file_path = 'output.json'  # Change this to your desired output file path
num_items_to_keep = 1000

# Function to delete items except the first 1000
def delete_items_except_first_n(input_file_path, output_file_path, num_items_to_keep):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for _ in range(num_items_to_keep):
                line = input_file.readline()
                if not line:
                    break  # End of file reached before reaching the desired number of items
                json_item = json.loads(line)
                json.dump(json_item, output_file, ensure_ascii=False)
                output_file.write('\n')

# Run the function
delete_items_except_first_n(input_file_path, output_file_path, num_items_to_keep)

print(f"{num_items_to_keep} items have been kept. Output saved to {output_file_path}")
