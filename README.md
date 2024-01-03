# KnowledgeGraphsProject
## Semester Project in Knowledge Graphs from Joey Hieronimy & Julian Hotter

## WP1 – Knowledge Creation:
### D1.1. Domain Selection and Identification of Sources (06.12.2023)
**Domain Decision:** Our choice involves modeling various businesses listed on YELP, encompassing not only food establishments such as restaurants. Furthermore, we intend to incorporate specific food items into these businesses. For instance, considering the example of McDonald's, the model would include distinct meals like cheeseburgers, hamburgers, Big Mac, and so forth. The objective is to create a knowledge graph that encapsulates both businesses and their associated meals.
Therefore we will make use of one structured dataset containing the businesses and one unstructured dataset, which includes reviews from those businesses, which we will use for extracting meals.

### YELP Dataset(s): <br>
**https://www.yelp.com/dataset** <br>
This Yelp dataset includes multiple different datasets.<br>
Our project uses the dataset about businesses and user reviews, which can be downloaded via the link provided.<br>
The review dataset will serve as unstructured, whereas the business dataset will serve as structured data.

**Structured Data:**<br>
**yelp_dataset/yelp_academic_dataset_business.json** <br>
This JSON file holds all businesses, whereas each business has a unique **businessID**.

**Unstructured Data:**<br>
For our project, we had to shorten the reviews dataset from YELP, since we decided to go with only 1000 reviews since the amount of data was too much to process further (millions).
Therefore we wrote a short script that gave us the first 1000 reviews.<br> **Script: yelp_dataset/rowFilter.py.** <br>
The JSON file **yelp_dataset/yelp_academic_dataset_review.json** is the result of the shortened review dataset. <br>
From this dataset, we only use two properties. Namely the **text** property & and **businessId** property.<br>
The **text** property, namely the written reviews is used to extract the meals with the help of NER of food entities.<br>
The **businessId** property is used to link the found meals to the businesses from the structured dataset.<br>

### Summarized:
1. Ontology - The structured dataset is used to build an ontology of (food)-businesses.
2. Ontology - The property **text** from the unstructured dataset is used to gather multiple meals from businesses.
   To conclude, this means when a business has reviews that include meal names, these meals are then mapped to that restaurant.
The mapping between is done via the **businessId**, a property in both datasets.
The result should be something like a meal menu for each business.


### D1.2. RDF data created from the sources (13.12.2023)
As outlined in the first work package (WP1), we have two different datasets.<br>
For both datasets, we provided a Python script, which converts the two JSON datasets from WP1, to RDF data.<br>
This RDF data then can be used to host the knowledge graph on WP3.

**Structured Dataset:** <br>
The Python script that was used to map the business dataset to RDF data is the **business_rdf_converter.py**. <br>
The resulting RDF dataset, used for the 1st ontology, can be found under **yelp_dataset/business.rdf**.

**Unstructured Dataset:** <br>
Before the unstructured dataset could be mapped to RDF an additional step had to be made. <br>
First, we needed to extract only the interesting information from this dataset, namely the **businessId** property and the **text** property. <br>
The **businessId** property is needed for mapping to the structured dataset. <br>
The **text** property is used for NER. <br>
Therefore the **yelp_dataset/reviews.py** was used.  <br>
This Python Script uses a model from a hugging face, which makes NER and is trained on food items. <br>
Initially, we wanted to make the NER ourselves with PythonSpacy, but since it is not trained on food items, it worked out quite badly.  <br>
Since we wanted not to train this model ourselves on food, we made use of an already trained model.  <br>
This model can be found here: https://huggingface.co/Dizex/InstaFoodRoBERTa-NER. <br>
The result of this extraction can be found under: **yelp_dataset/yelp_academic_dataset_review_nlp_processed.json** <br>
The results of this NER extraction are objects that only include the business for mapping purposes and the different meals associated with that business.
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
After we have our NER processed dataset, again we map this dataset, to RDF data with a Python script. <br>
This can be found under: **meal_rdf_converter.py** <br>
This conversion then results in the final RDF dataset for the 2nd ontology, which can be found under **yelp_dataset/meals.rdf**

**Python Script Mapping**
The mapping in the Python scripts operates as follows: JSON data from datasets are processed using the json library, and the resulting information is transformed into RDF triples using the rdflib library. The scripts utilize a set of mappings to associate dataset properties with corresponding classes and properties defined in the "schema.org" namespace. For instance, the first script focuses on businesses and their attributes, generating RDF triples with classes like LocalBusiness and Rating. Similarly, the second script deals with meals associated with businesses, creating RDF triples with classes such as FoodEstablishment. Provenance information, including creation date, data source, and the number of generated triples, is also added. Finally, the RDF graphs are serialized and exported to rdf files. Both scripts share a common structure for RDF generation, contributing to a standardized representation of Yelp dataset information in RDF format.

