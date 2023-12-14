# KnowledgeGraphsProject
## Semester Project in Knowledge Graphs from Joey Hieronimy & Julian Hotter

### Dataset: https://www.yelp.com/dataset
The Yelp dataset typically includes datasets about businesses, user reviews, and other related data.
For our purpose, we use the dataset of businesses and reviews.
Reviews will serve as unstructured data whereas businesses will serve as structured data.

### Note:
For our project, we had to shorten the reviews dataset since we decided to go with only 1000 reviews since the amount of data was too much to process further (millions).
Therefore we wrote a short script that gave us the first 1000 reviews.

### Unstructured Data:
#### yelp_academic_dataset_review.json
This JSON file holds 1000 reviews from users on Yelp. The text part, namely the written reviews is the interesting part here.


### Structured Data:
#### yelp_academic_dataset_business.json
This JSON file holds all businesses

### How is the knowledge combined?
#### The structured dataset is used to build an ontology of restaurants.
#### The unstructured dataset is used to map different dishes to restaurants so that we can derive something like a restaurant menu, like it is done with Google Reviews already. This means when a restaurant has a reviews with named dishes this dishes are then mapped to that restaurant.


The structured dataset is converted into RDF and can be accessed with the following link: 
https://drive.google.com/file/d/1ntWd4VDm23me5CyYl9xQKQoJAUK3-Vev/view?usp=sharing
The file is too large to be uploaded onto Git.


### Graph Repository
The Graph Repository is hosted in GraphDB on our local machine. The repository was exported as a .rj file and can be accessed with the following link: https://drive.google.com/file/d/13y2U3a4MsYBY4cqJpSwPVvBR9bp82OLs/view?usp=sharing
The file is again too large to be uploaded onto Git.


### Queries

In a previous version, it was necessary to link the data explicitly with a query. However, since adding classes, it does so automatically with the unique identifier.

#### Menu querying:

PREFIX schema: <http://schema.org/>

SELECT ?businessName ?meal
WHERE {
  ?business schema:name ?businessName .
  ?business schema:menu ?meal .
}


#### Provenance information

PREFIX schema: <http://schema.org/>

SELECT ?creationDate ?dataSource ?numberOfTriples
WHERE {
  ?provenance schema:creationDate ?creationDate ;
              schema:dataSource ?dataSource ;
              schema:numberOfTriples ?numberOfTriples .
}

