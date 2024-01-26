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


### D1.2. RDF data created from the sources (13.12.2023) (Hint: See section Extra-WP - Revisit Knowledge Modelling)
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

#### Dimension: Completeness
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

**Domain(Business) completeness:** <br>
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

#### Dimension: Correctness(Accuracy):
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

To semantically validate our knowledge graph, we want to make sure every business offers at least one meal. To do this, we impose a SHACL constraint that does exactly this. In order to use SHACL constraints in our GraphDB repository, we first had to change the settings, such that it accommodates SHACL constraints. After this is done, we can upload our .ttl SHACL file as we would normal RDF data, but importing it into a special named graph, the SHACL constraint graph defined in the settings of the repository. The default constraint graph is *http://rdf4j.org/schema/rdf4j#SHACLShapeGraph*. Since we want to impose the restriction that every business must offer at least one meal, our SHACL file looks as follows. We also check for every other common property of each FoodEstablishment, them being *type, identifier, name, address, addressLocality, addressRegion, postalCode, latitude, longitude, ratingValue, reviewCount, isOpen, category* and *hoursAvailable* wheter everey instance possesses at least one value for each of those. The first lines of our foodEstablishment.ttl file look like this:

```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix sh: <http://www.w3.org/ns/shacl#>.
@prefix schema: <http://schema.org/>.
@prefix ex: <http://example.org/>.

ex:BusinessShape
  a sh:NodeShape ;
  sh:targetClass schema:FoodEstablishment ;
  sh:property [
    sh:path schema:menu ;
    sh:minCount 1 ;
  ] ;
  sh:property [
    sh:path ns1:name ;
    sh:minCount 1 ;
  ] ;
```
After having uploaded the file to the SHACL repository, we get a *Failed SHACL validation* error, as naturally not all instances comply to our restriction. the entire validation output is found in the shaclValidationOutput.txt file.
There were a total of 35 instances that didn't comply to these restraints. After Investigation, we found out that all instances failed on the hoursAvailable minCount.

With 35 erroneous instances out of a total 568 FoodEstablishment, we get a score of 93.84% in this category.

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
   - Initially, we established weights for the metrics within each dimension. For the Accuracy dimension, we opted for equal weights as the importance of both metrics is relatively comparable. Concerning Completeness, we assigned a weight of 0.6 to Domain(Business) Completeness and a weight of 0.4 to Population Completeness. This decision was made because the chosen golden standard of 42 meals is somewhat ambiguous, and therefore the Domain(Business) Completeness should be weighted a little bit stronger.
   - The next step involves formulating the specific formulas for each metric.
     
      **Metric: Population Completeness:** <br>
      Population Completeness is calculated as the ratio of Average Meals per Food Establishment in the KG to Average Meals per Restaurant according to Google.

      **Metric: Domain(Business) Completeness:** <br>
      Domain(Business) is determined by the ratio of the number of all null Values including all businesses in the KG to the Number of all Properties including all businesses.

      **Metric: Semantic validity of businesses:** <br>
      Semantic validity is evaluated as the ratio of the Number of businesses that do not contain at least one meal to the Total number of businesses in our knowledge graph. 

      **Metric: Syntactic Validity of Property Values (meals):** <br>
      Syntactic Validity of Property Values is assessed through the ratio of the Number of meals not adhering to syntactic validity to the Total number of meals in the KG.

3. **Calculating an aggregated quality score:**
    - Finally, based on the defined metrics and weights, the quality score can be determined using the following formula.
      <img width="799" alt="Bildschirmfoto 2024-01-03 um 18 40 57" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/04a1a6ca-1b59-476a-a64d-13eb222cefc0">

   

***Dimension Completeness:***

   Population Completeness: 12.57% <br>
   Domain(Business) Completeness: 97.95% <br>

   $$ 0.4 \cdot 12.57 + 0.6 \cdot 97.95 = 63.79 $$
   
***Dimension Accuracy***

   Semantic validity: 0.5% <br>
   Syntactic Validity of Property Values: 97.37% <br>

   $$ 0.5 \cdot 93.83 + 0.5 \cdot 97.37 = 95.6 $$

   ***Notice:*** The low percentage of Semantic validity can be justified and makes sense since we only included 1000 reviews and had 100.000 Businesses in Total. <br>
   But it is still interesting to see, that 1000 Reviews created meals for about 500 restaurants.

