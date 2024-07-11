import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json

class ChromaDatabase:
    def __init__(self, persist_directory):
        if os.path.exists(persist_directory) == False:
            self.persist_directory = persist_directory
            self.db_exists = False

    def _load(self):
        self.db = Chroma(
            embedding_function=OpenAIEmbeddings(), 
            persist_directory=self.persist_directory
        )  

    def _create(self):
        self._load()
        self.db.persist()
        self.db_exists = True

    def _add(self, splits):
        self.db.add_documents(splits)
    
    def _get_db(self):
        return self.db
