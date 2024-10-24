import os
from typing import Dict, Any, List, Iterator
import torch
import yaml
from langchain.chains import RetrievalQA
from langchain.retrievers import EnsembleRetriever
from langchain_community.chat_models import ChatTongyi
from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever, ElasticSearchBM25Retriever
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import CharacterTextSplitter
import dotenv
dotenv.load_dotenv()

llm = ChatTongyi()

with open("./config/config,yaml", 'r') as f:
    params = yaml.safe_load(f)
EMBEDDING_PATH = params["embedding_path"]["linux"]
RERANK_PATH = params["rerank_path"]["linux"]

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
#EMBEDDING_DEVICE = "cpu"


def dao_loader(filepath):
    loader = PyPDFLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    # print(docs)

    return docs


def RAG_search(inputs) -> dict[str, Any]:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_PATH, model_kwargs={'device': EMBEDDING_DEVICE})
    docs = dao_loader("./rag/files/保密法.pdf")
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    doc_list = [doc.page_content for doc in docs]
    bm25_retriever = BM25Retriever.from_texts(
        doc_list, metadatas=[{"source": 1}] * len(doc_list)
    )
    bm25_retriever.k = 2

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever], weights=[0.5, 0.5]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=ensemble_retriever
    )

    return chain.invoke(inputs)


if __name__ == '__main__':
    query = "保密法第三条的内容是什么？"
    result = RAG_search(query)
    print(result)
