from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Load data and initialize chat engine
docs = SimpleDirectoryReader("forms/").load_data()
index = VectorStoreIndex.from_documents(docs)
memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        """ You are a helpful assistant. """
    ),
)

def pdf_chatbot(query):
    response = chat_engine.chat(query)
    return response.response


query = "Hello! Who are you?. And provide me all the names of the employees which works in our bank?"
response = pdf_chatbot(query)
print(response)