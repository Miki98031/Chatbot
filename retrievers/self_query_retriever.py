from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

class SQRetriever():
    def __init__(self, db, llm):
        self.db = db
        self.llm = llm

    def create_metadata(self):
        self.metadata = [
            AttributeInfo(
                name='source',
                description="Chunk should be from `ISO9001.pdf`",
                type='string'
            ),
            AttributeInfo(
                name='page',
                description="The page from the document",
                type='integer'
            )
        ]

        self.document_content_description = 'ISO 9001 standard document'

    def create_retriever(self):
        self.retriever = SelfQueryRetriever.from_llm(
            self.llm,
            self.db,
            self.document_content_description,
            self.metadata,
            verbose=True
        )
        return self.retriever