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


The structured dataset is converted into RDF and can be accessed with the following link: https://drive.google.com/file/d/1RN3UI_eKsCGpeCbdS5hm_HkSQqTguFGL/view?usp=sharing .
The file is too large to be uploaded onto Git.


### Graph Repository
The Graph Repository is hosted in GraphDB on our local machine. The repository was exported as a .rj file and can be accessed with the following link: https://drive.google.com/file/d/1SqUEAvSJhQ3xlqfjD1AlNnHQ_DuGXaR8/view?usp=share_link
The file is again too large to be uploaded onto Git.

## Queries

### Linking:

PREFIX ns1: <http://schema.org/>

INSERT {
  GRAPH <http://example.com/linked-data/> {
    ?business ns1:hasMenu ?menu .
  }
}
WHERE {
  GRAPH <http://example.com/business/> {
    ?business ns1:identifier ?businessId .
  }
  GRAPH <http://example.com/meals/> {
    ?menu ns1:identifier ?businessId .
  }
}


### Menu quering

PREFIX schema: <http://schema.org/>

SELECT ?business ?name ?menuItem
WHERE {
  ?business schema:hasMenu ?menu .
  ?business schema:name ?name .
  ?menu schema:menu ?menuItem .
}

