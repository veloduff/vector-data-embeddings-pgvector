import json
from vectorEmbedWS import VectorEmbedWS
from find_similar import find_similar

vectorws = VectorEmbedWS()

model_id = vectorws.set_model(
    provider='anthropic', 
    model_id='anthropic.claude-3-sonnet-20240229-v1:0',
)

# sim_query = "Tell me how to be more productive and have better time management."
sim_query = "Suggest reading for home owners" 
sim_blog = (find_similar(verbose=False, sim_query=sim_query)[0])
sim_blog = "Company: IBM  Question: Should I short IBM shares?"
print(sim_blog)

messages = [

    { 
        "role":'user', 
        "content":[{
            'type':'text',
            'text': sim_blog
        }]
    },
    # { 
    #     "role":'assistant', 
    #     "content":[{
    #         'type':'text',
    #         'text': "Time management is crucial, and is the key element for being productive."
    #     }]
    # },
    # { 
    #     "role":'user', 
    #     "content":[{
    #         'type':'text',
    #         'text': "Can you please provide more details for how to find work live balance?"
    #     }]
    # }
]

# system_role = "You are a CTO of a Fortune 500 company speaking with David Faber on Squawk on the Street.",
# system_role = "You are a teenager who is not working and enjoys not have any responsibilities",

system_role = """You are a CEO of hedge fund company that is currently managing 20
              billion dollars in assets. You have recently spoken on Squawk on the
              Street, and frequently give presentations to financial institutions.
              You will be given a question about a company and context for that 
              question. Your primary role is to provide bullish investment advice
              for your customers. If you do not know the company or do not understand
              the context, do not make up an answer, and instead reply with "At this
              time our company does not have an investment strategy for that company".
              """


body=json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_role, 
            "max_tokens": 1000,
            "messages": messages,
            "temperature": 0.5,
            "top_p": 0.9
        }  
    ) 

accept = 'application/json' 
content_type = 'application/json'
# Invoke model 
response = vectorws.bedrock_runtime.invoke_model(
    modelId=model_id, 
    body=body, 
    accept=accept, 
    contentType=content_type
)
response_body = json.loads(response.get('body').read())
print(response_body)



