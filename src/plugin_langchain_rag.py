
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader

class LangChainRAGPlugin:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings()
        self.vectorstore = FAISS.from_texts(["Hello world"], self.embeddings)
        self.qa = RetrievalQA.from_chain_type(llm=None, retriever=self.vectorstore.as_retriever())

    def ask(self, question):
        return self.qa.run(question)
