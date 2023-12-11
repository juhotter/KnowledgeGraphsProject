import json
from rdflib import Graph, Namespace, Literal, URIRef

# Load JSON data
with open('./yelp_dataset/yelp_academic_dataset_review_nlp_processed.json', 'r') as file:
    data = json.load(file)

# Create an RDF graph
g = Graph()

# Define schema.org namespace
schema = Namespace("http://schema.org/")

# Define mappings between JSON properties and schema.org properties for meals
meal_mappings = {
    "meals": schema.menu,
    "businessId": schema.identifier,
}

# Iterate through each entry in the JSON data
for entry in data:
    # Create a unique URI for the business
    business_uri = URIRef(f"http://example.com/business/{entry['businessId']}")

    # Add triples for each property
    for json_property, schema_property in meal_mappings.items():
        if json_property in entry and entry[json_property] is not None:
            if json_property == "meals":
                # Special handling for meals
                for meal in entry[json_property]:
                    g.add((business_uri, schema_property, Literal(meal, lang="en")))
            else:
                g.add((business_uri, schema_property, Literal(entry[json_property], lang="en")))

# Serialize the RDF graph to a file
g.serialize(destination='./yelp_dataset/meals.rdf', format='xml')
