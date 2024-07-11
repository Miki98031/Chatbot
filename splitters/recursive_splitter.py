from langchain.text_splitter import RecursiveCharacterTextSplitter

class RecursiveSplitter:
    def split(self, docs):
        chunk_size = 1000
        chunk_overlap = 150
        separators = ['\n\n', '\n', '(?<=\.)', ' ', '']

        rc_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators
        )

        splits = rc_text_splitter.split_documents(docs)
        return splits
        
