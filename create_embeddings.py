from vectorEmbedWS import VectorEmbedWS 
from psycopg2.extras import execute_values
from blog_posts import blog_posts

vectorws = VectorEmbedWS()
model_id = vectorws.set_model(verbose=True)

## Connect to database and set cursor
conn = vectorws.db_conn()
cur = conn.cursor()

## Test database connection
# vectorws.test_db_conn(conn)

## Iterate through blog list, get embedding, add as a tuple to a new list 
blog_tuples_list = list()
for blog in blog_posts:
    b_title = blog["title"]
    b_desc  = blog["description"]
    blog_post_text = f'{b_title} {b_desc}'
    embedding, tokens = vectorws.get_embedding(model_id, blog_post_text)
    ## build a list and use for batch insert, values appended need to be a tuple
    blog_tuples_list.append((b_title, b_desc, embedding))

## Insert (batch insert) in to database
table_name = "blogs"
query =  f"INSERT INTO {table_name} (title, body, embedding) VALUES %s;"
execute_values(cur, query, blog_tuples_list)

conn.commit()
cur.close()
print(f'{cur.rowcount} rows affected.')
