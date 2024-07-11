from splitters.recursive_splitter import RecursiveSplitter
from splitters.token_splitter import TokenSplitter

def split(docs):
    splitters = {
        'recursive': RecursiveSplitter(),   
        'token' : TokenSplitter()
    }

    #add condition for specific splitter (if necessary)
    
    splitter = splitters['recursive']
    
    return splitter.split(docs)
