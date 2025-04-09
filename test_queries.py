
def test_queries() -> str:
    ## Add custom query 
    test_queries = [
        "0:work live balance",
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
    
    tq_num = 3           # Which query to use from test_queries list

    sim_count = 1        # How many blogs to return 
    sim_threshold = .1   # What cosine_similarity threshold should be used
    
    return test_queries[tq_num].split(':')[1]