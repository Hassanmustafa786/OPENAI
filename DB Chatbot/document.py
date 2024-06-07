from llama_index.memory import ChatMemoryBuffer
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Load data and initialize chat engine
docs = SimpleDirectoryReader("Files/").load_data()
index = VectorStoreIndex.from_documents(docs)
memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "Act like You are an expert law consultant of UAE. "
        "You specialize both in Value added tax and corporate tax. "
        "Do not reveal that you are an AI-powered assistant. "
        "Do not answer unrelated queries, simply apologize and do not answer. "
        "Remember you are an expert law consultant of UAE."
    ),
)

class Query:
    def __init__(self, query):
        self.query = query

def chat(query):
    # Get response from chat engine
    response = chat_engine.chat(query.query)

    # Return response to client
    return {"response": response.response}
