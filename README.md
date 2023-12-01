# KnowledgeGraphsProject
## Semester Project in Knowledge Graphs from Joey Hieronimy & Julian Hotter

### Dataset: https://www.yelp.com/dataset
The Yelp dataset typically includes datasets about businesses, user reviews, and other related data.
For our purpose, we use the dataset of businesses and reviews.
Reviews will serve as unstructured data whereas businesses will serve as structured data.

### Note:
For our project, we had to shorten both datasets and decided to go with only 1000 reviews since the amount of data was too much to process further.
Therefore we wrote a short script that filtered us all businesses that were named in those 1000 reviews used.

### Unstructured Data:
#### yelp_academic_dataset_review.json
This JSON file holds 1000 reviews from users on Yelp.

### Structured Data:
#### yelp_academic_dataset_business.json
This JSON file holds all businesses, which were mentioned in the reviews of the yelp_academic_dataset_review.json.

Deadlines:
D1.1. Domain Selection and Identification of sources (06.12.2023) ✔️
D1.2. RDF data created from the sources (13.12.2023)
D2.1. Knowledge graph stored in a triple store (20.12.2023)
D3.1. Calculation of the quality scores for the correctness and completeness dimensions as well as the
calculation of an aggregated quality score (03.01.2027)
D4.1. Enriched knowledge graph with linked duplicate instances (17.01.2023)
D5.1. Error detection implementation and a report of the found errors (31.01.2023)
