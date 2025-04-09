from tabulate import tabulate
from vectorEmbedWS import VectorEmbedWS

vectorws = VectorEmbedWS()

def find_similar(verbose=False, sim_query=None):

    if verbose: print(f'Using query: "{sim_query}"') 
    model_id = vectorws.set_model()
    
    ## Connect to database and set cursor
    conn = vectorws.db_conn()
    cur = conn.cursor()
    
    ## Test database connection
    # vectorws.test_db_conn(conn)
    
    sim_count = 3        # How many blogs to return 
    sim_threshold = .01   # What cosine_similarity threshold should be used

    query_embedding, text_token_count = vectorws.get_embedding(model_id, sim_query)
    if verbose: print(f'Text token count: {text_token_count}')

    ## The SELECT statement uses the cosine distance operator <=>, which is included
    ##  in the pgvector extension
    cur.execute(
        """SELECT id, title, body,
            1 - (CAST (embedding as vector) <=> CAST (%s as vector)) AS cosine_similarity
            FROM blogs 
            WHERE 1 - (CAST (embedding as vector) <=> CAST (%s as vector)) > %s 
            ORDER BY cosine_similarity DESC LIMIT %s""", 
        (query_embedding, query_embedding, sim_threshold, sim_count) 
    )

    if verbose: 
        cols = [ x[0] for x in cur.description]
        try:
            print(tabulate(
                cur.fetchall(), 
                headers=cols, 
                tablefmt='grid', 
                maxcolwidths=[None, 40, 80, None]
            ))
            print(f'{cur.rowcount} blogs found.')
            cur.close()
        except IndexError:
            print(f'No similar blogs found with query "{sim_query}" with a similarity greater than {sim_threshold}')
    else:
        similar_blogs = cur.fetchall()
        title_body = list()
        for blog in similar_blogs: 
            title_body.append(blog[1] + ": " + blog[2])

        cur.close()
        return title_body 


if __name__ == "__main__":
    ##print(find_similar(verbose=False)[0][2])
    find_similar(verbose=True)

