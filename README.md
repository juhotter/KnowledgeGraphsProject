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

### How is the knowledge combined?
#### The structured dataset is used to build an ontology of restaurants.
#### The unstructured dataset is used to map different dishes to restaurants so that we can derive something like a restaurant menu, like it is done with Google Reviews already.

