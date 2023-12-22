# KnowledgeGraphsProject
## Semester Project in Knowledge Graphs from Joey Hieronimy & Julian Hotter

## WP1 – Knowledge Creation:
### D1.1. Domain Selection and Identification of Sources (06.12.2023)
**Domain Decision:** Our choice involves modeling various enterprises listed on YELP, encompassing not only food establishments such as restaurants but potentially extending beyond that category. Furthermore, we intend to incorporate specific food items into these enterprises. For instance, considering the example of McDonald's, the model would include distinct meals like cheeseburgers, hamburgers, Big Mac, and so forth. The objective is to create a knowledge graph that encapsulates both businesses and their associated meals.
Therefore we will make use of one structured dataset containing the businesses and one unstructured dataset, which includes reviews from those businesses.

### Datasets: 
**https://www.yelp.com/dataset**
This Yelp dataset includes multiple different datasets.
For our project, we use datasets about businesses and user reviews.
Reviews will serve as unstructured data whereas businesses will serve as structured data.

### Structured Data:
**yelp_academic_dataset_business.json**
This JSON file holds all businesses, whereas each business has a unique **businessID**.

### Unstructured Data:
For our project, we had to shorten the reviews dataset from YELP, since we decided to go with only 1000 reviews since the amount of data was too much to process further (millions).
Therefore we wrote a short script that gave us the first 1000 reviews. **Script: yelp_dataset/rowFilter.py.**
The JSON file **yelp_academic_dataset_review.json** is the result of the shortened review dataset. 
From this dataset, we only use two properties. Namely the **text** property & and **businessId** property.
The **text** property, namely the written reviews is used to extract the meals with the help of NER of food entities.
The **businessId** property is used to link the found meals to the businesses from the structured dataset.

### How is the knowledge combined?
1. Ontology - The structured dataset is used to build an ontology of (food)-businesses.
2. Ontology - The property **text** from the unstructured dataset is used to gather multiple meals from businesses.
   The result should be something like a meal menu for each business.
   To conclude, this means when a business has reviews that include meal names, these meals are then mapped to that restaurant.
   The mapping between those two ontologies is done via the **businessId**, which is a property in both datasets.

### D1.2. RDF data created from the sources (13.12.2023)


## WP2 – Knowledge Hosting:
### D2.1. Knowledge graph stored in a triple store (20.12.2023)





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

