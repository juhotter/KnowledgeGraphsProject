from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

tokenizer = AutoTokenizer.from_pretrained("Dizex/InstaFoodRoBERTa-NER")
model = AutoModelForTokenClassification.from_pretrained("Dizex/InstaFoodRoBERTa-NER")

pipe = pipeline("ner", model=model, tokenizer=tokenizer)

output_list = []

with open('yelp_academic_dataset_review.json', 'r') as json_file:
    data = json.load(json_file)
    for sample_load_file in data:
        business_id = sample_load_file['business_id']
        text = sample_load_file['text']

        ner_entity_results = pipe(text, aggregation_strategy="simple")

        def convert_entities_to_list(text, entities: list[dict]) -> list[str]:
            ents = []
            for ent in entities:
                e = {"start": ent["start"], "end": ent["end"], "label": ent["entity_group"]}
                if ents and -1 <= ent["start"] - ents[-1]["end"] <= 1 and ents[-1]["label"] == e["label"]:
                    ents[-1]["end"] = e["end"]
                    continue
                ents.append(e)

            return [text[e["start"]:e["end"]] for e in ents]

        food = convert_entities_to_list(text, ner_entity_results)
        output = {"meals": food, "businessId": business_id}
        output_list.append(output)

output_file_path = 'output.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(output_list, output_file, ensure_ascii=False, indent=2)
