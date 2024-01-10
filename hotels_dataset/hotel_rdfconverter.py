import csv
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS

schema = Namespace("http://schema.org/")

def convert_csv_to_rdf(csv_file_path):
    
    graph = Graph()

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # URI
            name_for_uri = row['name'].replace(' ', '_')
            instance_uri = URIRef(f"http://example.com/hotel/{name_for_uri}")

            graph.add((instance_uri, RDF.type, schema.Hotel))

            # Properties
            graph.add((instance_uri, schema.name, Literal(row['name'])))
            graph.add((instance_uri, schema.address, Literal(row['address'])))
            graph.add((instance_uri, schema.city, Literal(row['city'])))
            graph.add((instance_uri, schema.country, Literal(row['country'])))
            graph.add((instance_uri, schema.latitude, Literal(row['latitude'])))
            graph.add((instance_uri, schema.longitude, Literal(row['longitude'])))
            graph.add((instance_uri, schema.postalCode, Literal(row['postalCode'])))
            graph.add((instance_uri, schema.province, Literal(row['province'])))

    return graph

def save_rdf_to_file(rdf_graph, output_file_path):
    rdf_graph.serialize(destination=output_file_path, format='turtle')

if __name__ == "__main__":
    csv_file_path = './hotels_dataset/hotels_data_filtered.csv'

    output_file_path = './hotels_dataset/hotels.rdf'

    rdf_graph = convert_csv_to_rdf(csv_file_path)

    save_rdf_to_file(rdf_graph, output_file_path)