## WP2 – Knowledge Hosting:
### D2.1. Knowledge graph stored in a triple store (20.12.2023)
Both RDF files, namely **yelp_dataset/meals.rdf** and **yelp_dataset/business.rdf**, which result from WP2 now can be used to create and host the knowledge graph. <br>
This hosting is done via the GraphDB triple store. <br>
This can be simply done by uploading **both** RDF files, which hold the triples, to GraphDB, via the importRDF option. <br>
Furthermore, in a previous version of our project, it was necessary to link the two ontologies explicitly with a SPARQL query. <br>
***Why?*** <br>
Because, on our first attempt, we missed mapping the JSON dataset properties to schema.org classes, which we came up with in-class discussion. <br>
However, since we now added classes to the ontology via the Python RDF mapping script, this connection of the ontologies happens automatically with a unique identifier and is not necessary anymore.

#### Graph Repository Hosting
When both RDF files are to GraphDB, the ontologies now connect automatically via the business, as outlined in the previous section. <br>
Therefore, when uploaded, the Graph Repository is hosted in GraphDB on our **local machine**.  <br>
Therefore the repository was exported as a .rj file and can be accessed under **statements.rj**.

With our dataset now being correctly mapped to the appropriate schema.org classes, we are now able to visualize our data in the GraphDB Workbench. When viewing the class hierarchy, we can see that, unsurprisingly, we don't have a real hierarchy, but rather a set of separate classes. The classes are schema:LocalBusiness, schema:Rating, schema:FoodEsteblishment and schema:Provenance. In the hierarchy, we can see that there exist a lot more examples in the schema:Localbusiness class compared to schema:Foodestablishment. This is due to the fact that, firstly not every business from the dataset is a food-based business, and secondly, the foods served by the places are extracted from the reviews about that place, and not every review contains information about food served.
![class-hierarchy-KG-Project](https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/ee117bc6-b4a4-445a-a86f-38b6545972d8)

We are now also able to visualise the relationship of an example business. For this, we can navigat to the "Visual Graph" tab in the GraphDB Workbench and enter an example URI of a given business. In the image below, you can see the example of "Landry's Seafood House". We can observe that it is connected to the schema:LocalBusiness, schema:Rating and Schema:FoodEstablishment classes. The connection to schema:FoodEstablishment is there because a review contained a mention of at least a food product served at the restaurant. Notice how items from the menu are listed as a property of the business, as we can see 9 items in the "menu" property of this place, including bread, fish and mushrooms. This signals that the linking of both datasets worked as expected.
<img width="715" alt="graph_example" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/26a159d9-de51-411a-a2a8-8e5b81f583b6">


#### Example Queries

We imported the classes as two separate named graphs, **business** and **meals**. However, as mentioned above, since linking is not necessary anymore due to the unique identifiers overlapping in both datasets, we could update the queries as not to specify the named graph anymore, but we can simply extract the necessary information from the default graph.

Here are two examples of SPARQL queries provided, for better reproducability.

***Example Query: Menu***
This query outputs the name as well as all the menu items from every establishment that has a menu. Having a successful output of this query means a successful linkage of both dataset, as the connection between the properties of the business, such as name, are completely separate in the dataset from the menu items, and the linking only happens inside GraphDB. Shown below are the first 20 rows of the output.
 ```
PREFIX schema: <http://schema.org/>
SELECT ?businessName ?meal
WHERE {
  ?business schema:name ?businessName .
  ?business schema:menu ?meal .
}
```
***Output:***
<img width="1039" alt="name_menu output" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/48cd0d5b-a2b5-47e8-9696-719afa9eadd9">

***Example Query: Provenance information***
This query shows the provenance information of the entire linked graph, which means the creation date of data, the source where we have it from, and the number of triples inside each graph. The two rows shown in the output below are the business graph as well as the meals graph. The amount of triples in the meals graph is so low since the triples are only created once for each business offering food, rather than for every food item anew.
 ```
PREFIX schema: <http://schema.org/>

SELECT ?creationDate ?dataSource ?numberOfTriples
WHERE {
  ?provenance schema:creationDate ?creationDate ;
              schema:dataSource ?dataSource ;
              schema:numberOfTriples ?numberOfTriples .
}
```
***Output***
<img width="1037" alt="provenance output" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/c7e70835-0259-4958-8a25-bd8958833884">

