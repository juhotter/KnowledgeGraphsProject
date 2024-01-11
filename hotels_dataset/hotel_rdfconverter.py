import csv
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

schema = Namespace("http://schema.org/")

def convert_csv_to_rdf(csv_file_path, output_file_path):
    graph = Graph()

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # URI
            name_for_uri = row['name'].replace(' ', '_')
            city_for_uri = row['city'].replace(' ', '_')
            
            # Adding city to URI to distinguish hotels with the same name
            instance_uri = URIRef(f"http://example.com/hotel/{name_for_uri}_{city_for_uri}")

            graph.add((instance_uri, RDF.type, schema.Hotel))

            graph.add((instance_uri, schema.name, Literal(row['name'], lang='en')))
            graph.add((instance_uri, schema.address, Literal(row['address'], lang='en')))
            graph.add((instance_uri, schema.city, Literal(row['city'], lang='en')))
            graph.add((instance_uri, schema.country, Literal(row['country'], lang='en')))

            # Check if latitude and longitude are not empty before converting to float
            if row['latitude']:
                graph.add((instance_uri, schema.latitude, Literal(float(row['latitude']), datatype=XSD.double)))
            if row['longitude']:
                graph.add((instance_uri, schema.longitude, Literal(float(row['longitude']), datatype=XSD.double)))

            graph.add((instance_uri, schema.postalCode, Literal(row['postalCode'], lang='en')))
            graph.add((instance_uri, schema.province, Literal(row['province'], lang='en')))

    graph.serialize(destination=output_file_path, format='xml')

if __name__ == "__main__":
    csv_file_path = './hotels_dataset/hotels_data_filtered.csv'

    output_file_path = './hotels_dataset/hotels.rdf'
    convert_csv_to_rdf(csv_file_path, output_file_path)
