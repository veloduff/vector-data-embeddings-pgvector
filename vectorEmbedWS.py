import os
import sys
import json
import boto3
import psycopg2
from tabulate import tabulate
from blog_posts import blog_posts


class VectorEmbedWS:

    def __init__(self) -> None:
        self.region = 'us-west-2'
        session = boto3.Session(region_name=self.region)
        self.bedrock = session.client('bedrock')
        self.bedrock_runtime = session.client('bedrock-runtime')
        self.rds_client = session.client('rds')
        self.ssm_client = session.client('ssm') 
        self.secret_mgr = session.client('secretsmanager') 


    def get_param(self, param) -> str: 
        response = self.ssm_client.get_parameter(
            Name=param,
            WithDecryption=True
        )
        return response['Parameter']['Value']


    def get_secret(self, secret_name) -> json: 
        get_secret_value_response = self.secret_mgr.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)


    def db_conn(self, endpoint=None, port=None, userName=None, dbname=None, dbSecretName=None, password=None) -> object:
        ENDPOINT     = endpoint if endpoint else self.get_param('/vector-database-01/endpoint')
        PORT         = port if port else self.get_param('/vector-database-01/portNum')
        USER         = userName if userName else self.get_param('/vector-database-01/userName')
        DBNAME       = dbname if dbname else self.get_param('/vector-database-01/dbName')
        dbSecretName = dbSecretName if dbSecretName else self.get_param('/vector-database-01/dbSecretName')
        password     = password if password else self.get_secret(dbSecretName)['password']
        os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
        try:
            conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=password, sslmode='require')
        except Exception as e:
            print("Database connection failed due to {}".format(e))      
        return conn
    

    def test_db_conn(self, conn) -> None:
        ## should print time info
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)


    def available_models(self, provider='amazon', list_all=False) -> list:
        # Find all available Amazon Models
        self.available_models = self.bedrock.list_foundation_models()
        models = list()
        for model in self.available_models['modelSummaries']:
            if provider in model['modelId']:
                models.append(model['modelId'])
                if list_all:
                    print(model['modelId'])
        return models


    def set_model(self, verbose=False, provider='amazon', model_id='amazon.titan-embed-text-v2:0') -> str:
        models = self.available_models(provider, list_all=False)
        model_id = model_id 
        if model_id in models:
            if verbose: print(f'Using model: {model_id}')
            return model_id
        else:
            sys.exit(f'Model not found: {model_id}')


    def data_check(self) -> None:
        for n, bp in enumerate(blog_posts):
            # print(f'{n}:{bp.split(":")[0]}')
            print(f'{n}:{bp["title"]}')


    def get_embedding(self, modelId, prompt_data) -> dict:
        # Define prompt and model parameters
        prompt_data=prompt_data
        body = json.dumps({
            "inputText": prompt_data,
        })
        accept = 'application/json' 
        content_type = 'application/json'
        # Invoke model 
        response = self.bedrock_runtime.invoke_model(
            body=body, 
            modelId=modelId, 
            accept=accept, 
            contentType=content_type
        )
        response_body = json.loads(response['body'].read())
        embedding = response_body.get('embedding')
        textTokenCount = response_body.get('inputTextTokenCount')
        ## Print the Embedding
        # print(f'embedding(first 10): {embedding[:10]}')
        # print(f'embedding_length: {len(embedding)}')
        return embedding, textTokenCount

