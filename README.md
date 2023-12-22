# KnowledgeGraphsProject
## Semester Project in Knowledge Graphs from Joey Hieronimy & Julian Hotter

## WP1 – Knowledge Creation:
### D1.1. Domain Selection and Identification of Sources (06.12.2023)
**Domain Decision:** Our choice involves modeling various businesses listed on YELP, encompassing not only food establishments such as restaurants. Furthermore, we intend to incorporate specific food items into these businesses. For instance, considering the example of McDonald's, the model would include distinct meals like cheeseburgers, hamburgers, Big Mac, and so forth. The objective is to create a knowledge graph that encapsulates both businesses and their associated meals.
Therefore we will make use of one structured dataset containing the businesses and one unstructured dataset, which includes reviews from those businesses, which we will use for extracting meals.

### YELP Dataset(s): 
**https://www.yelp.com/dataset**
This Yelp dataset includes multiple different datasets.
Our project uses the dataset about businesses and user reviews, which can be downloaded via the link provided.
The review dataset will serve as unstructured, whereas the business dataset will serve as structured data.

**Structured Data:**
**yelp_academic_dataset_business.json**
This JSON file holds all businesses, whereas each business has a unique **businessID**.

**Unstructured Data:**
For our project, we had to shorten the reviews dataset from YELP, since we decided to go with only 1000 reviews since the amount of data was too much to process further (millions).
Therefore we wrote a short script that gave us the first 1000 reviews. **Script: yelp_dataset/rowFilter.py.**
The JSON file **yelp_academic_dataset_review.json** is the result of the shortened review dataset. 
From this dataset, we only use two properties. Namely the **text** property & and **businessId** property.
The **text** property, namely the written reviews is used to extract the meals with the help of NER of food entities.
The **businessId** property is used to link the found meals to the businesses from the structured dataset.

### Summarized:
1. Ontology - The structured dataset is used to build an ontology of (food)-businesses.
2. Ontology - The property **text** from the unstructured dataset is used to gather multiple meals from businesses.
   To conclude, this means when a business has reviews that include meal names, these meals are then mapped to that restaurant.
The mapping between is done via the **businessId**, a property in both datasets.
The result should be something like a meal menu for each business.


### D1.2. RDF data created from the sources (13.12.2023)
As outlined in the first work package (WP1), we have two different datasets.
For both datasets, we provided a Python script, which converts the two JSON datasets from WP1, to RDF data.
This RDF data then can be used to host the knowledge graph on WP3.

**Structured Dataset:**
The Python script that was used to map the business dataset to RDF data is the **business_rdf_converter.py**.
The resulting RDF dataset, used for the 1st ontology, can be found under **business.rdf**

**Unstructured Dataset:**
Before the unstructured dataset could be mapped to RDF an additional step had to be made.
First, we needed to extract only the interesting information from this dataset, namely the **businessId** property and the **text** property.
The **businessId** property is needed for mapping to the structured dataset.
The **text** property is used for NER.
Therefore the **yelp_dataset/reviews.py** was used. 
This Python Script uses a model from a hugging face, which makes NER and is trained on food items.
Initially, we wanted to make the NER ourselves with PythonSpacy, but since it is not trained on food items, it worked out quite badly. 
Since we wanted not to train this model ourselves on food, we made use of an already trained model. 
This model can be found here: https://huggingface.co/Dizex/InstaFoodRoBERTa-NER.
The result of this extraction can be found under: **yelp_dataset/yelp_academic_dataset_review_nlp_processed.json**
**The results of this NER extraction are objects that only include the business for mapping purposes and the different meals associated with that business.
 ``` {
    "meals": [
      "wings",
      "bleu cheese",
      "ribeye",
      "beers"
    ],
    "businessId": "LHSTtnW3YHCeUkRDGyJOyw"
  },
```
After we have our NER processed dataset, again we map this dataset, to RDF data with a Python script.
This can be found under: **meal_rdf_converter.py**
This conversion then results in the final RDF dataset for the 2nd ontology, which can be found under **yelp_dataset/meals.rdf**

**Python Script Mapping**
The mapping in the Python scripts operates as follows: JSON data from datasets are processed using the json library, and the resulting information is transformed into RDF triples using the rdflib library. The scripts utilize a set of mappings to associate dataset properties with corresponding classes and properties defined in the "schema.org" namespace. For instance, the first script focuses on businesses and their attributes, generating RDF triples with classes like LocalBusiness and Rating. Similarly, the second script deals with meals associated with businesses, creating RDF triples with classes such as FoodEstablishment. Provenance information, including creation date, data source, and the number of generated triples, is also added. Finally, the RDF graphs are serialized and exported to rdf files. Both scripts share a common structure for RDF generation, contributing to a standardized representation of Yelp dataset information in RDF format.

## WP2 – Knowledge Hosting:
### D2.1. Knowledge graph stored in a triple store (20.12.2023)
Both RDF files which result from WP2 now can be used to create and host the knowledge graph.
This hosting is done via the GraphDB triple store.
This can be simply done by uploading **both** RDF files, which hold the triples, to GraphDB, via the importRDF option.
Furthermore, in a previous version of our project, it was necessary to link the two ontologies explicitly with a SPARQL query.
***Why?***
Because, on our first attempt, we missed mapping the JSON dataset properties to schema.org classes, which we came up with in-class discussion.
However, since we now added classes to the ontology via the Python RDF mapping script, this connection of the ontologies happens automatically with a unique identifier and is not necessary anymore.

#### Graph Repository Hosting
When both RDF files are to GraphDB, the ontologies now connect automatically via the business, as outlined in the previous section.
Therefore, when uploaded, the Graph Repository is hosted in GraphDB on our **local machine**. 
Therefore the repository was exported as a .rj file and can be accessed under **statements.rj**.

#### Example Queries
Here are two examples of SPARQL queries provided, for better reproducability.
*** Example Query: Menu***
 ```
PREFIX schema: <http://schema.org/>
SELECT ?businessName ?meal
WHERE {
  ?business schema:name ?businessName .
  ?business schema:menu ?meal .
}
```
***Example Query: Provenance information***
 ```
PREFIX schema: <http://schema.org/>

SELECT ?creationDate ?dataSource ?numberOfTriples
WHERE {
  ?provenance schema:creationDate ?creationDate ;
              schema:dataSource ?dataSource ;
              schema:numberOfTriples ?numberOfTriples .
}
```
## WP3 – Knowledge Assessment
### D3.1. Calculation of the quality scores for the correctness and completeness dimensions as well as the
calculation of an aggregated quality score (03.01.2027)
