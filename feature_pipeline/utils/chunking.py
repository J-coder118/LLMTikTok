from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

text_splitter = SemanticChunker(OpenAIEmbeddings())

def chunk_text(text: str) -> list[str]:
    text_splitter = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="percentile"
    )
    docs = text_splitter.create_documents([text])
    # check docs[1], len(docs)
    # chunks = []
    return docs
