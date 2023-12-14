import json
from rdflib import Graph, Namespace, Literal, URIRef, RDF, XSD
from datetime import datetime

with open('./yelp_dataset/yelp_academic_dataset_review_nlp_processed.json', 'r') as file:
    data = json.load(file)

g = Graph()

schema = Namespace("http://schema.org/")

# mappings
meal_mappings = {
    "meals": (schema.menu, schema.FoodEstablishment),
    "businessId": (schema.identifier, schema.LocalBusiness),
}

# iterate through each entry
for entry in data:
    business_uri = URIRef(f"http://example.com/business/{entry['businessId']}")

    # add class for LocalBusiness
    g.add((business_uri, RDF.type, schema.LocalBusiness))

    for json_property, (schema_property, property_class) in meal_mappings.items():
        if json_property in entry and entry[json_property] is not None:
            if json_property == "meals":
                for meal in entry[json_property]:
                    # add class for FoodEstablishment
                    if property_class:
                        g.add((business_uri, RDF.type, property_class))
                    g.add((business_uri, schema_property, Literal(meal, lang="en")))
            else:
                g.add((business_uri, schema_property, Literal(entry[json_property], lang="en")))

# provenance information
provenance_uri = URIRef("http://example.com/provenance")
g.add((provenance_uri, RDF.type, schema.Provenance))
g.add((provenance_uri, schema.creationDate, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
g.add((provenance_uri, schema.dataSource, Literal("https://www.yelp.com/dataset", lang="en")))
g.add((provenance_uri, schema.numberOfTriples, Literal(len(g), datatype=XSD.integer)))

# export
g.serialize(destination='./yelp_dataset/meals_with_provenance.rdf', format='xml')
