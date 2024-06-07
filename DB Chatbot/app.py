from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

sqlite_uri = 'sqlite:///./HRDataset.db' 
db = SQLDatabase.from_uri(sqlite_uri)



llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

sql_toolkit=SQLDatabaseToolkit(db=db,llm=llm)
sql_toolkit.get_tools()



# memory = ConversationBufferMemory(memory_key="history", return_messages=True)

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent_executor = create_sql_agent(llm,toolkit=sql_toolkit ,agent_type="openai-tools",verbose=True)

query="give me the data of jack torrence"

response=agent_executor.run(query)

# response=agent_executor.run(prompt.format_prompt(question=query))