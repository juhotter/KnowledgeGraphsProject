import json
from rdflib import Graph, Namespace, Literal, URIRef

# Load JSON data
with open('yelp_academic_dataset_business.json', 'r') as file:
    data = json.load(file)

# Create an RDF graph
g = Graph()

# Define schema.org namespace
schema = Namespace("http://schema.org/")

# Define mappings between JSON properties and schema.org properties
property_mappings = {
    "business_id": schema.identifier,
    "name": schema.name,
    "address": schema.address,
    "city": schema.addressLocality,
    "state": schema.addressRegion,
    "postal_code": schema.postalCode,
    "latitude": schema.latitude,
    "longitude": schema.longitude,
    "stars": schema.ratingValue,
    "review_count": schema.reviewCount,
    "is_open": schema.openingHoursSpecification,
    "attributes": schema.additionalProperty,
    "categories": schema.category,
    "hours": schema.hoursAvailable,
}

# Iterate through each business in the JSON data
for business in data:
    # Create a unique URI for the business
    business_uri = URIRef(f"http://example.com/business/{business['business_id']}")

    # Add triples for each property
    for json_property, schema_property in property_mappings.items():
        if json_property in business and business[json_property] is not None:
            # Special handling for attributes and hours
            if json_property == "attributes":
                for attr_key, attr_value in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(attr_value, lang="en")))
            elif json_property == "hours" and business[json_property] is not None:
                for day, hours in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(f"{day} {hours}", lang="en")))
            else:
                g.add((business_uri, schema_property, Literal(business[json_property], lang="en")))

# Serialize the RDF graph to a file
g.serialize(destination='output.rdf', format='xml')
