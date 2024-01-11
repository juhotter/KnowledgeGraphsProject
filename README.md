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
This query outputs the name as well as all the menu items from every establishment that has a menu. Having a successful output of this query means a successful linkage of both dataset, as the connection between the properties of the business, such as name, are completely separate in the dataset from the menu items, and the linking only happens inside GraphDB. Shown below are the first 20 rows of the output, which in total had 3,072 rows.
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

#### Dimension Completeness
For this dimension, we decided to use the following two metrics:<br>

**Population completeness:** <br>
This refers to the degree to which KG covers a basic population. <br>
Therefore his metric requires a gold standard, which will represent a specific domain. <br>
The gold standard would be the average number of meals that a restaurant generally has, which is around 42 according to Google. <br>
Source: https://supertuffmenus.com/blogs/blog/what-is-the-average-size-of-a-restaurant-menu <br>
We then compare this golden standard with the average number of meals from our food establishment businesses in the knowledge graph. This would be the metric to determine our completeness for meals for a food establishment. <br>

The SPARQL query used to get the average amount of meals is shown below. Please note that we only consider the businesses which have at least one meal attached to them, as this allows for a more comprehensive overview. If we were to consider all the businesses, the average would near zero, as we imported a lot more businesses into our KG than we did reviews (2.3 million compared to ~600). The query also returns the total amount of meals as well as the total amount of establishments serving those meals. The output is shown below the query.

```
PREFIX schema: <http://schema.org/>

SELECT
  (AVG(?menuItemCount) as ?averageMenuItems)
  (SUM(?menuItemCount) as ?totalMenuItems)
  (COUNT(DISTINCT ?business) as ?totalBusinesses)
WHERE {
  {
    SELECT ?business (COUNT(?meal) as ?menuItemCount)
    WHERE {
      ?business schema:name ?businessName .
      ?business schema:menu ?meal .
    }
    GROUP BY ?business
  }
}
```
<img width="1000" alt="avg_meals" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/14bab57a-354c-47f4-a026-c79982d42f58">

As we can see, the average amount of meals registered in our graph is 5.28. When comparing this to the golden standard of 42, we have a population completeness of 12.57% in this category.

**Data completeness:** <br>
This refers to the missing values in the KG. <br>
Given that our businesses are sourced from the Yelp dataset, which consistently includes all top-level properties such as address, rating, longitude, and latitude, etc., and in cases where these properties are not available, they are represented as null values. In this context, we will assess the presence of null values in the knowledge graph, indicating properties that lack actual information. This analysis will assist us in gauging the data completeness of our businesses.

To check this, we wrote a query that returns the total amount of businesses that posess a core property. The core attributes in our dataset are the following: name, address, addressLocality, addressRegion, postalCode, latitude, longitude, ratingValue, reviewCount, is_open, category, hoursAvailable. To achieve this, we use the SPARQL "DISTINCT" and "COUNT" keyword, thus count the distinct instances that have a certain property. We only count distinct entities since a business can have multiple instances of the same property.

```
PREFIX schema: <http://schema.org/>

SELECT (COUNT(DISTINCT ?business) as ?countHoursAvailable)
WHERE {
  ?business schema:hoursAvailable ?hoursAvailable .
}
```
<img width="1001" alt="totalHoursAvailable" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/ddb3a7bd-a1ad-46f3-8fee-1b3f348e5e84">

Above is shown an example of how such a query looks to check the total amount of entities that posess the "hoursAvailable" attribute. As we can see, a total of 84564 businesses have this property. We compared every core attribute, by utilizing this query structure, to the total amount of businesses in our graph (100000) and got the following result:

Total | name | address | addressLocality | addressRegion | postalCode | latitude | longitude | ratingValue | reviewCount | category | hoursAvailable | additionalProperty 
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |--- | ---
100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 99931 | 84564 | 90915

As we can see, almost all the entities have all the properties, and only for three distinct attributes (amongst them the less important additionalProperty), we have entities that are missing those attributes. If we take the average of all the properties, we get a completeness of 
**97.95%**.

#### Dimension Correctness(Accuracy):
For this dimension, we decided to use the following two metrics: <br>

<!---
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

