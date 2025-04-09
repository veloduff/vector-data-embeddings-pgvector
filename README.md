# Vector Data and Embeddings

## AWS Services used

* Bedrock
* RDS - PostgreSQL with pgvector
* Parameter Store
* Secrets Manager
* Boto3

## Overview of vectors

**Embeddings as a Tool**
* Embeddings map items **low-dimensional vectors** in a way that similar items are close to each other
* Embeddings can also be applied to dense data (e.g. audio) to create a meaningful similarity metric
* Combining diverse data types (e.g. text, images, audio, ...) as a vector, can help define a similarities between them

**Links**
* <a href="https://aws.amazon.com/what-is/embeddings-in-machine-learning/">Embeddings in Machine Learning</a>
* <a href="https://github.com/aws-samples/aurora-postgresql-pgvector/tree/main/03_SimilaritySearchSentimentAnalysis">Semantic Search and Sentiment Analysis using pgvector, Aurora PostgreSQL and Aurora Machine Learning (Aurora ML)</a>
* <a href="https://catalog.workshops.aws/gtm-sql-vector/en-US/04-bedrock/05-function">Bedrock Similarity Searches</a>

## Data for blogs

Claude 3 Sonnet was used to generate the blogs in `blog_posts.py` with the prompt:

"create a python array with 25 titles and long descriptions of random blog posts"


## Setup a PostgreSQL database with pgvector

1. Create a PostgreSQL database
1. Install and launch pgAdmin
   1. In pgAdmin - Select the database
   1. Launch Query editor
   1. Enable the **vector** extension:
      `create extension vector;`
   1. Verify the **vector** extension is enabled:
      `select * from pg_extension;`
   1. Create the table:
      ```sql
      create table blogs (
        id bigserial primary key,
        title text,
        body text,
        embedding vector(1024) -- 1024 dimensions works for Titan v2
      );
      ```

## Create embeddings and find similar vectors  

1. Create the embeddings for the blogs posts, and store the title, body, and embedding in the database.
   ```sh
   python create_embeddings.py
   ```
1. Setup parameters for finding similar blogs. 
   1. Add a custom query.  In `find_similar.py`, update `test_queries` with a custom query, it must use the `N:description` format, where N is the array number.

      ```py
      test_queries = [
          "0:work life balance",
          "1:Eat amazing global cuisine",
          "2:traveling the world",
          "3:traveling the world eating food and meeting people",
          "4:increase my productivity",
          "5:how can I get in to better shape",
          "6:advice for living",
          "7:meditation",
          "8:work life mediation traveling cooking eating",
          "9:practicing mindfullness while traveling and eating around the world",
          "10:cook amazing food while traveling with friends and family",
      ] 
      tp_num = 10
      ```

   1. Update these variables

      ```py
      tp_num = 10          # Which query to use from test_queries list
      sim_count = 3        # How many blogs to return 
      sim_threshold = .1   # What cosine_similarity threshold should be used
      ```

1. Find similar blogs to the custom query.

   The `SELECT` statement in the `find_similar.py` file uses the cosine distance operator `<=>`, which is included
   in the pgvector extension: https://github.com/pgvector/pgvector#querying

   Find similar blogs: 
   ```sh
   python find_similar.py
   ```

   Example output:

   ```sh
   Using modelId: amazon.titan-embed-text-v2:0
   Using query: "cook amazing food while traveling with friends and family"
   +------+------------------------------------------+----------------------------------------------------------------------------------+---------------------+
   |   id | title                                    | body                                                                             |   cosine_similarity |
   +======+==========================================+==================================================================================+=====================+
   |  474 | The Art of Mindful Travel: Enhancing     | Travel offers the opportunity to explore new landscapes, immerse in diverse      |            0.148774 |
   |      | Your Journey with Presence and Intention | cultures, and create lasting memories. However, the act of traveling can often   |                     |
   |      |                                          | become a rushed and mindless experience, leaving us disconnected from the        |                     |
   |      |                                          | present moment and the richness of our surroundings. This blog post introduces   |                     |
   |      |                                          | the concept of mindful travel, a practice that encourages presence, intention,   |                     |
   |      |                                          | and a deeper appreciation for the journey itself. We explore strategies for      |                     |
   |      |                                          | cultivating mindfulness while on the road, such as slowing down, engaging with   |                     |
   |      |                                          | locals, and savoring the sensory experiences of each destination. Additionally,  |                     |
   |      |                                          | we provide practical tips for planning mindful travel itineraries and packing    |                     |
   |      |                                          | mindfully, ensuring a more fulfilling and memorable adventure.                   |                     |
   +------+------------------------------------------+----------------------------------------------------------------------------------+---------------------+
   |  462 | Exploring the World of Plant-Based       | As the health and environmental benefits of plant-based diets become             |            0.126262 |
   |      | Eating: Benefits, Recipes, and Tips      | increasingly recognized, more people are embracing this lifestyle choice. This   |                     |
   |      |                                          | blog post serves as a comprehensive guide to plant-based eating, exploring the   |                     |
   |      |                                          | nutritional advantages, debunking common myths, and providing practical tips for |                     |
   |      |                                          | transitioning to a plant-rich diet. We also share a collection of delicious and  |                     |
   |      |                                          | nutritious plant-based recipes, showcasing the versatility and flavor of plant-  |                     |
   |      |                                          | based cuisine.                                                                   |                     |
   +------+------------------------------------------+----------------------------------------------------------------------------------+---------------------+
   |  456 | Exploring the World of Mindful Eating:   | In our fast-paced lives, we often consume food mindlessly, without fully         |            0.119938 |
   |      | Nourishing the Body and Soul             | appreciating its flavors, textures, and nutritional value. This blog post        |                     |
   |      |                                          | introduces the concept of mindful eating, a practice that encourages us to savor |                     |
   |      |                                          | each bite and cultivate a deeper connection with our food. We explore the        |                     |
   |      |                                          | benefits of mindful eating, from improved digestion and increased satiety to a   |                     |
   |      |                                          | heightened appreciation for the culinary experience. With practical tips and     |                     |
   |      |                                          | guided exercises, we offer a path to a more nourishing and fulfilling            |                     |
   |      |                                          | relationship with food.                                                          |                     |
   +------+------------------------------------------+----------------------------------------------------------------------------------+---------------------+
   3 blogs found.
   ```