## WP3 – Knowledge Assessment
### D3.1. Calculation of the quality scores for the correctness and completeness dimensions as well as the calculation of an aggregated quality score <br>

To assess the quality score of our knowledge graph, we will evaluate it based on two dimensions: correctness and completeness. Each dimension comprises two distinct metrics.<br>

#### Dimension Correctness
For this dimension, we decided to use the following two metrics:<br>

**Population completeness:** <br>
This refers to the degree to which KG covers a basic population. <br>
Therefore his metric requires a gold standard, which will represent a specific domain. <br>
The gold standard would be the average number of meals that a restaurant generally has, which is around 42 according to Google. <br>
Source: https://supertuffmenus.com/blogs/blog/what-is-the-average-size-of-a-restaurant-menu <br>
We then compare this golden standard with the average number of meals from our food establishment businesses in the knowledge graph. This would be the metric to determine our completeness for meals for a food establishment. <br>

**Data completeness:** <br>
This refers to the missing values in the KG. <br>
Given that our businesses are sourced from the Yelp dataset, which consistently includes all top-level properties such as address, rating, longitude, and latitude, etc., and in cases where these properties are not available, they are represented as null values. In this context, we will assess the presence of null values in the knowledge graph, indicating properties that lack actual information. This analysis will assist us in gauging the data completeness of our businesses.

#### Dimension Accuracy:
For this dimension, we decided to use the following two metrics: <br>

**Syntactic Structure** <br>
In this context, the focus is on examining how certain properties are represented in the knowledge graph. <br>
Therefore a meaningful check on the syntactic structure could involve examining the relevant attributes, such as the address or hours of operation, to ensure correct formatting and consistency. <br>
In our example, we will measure the **hours** property, meaning if the format is the following: <br> 
This can be done via a simple regex filter. <br>
 ```
"hours": {
      "Monday": "8:0-22:0",
      "Tuesday": "8:0-22:0",
      "Wednesday": "8:0-22:0",
      "Thursday": "8:0-22:0",
      "Friday": "8:0-23:0",
      "Saturday": "8:0-23:0",
      "Sunday": "8:0-22:0"
    }
```
**Syntactic validity of property values** <br>
The values here would be the individual meals that come from the Named Entity Recognition (NER), such as "Burger," but also variations like "Bur’ger." These are then compared using a regular expression (REGEX) to filter out meals containing special characters or numbers. For example, "Bur’ger" should not be included, only "Burger." <br>
This count is then compared with the total number of meals. Consequently, we have the number of meals that contain special characters or numbers, which can be processed in the next step. <br>
It's worth noting that there are meals that can be written with an apostrophe, such as "po’boy." However, one can also write this meal as "Po-Boy." We want our knowledge graph to include only meals that contain alphabetical letters, spaces, or hyphens, but no other special characters. Hence, this assessment.

#### Quality Assessment:
**The calculation of the overall quality score for a knowledge graph can be summarized in three steps:**

1. **Deciding on Dimension Weights:**
   - We decided to weight both dimensions equally.

2. **Calculating Metric Values:**
   - Initially, we established weights for the metrics within each dimension. For the Accuracy dimension, we opted for equal weights as the importance of both metrics is relatively comparable. Concerning Completeness, we assigned a weight of 0.6 to Data Completeness and a weight of 0.4 to Population Completeness. This decision was made because the chosen golden standard of 42 meals is somewhat ambiguous.
   - The next step involves formulating the specific formulas for each metric.
    **Calculating Metric Values:**

Initially, we established weights for the metrics within each dimension. For the Accuracy dimension, we opted for equal weights as the importance of both metrics is relatively comparable. Concerning Completeness, we assigned a weight of 0.6 to Data Completeness and a weight of 0.4 to Population Completeness. This decision was made because the chosen golden standard of 42 meals is somewhat ambiguous. The next step involves formulating the specific formulas for each metric.

**Metric: Population Completeness:**
\[ \text{Population Completeness} = \frac{\text{Average Meals per Food Establishment in the KG}}{\text{Average Meals per Restaurant according to Google}} \]

**Metric: Data Completeness:**
\[ \text{Data Completeness} = \frac{\text{Sum of all null Values of All Properties contained in the KG}}{\text{Sum of all Properties without the meal properties}} \]

**Syntactic Structure:**
\[ \text{Syntactic Structure} = \frac{\text{Number of hours which do not adhere to the syntactic structure}}{\text{Total occurrences of the hour property}} \]

**Syntactic Validity of Property Values:**
\[ \text{Syntactic Validity of Property Values} = \frac{\text{Number of meals not adhering to syntactic validity}}{\text{Total number of meals in the KG}} \]