In order to achieve this, we wrote wrote a query that checks with the help of a REGEX wheter this property is always true. The regex checks if the first part of the hoursAvailable is any of the weekdays. Next, it checks if the open hours conform to the following pattern: "\\d{1,2}|\\d{1}:\\d{1,2}|\\d{1}-\\d{1,2}|\\d{1}:\\d{1,2}|\\d{1}" . This looks a bit intimidating, but it basically only looks if the structure is "number:number-number:number". We use both \\d{1,2} and \\\\d{1} as possible placeholders for each number since the hours my be given as single or as double digits. If the data in our dataset were saved as e.g. 08:00 instead of 8:0, we could omit all the \\d{1} and only check for \\d{1,2}. The query looks as follows:

```
PREFIX ns1: <http://schema.org/>

SELECT ?businessName ?hoursAvailable
WHERE {
  ?business ns1:hoursAvailable ?hoursAvailable .
  ?business ns1:name ?businessName .

  FILTER (!regex(?hoursAvailable, "^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \\d{1,2}|\\d{1}:\\d{1,2}|\\d{1}-\\d{1,2}|\\d{1}:\\d{1,2}|\\d{1}$"))
}
```
<img width="1000" alt="hours_syntax" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/0fa510f6-2c7d-44d1-977b-3c976ce1fa31">

We can see that all the hours saved do conform to our pattern. This means our score for the syntactic accuracy of the opening hours is 100%. As a sanity check, we also checked the output if we removed the negation of the regex, and indeed it did return the entirety of the opening hours:
<img width="1001" alt="hours" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/3c9efaf3-9c55-4f28-bb34-76cb739d222a">
-->

**Semantic validity of businesses**

To semantically validate our knowledge graph, we want to make sure every business offers at least one meal. To do this, we impose a SHACL constraint that does exactly this. In order to use SHACL constraints in our GraphDB repository, we first had to change the settings, such that it accomodates for SHACL constraints. After this is done, we can upload our .ttl SHACL file as we would normal RDF data, but importing it into a special named graph, the SHACL constraint graph defined in the settings of the repository. The default constraint graph is *http://rdf4j.org/schema/rdf4j#SHACLShapeGraph*. Since we want to impose the restriction that every business must offer at least one meal, our SHACL file looks as follows.

```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix sh: <http://www.w3.org/ns/shacl#>.
@prefix schema: <http://schema.org/>.
@prefix ex: <http://example.org/>.

ex:BusinessShape
  a sh:NodeShape ;
  sh:targetClass schema:LocalBusiness ;
  sh:property [
    sh:path schema:menu ;
    sh:minCount 1 ;
  ] .
```
After having uploaded the file to the SHACL repository, we get a *Failed SHACL validation* error, as naturally not all instances comply to our restriction. the entire validation output is found in the shaclValidationOutput.txt file.

**Syntactic validity of property values** <br>
The values here would be the individual meals that come from the Named Entity Recognition (NER), such as "Burger," but also variations like "Bur’ger." These are then compared using a regular expression (REGEX) to filter out meals containing special characters or numbers. For example, "Bur’ger" should not be included, only "Burger." <br>
This count is then compared with the total number of meals. Consequently, we have the number of meals that contain special characters or numbers, which can be processed in the next step. <br>
It's worth noting that there are meals that can be written with an apostrophe, such as "po’boy." However, one can also write this meal as "Po-Boy." We want our knowledge graph to include only meals that contain alphabetical letters, spaces, or hyphens, but no other special characters. Hence, this assessment.

For this, we wrote a query that returns all the meals that contain other characters than the usual alphabetical letters or spaces.
```
PREFIX schema: <http://schema.org/>

SELECT ?businessName ?meal
WHERE {
  ?business schema:name ?businessName .
  ?business schema:menu ?meal .

  FILTER (regex(?meal, "[^a-zA-Z ]"))
}
```
<img width="1001" alt="sonderzeichen_meals" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/bb6afc34-b492-4509-bfa7-56af13e4729a">

