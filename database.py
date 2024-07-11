from databases.chroma_database import ChromaDatabase
import os
import jsonpickle
import json

def get_database(splits):
    if os.path.exists('chroma.json') == False:
        databases = {
            'chroma' : ChromaDatabase('docs/chroma')
        }

        #add condition for specific database (if necessary)

        database_type = databases['chroma']
        if database_type.db_exists == False:
            database_type._create() 
    
        json_string = jsonpickle.encode(database_type)
        with open('chroma.json', 'w', encoding='utf-8') as f:
            json.dump(json_string, f)

    else:
        with open('chroma.json', 'r') as f:
            json_string = json.load(f)
            database_type = jsonpickle.decode(json_string)
            database_type._load()

    if(len(splits) != 0):
        database_type._add(splits)
        
    return database_type._get_db()