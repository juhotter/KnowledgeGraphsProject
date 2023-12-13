import json
from rdflib import Graph, Namespace, Literal, URIRef, RDF

# Load JSON data
with open('./yelp_dataset/yelp_academic_dataset_business.json', 'r') as file:
    data = json.load(file)

# Create an RDF graph
g = Graph()

# Define schema.org namespace
schema = Namespace("http://schema.org/")

# Define mappings between JSON properties and schema.org properties and classes
property_mappings = {
    "business_id": (schema.identifier, None),
    "name": (schema.name, schema.LocalBusiness),
    "address": (schema.address, schema.LocalBusiness),
    "city": (schema.addressLocality, schema.LocalBusiness),
    "state": (schema.addressRegion, schema.LocalBusiness),
    "postal_code": (schema.postalCode, schema.LocalBusiness),
    "latitude": (schema.latitude, schema.GeoCoordinates),  # Class for latitude
    "longitude": (schema.longitude, schema.GeoCoordinates),  # Class for longitude
    "stars": (schema.ratingValue, schema.Rating),  # Map "stars" to "Rating" type
    "review_count": (schema.reviewCount, schema.Rating),
    "is_open": (schema.openingHoursSpecification, schema.LocalBusiness),
    "attributes": (schema.additionalProperty, schema.LocalBusiness),
    "categories": (schema.category, schema.LocalBusiness),
    "hours": (schema.hoursAvailable, schema.LocalBusiness),
}

# Iterate through each business in the JSON data
for business in data:
    # Create a unique URI for the business
    business_uri = URIRef(f"http://example.com/business/{business['business_id']}")

    # Add class for LocalBusiness
    g.add((business_uri, RDF.type, schema.LocalBusiness))

    # Add triples for each property and its class
    for json_property, (schema_property, property_class) in property_mappings.items():
        if json_property in business and business[json_property] is not None:
            # Special handling for attributes and hours
            if json_property == "attributes":
                for attr_key, attr_value in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(attr_value, lang="en")))
            elif json_property == "hours" and business[json_property] is not None:
                for day, hours in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(f"{day} {hours}", lang="en")))
            else:
                if property_class:
                    # Add a triple indicating the type of the property value
                    g.add((business_uri, schema_property, RDF.type, property_class))
                g.add((business_uri, schema_property, Literal(business[json_property], lang="en")))
# Serialize the RDF graph to a file
g.serialize(destination='output.rdf', format='xml')