This query returned a total of 81 results, meaning there are only 81 instances of meals in our dataset that do not adhere to the standard characters. If we compare that to the entirety of meals in our graph, 3,072 (see section Example Query: Menu), we can conclude that only 2.63% of the meals deviate from the standard naming scheme. This means we have a syntactic validity of the meal property value of 97.37%.



#### Quality Assessment:
**The calculation of the overall quality score for a knowledge graph can be summarized in three steps:**

1. **Deciding on Dimension Weights:**
   - We decided to weight both dimensions equally, namely 0.5 and 0.5

2. **Calculating Metric Values:**
   - Initially, we established weights for the metrics within each dimension. For the Accuracy dimension, we opted for equal weights as the importance of both metrics is relatively comparable. Concerning Completeness, we assigned a weight of 0.6 to Data Completeness and a weight of 0.4 to Population Completeness. This decision was made because the chosen golden standard of 42 meals is somewhat ambiguous, and therefore the Data Completeness should be weighted a little bit stronger.
   - The next step involves formulating the specific formulas for each metric.
     
      **Metric: Population Completeness:** <br>
      Population Completeness is calculated as the ratio of Average Meals per Food Establishment in the KG to Average Meals per Restaurant according to Google.

      **Metric: Data Completeness:** <br>
      Data Completeness is determined by the ratio of the Sum of all null Values of All Properties contained in the KG to the Sum of all Properties without the meal properties.

      **Syntactic Structure:** <br>
      Syntactic Structure is evaluated as the ratio of the Number of hours that do not adhere to the syntactic structure to the Total occurrences of the hour property.

      **Syntactic Validity of Property Values:** <br>
      Syntactic Validity of Property Values is assessed through the ratio of the Number of meals not adhering to syntactic validity to the Total number of meals in the KG.

3. **Calculating an aggregated quality score:**
    - Finally, based on the defined metrics and weights, the quality score can be determined using the following formular.
      <img width="799" alt="Bildschirmfoto 2024-01-03 um 18 40 57" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/04a1a6ca-1b59-476a-a64d-13eb222cefc0">

   

***Dimension Completeness:***

   Population Completeness: 12.57% <br>
   Data Completeness: 97.95% <br>

   $$ 0.4 \cdot 12.57 + 0.6 \cdot 97.95 = 63,79 $$
   
***Dimension Accuracy***

   Syntactic Structure: 100% <br>
   Syntactic Validity of Property Values: 97.37% <br>

   $$ 0.5 \cdot 100 + 0.5 \cdot 97.37 = 98.68 $$

***Quality Score***

   $$ T(k) = 0.5 \cdot 63,79 + 0.5 \cdot 98.68 = 81.24 $$

We get an overall quality score of **81.24** in our knowledge graph.


## WP4 – Knowledge Enrichment
### D4.1. Enriched knowledge graph with linked duplicate instances <br>


We added hotel data from https://data.world/datafiniti/hotel-reviews/workspace/file?filename=7282_1.csv
We cleaned up the data, removed the reviews as well as duplicate hotels.

Uploaded everything to a new named graph, http://example.com/hotel
Then we connected them using this sparql query, connecting them by city:
```
PREFIX schema: <http://schema.org/>

INSERT {
  GRAPH <http://example.com/connectedByCity> {
    ?business schema:connectedTo ?hotel .
  }
}
WHERE {
  GRAPH <http://example.com/business> {
    ?business schema:addressLocality ?city .
  }
  GRAPH <http://example.com/hotel> {
    ?hotel schema:addressLocality ?city .
    FILTER (?hotel != ?business)  # exclude self-connections
  }
}
```


We can query the businesses and the surrounding hotels with this:

```
PREFIX schema: <http://schema.org/>

SELECT ?businessName ?hotelName
WHERE {
    ?business schema:connectedTo ?hotel .
    ?business schema:name ?businessName .
    ?hotel schema:name ?hotelName .
}
```
<img width="1043" alt="Screenshot 2024-01-11 at 09 43 17" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/fb59597f-3f6c-4fae-99df-313d6dd95576">


If we visualize a business we now get the following. The red is the business, and the yellow are the hotel IDs it is connected to 

<img width="544" alt="business_hotel_visual" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/6c5bb4b0-dc54-4e7c-9658-69c82a10f5d7">


