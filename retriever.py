from langchain.llms import OpenAI
from retrievers.self_query_retriever import SQRetriever

def get_retriever(db):
    llm = OpenAI(temperature=0.0)
    retrievers = {
       'sqr' : SQRetriever(db, llm) 
    }
    
    #add condition for specific retriever (if necessary)

    retriever_wrapper = retrievers['sqr']
    retriever_wrapper.create_metadata()
    retriever = retriever_wrapper.create_retriever()
    return retriever