***Quality Score***

   $$ T(k) = 0.5 \cdot 63,79 + 0.5 \cdot 95.6 = 80.19 $$

We get an overall quality score of **56.24** in our knowledge graph.


## WP4 – Knowledge Enrichment
### D4.1. Enriched knowledge graph with linked duplicate instances <br>

In our pursuit of enhancing our knowledge graph, we conceived the idea of linking food establishments to hotels based on their respective cities. This approach is designed to offer users a seamless experience when planning trips to restaurants, enabling them to find hotels within the same city, for example for an overnight stay after a long dinner. For instance, in scenarios where one may have drank a bit too much at a restaurant and requires lodging, our enriched knowledge graph becomes a valuable resource. <br> 
To populate our knowledge graph with hotel data from various cities, we integrated information from (https://data.world/datafiniti/hotel-reviews/workspace/file?filename=7282_1.csv). <br> This information can be mapped to the hotel schema from schema.org (https://schema.org/Hotel).

### Cleaning of the Dataset
In the subsequent step, we rigorously cleaned the data. This involved the removal of duplicate hotels through a meticulous duplicate detection process. Furthermore, we excluded reviews from our dataset, focusing solely on essential properties such as city and hotel properties. For example one hotel as RDF.
```
<rdf:Description rdf:about="http://example.com/hotel/979155f8a2c9">
    <rdf:type rdf:resource="http://schema.org/Hotel"/>
    <ns1:name xml:lang="en">Best Western Owasso Inn &amp; Suites</ns1:name>
    <ns1:address xml:lang="en">7653 N Owasso Expy</ns1:address>
    <ns1:addressLocality xml:lang="en">Owasso</ns1:addressLocality>
    <ns1:country xml:lang="en">US</ns1:country>
    <ns1:latitude rdf:datatype="http://www.w3.org/2001/XMLSchema#double">36.265007</ns1:latitude>
    <ns1:longitude rdf:datatype="http://www.w3.org/2001/XMLSchema#double">-95.846871</ns1:longitude>
    <ns1:postalCode xml:lang="en">74055-3339</ns1:postalCode>
    <ns1:addressRegion xml:lang="en">OK</ns1:addressRegion>
  </rdf:Description>
```
### Scripts and Data
All the necessary scripts for the cleaning process, the resulting dataset, the RDF converter, and the final RDF data can be found in the subfolder `hotels_dataset`.


Everything has been uploaded to a new named graph at http://example.com/hotel. <br>
We then established connections using a SPARQL query, linking the entities based on their respective cities, which are included in the schema.org hotel.addressLocality property.
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


After the linking step, we are now able to query the businesses and the surrounding hotels with the following:

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

Further, we can now visualize a business, where the red signifies the business entity, and the blue represents the connected hotel IDs.<br> 
The connected hotel IDs show that those are the hotels that would be in the same city as the restaurant.
<img width="544" alt="business_hotel_visual" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/6c5bb4b0-dc54-4e7c-9658-69c82a10f5d7">

**Geographical coordinates**

Next, we also wanted to connect the businesses and hotels by their geographical coordinates. These are given as latitude and longitude in each of the instances for hotel and business. For this, we followed the same procedure as above, but only with a slightly augmented query, checking if both the latitude and longitude of both establishments fall inside of 0.05 degrees within another. The reason we first check the city and only after it the geographical coordinates is because of time performance, as it would otherwise be infeasable to loop over each business and hotel. This is of course a slight simplification, as locations within a certain geographical interval do not always fall in the same city, but the benefits of this simplyfication outweigh the edge cases. We chose 0.05 degrees in both directions as our baseline since this corresponds to 6 km, which is a manageable distance even by foot. Below the query is shown the output with additional columns showing the latitude and longitude distance between both businesses.
```
PREFIX schema: <http://schema.org/>

INSERT {
  GRAPH <http://example.com/connectedByGeo> {
    ?business schema:connectedTo ?hotel .
  }
}
WHERE {
  GRAPH <http://example.com/business> {
    ?business schema:addressLocality ?city ;
               schema:latitude ?businessLat ;
               schema:longitude ?businessLong .
  }
  GRAPH <http://example.com/hotel> {
    ?hotel schema:addressLocality ?city ;
           schema:latitude ?hotelLat ;
           schema:longitude ?hotelLong .
    FILTER (?hotel != ?business)  # exclude self-connections
    FILTER (ABS(?businessLat - ?hotelLat) <= 0.1 && ABS(?businessLong - ?hotelLong) <= 0.1)
  }
}
```
<img width="951" alt="Screenshot 2024-01-22 at 16 29 44" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/74101582/bf7cc2ff-5086-4016-898e-59b1e535fd40">

This resulted in a total of 39587 connections, about 36.21% of the 109299 connections made with only the city.
compared to our original dataset of 100000 businesses, the augmentations increased our KG by 39.58% or 109.29% respectively, which is a lot.

##  WP5 - Knowledge Cleaning
### D5.1. Error detection implementation and a report of the found errors (31.01.2023)
The shacle error detection output can be found under *shaclValidationOutput.txt* <br>

How would we clean now the dataset?
- Concerning food establishments that lack at least one meal, we propose removing those establishments from our Knowledge Graph. Therefore, the cleaning step would involve a straightforward deletion process of food establishments. <br>
- Regarding single meals that do not adhere to our proposed schema or are incorrect due to Named Entity Recognition (NER) issues, we have two options. We can either individually examine <br> those properties causing errors and fix them with human domain knowledge or simply remove them. <br>


##  Extra-WP - Revisit Knowledge Modelling
As we found areas for improvement in our modeling approach in WP1, we have chosen to revisit WP1 and make necessary adjustments to enhance the overall modeling. <br>
Therefore we changed the python rdf mapper: the new one can be found under the name *business_rdf_converter_new_modelling.py*
It's crucial to highlight that these adjustments specifically relate to properties that were not employed in assessments and do not have any impact on the rest of WP.
Hence, it is not required to revisit the subsequent WP with the updated modeling.
<br> <br>
We encountered three major issues. <br>
Firstly, the opening hours were represented as simple strings instead of utilizing a dedicated schema.org notation. <br>
Secondly, the categories associated with a restaurant, such as steakhouse or seafood, were stored in an array rather than individually as separate properties. <br>
The third issue pertained to a restaurant having multiple additional pieces of information, such as the property **card_accepted**, which were stored in a basic JSON format with strings instead of being mapped to dedicated schema.org properties.

### First issue - Hours Property<br>
<img width="617" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/5b5efc26-7ed2-4afe-aa33-f0fbe7df6c22"> <br>
As you can see, we modeled the hours available via simple strings.<br>
Now we changed, so that we make use of the schema.org *dayOfTheWeek*, *openingHoursSpecification*, *opens*, and *closes*. <br>
Then the RDF File looks like the following. <br>
<img width="765" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/7523e0a6-0153-4500-974d-cc7d8e689612"> <br>

### Second issue - Category Property <br>
This was quite unspectacular. <br>
Rather than consolidating all categories into a single property, we opted to split them, resulting in the following structure: <br>
<img width="719" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/12e5e7bc-6abc-4109-924c-71dc6fb67b26"> <br>

### Third issue - Attributes Property <br>
The structured dataset from Yelp that we utilize contains an "attributes" property, which encompasses various additional information without a distinct structure.<br>
<img width="827" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/afc6928a-d42e-4f23-a967-fc55d5b218af"> <br>
Until now we just mapped those properties to the business via the schema.org *additionalProperty* property, which makes no real sense. <br>
<img width="541" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/af613c50-f947-4d86-9f4c-1c2c231bc1c1"> <br>
Now we started to look at those properties and to find out which properties have an equivalent to schema.org. <br>
For example, when the additional Attribute is *"BusinessAcceptsCreditCards": "True",*, then we could instead of saving it to the *additionalProperty* property in the RDF,
map it to the schema.org property *paymentAccepted* <br>
<img width="519" alt="image" src="https://github.com/juhotter/KnowledgeGraphsProject/assets/64087284/677c2154-6279-4480-8a99-f65c3bf088a4"> <br>
We employed this approach for a few properties that seemed sensible. However, due to the dataset's size, it is impractical to continue in the same manner. This is intended to provide an initial concept and starting point for how the modeling of this property could be pursued.

## WP 6 - Presentation
The presentation can be found under: <br>
https://docs.google.com/presentation/d/1yqre0ugxCmWim6iGnOxCvcV0aj4rGTAaGO3Yqmwv0BM/edit?usp=sharing





