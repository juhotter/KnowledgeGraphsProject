import json
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD
from datetime import datetime

with open('./yelp_dataset/yelp_academic_dataset_business.json', 'r') as file:
    data = json.load(file)

g = Graph()

schema = Namespace("http://schema.org/")

# define mappings
property_mappings = {
    "business_id": (schema.identifier, None),
    "name": (schema.name, schema.LocalBusiness),
    "address": (schema.address, schema.LocalBusiness),
    "city": (schema.addressLocality, schema.LocalBusiness),
    "state": (schema.addressRegion, schema.LocalBusiness),
    "postal_code": (schema.postalCode, schema.LocalBusiness),
    "latitude": (schema.latitude, None),
    "longitude": (schema.longitude, None),
    "stars": (schema.ratingValue, schema.Rating),
    "review_count": (schema.reviewCount, schema.Rating),
    "is_open": (schema.is_open, None),
    "attributes": (schema.additionalProperty, schema.LocalBusiness),
    "categories": (schema.category, schema.LocalBusiness),
    "hours": (schema.hoursAvailable, schema.LocalBusiness),
}

# iterate through each business
for business in data:
    # create a unique URI
    business_uri = URIRef(f"http://example.com/business/{business['business_id']}")

    # add class for LocalBusiness
    g.add((business_uri, RDF.type, schema.LocalBusiness))

    # add triples
    for json_property, (schema_property, property_class) in property_mappings.items():
        if json_property in business and business[json_property] is not None:
            # special handling for attributes and hours
            if json_property == "attributes":
                for attr_key, attr_value in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(attr_value, lang="en")))
            elif json_property == "hours" and business[json_property] is not None:
                for day, hours in business[json_property].items():
                    g.add((business_uri, schema_property, Literal(f"{day} {hours}", lang="en")))
            elif json_property in ["latitude", "longitude"]:
                g.add((business_uri, schema_property, Literal(business[json_property])))
            else:
                # check if property_class is not None
                if property_class:
                    g.add((business_uri, RDF.type, property_class))
                g.add((business_uri, schema_property, Literal(business[json_property], lang="en")))

# provenance information
provenance_uri = URIRef("http://example.com/provenance")
g.add((provenance_uri, RDF.type, schema.Provenance))
g.add((provenance_uri, schema.creationDate, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
g.add((provenance_uri, schema.dataSource, Literal("https://www.yelp.com/dataset", lang="en")))
g.add((provenance_uri, schema.numberOfTriples, Literal(len(g), datatype=XSD.integer)))

# export to a file
g.serialize(destination='./yelp_dataset/business_withClasses_and_provenance.rdf', format='xml')