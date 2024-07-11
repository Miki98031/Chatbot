from langchain.text_splitter import TokenTextSplitter

class TokenSplitter:
    def split(self, docs):
        token_chunk_size = 274
        token_chunk_overlap = 41

        token_text_splitter = TokenTextSplitter(
            chunk_size=token_chunk_size,
            chunk_overlap=token_chunk_overlap,
        )

        splits = token_text_splitter.split_documents(docs)
        return splits
        
