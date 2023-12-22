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

#### Structured Data:
**yelp_academic_dataset_business.json**
This JSON file holds all businesses, whereas each business has a unique **businessID**.

#### Unstructured Data:
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

***Structured Dataset:**
The Python script that was used to map the business dataset to RDF data is the **business_rdf_converter.py**.
The resulting RDF dataset can be found under **business.rdf**

***Unstructured Dataset:**
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
After we have our NER processed dataset, again we map this dataset, to RDF data with a python script.
This can be found under: **meal_rdf_converter.py**


## WP2 – Knowledge Hosting:
### D2.1. Knowledge graph stored in a triple store (20.12.2023)
#### Graph Repository
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

## WP3 – Knowledge Assessment
### D3.1. Calculation of the quality scores for the correctness and completeness dimensions as well as the
calculation of an aggregated quality score (03.01.2027)
