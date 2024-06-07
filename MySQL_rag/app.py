from dotenv import load_dotenv
from operator import itemgetter
from few_shot_examples import examples
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ChatMessageHistory

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
history = ChatMessageHistory()
vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    vectorstore,
    k=2,
    input_keys=["input"],
)

sqlite_uri = 'sqlite:///./HRDataset.db' 
db = SQLDatabase.from_uri(sqlite_uri)


question=""
generate_query = create_sql_query_chain(llm, db)
sql_query = generate_query.invoke({"question": question})
print(sql_query)

execute_query = QuerySQLDataBaseTool(db=db)
execute_query.invoke(sql_query)

chain = generate_query | execute_query


answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user questiony.Your answer should contain thank you at the end of messages.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

rephrase_answer = answer_prompt | llm | StrOutputParser()

chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)


few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input","top_k"],
)



final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Act like an HR.You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for referecne and hsould be considered while answering follow up questions."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

generate_query = create_sql_query_chain(llm, db,final_prompt)

chain = (
# RunnablePassthrough.assign(table_names_to_use=select_table) |
RunnablePassthrough.assign(query=generate_query).assign(
    result=itemgetter("query") | execute_query
)
| rephrase_answer
)

def langchain_query_executor(query):
    response = chain.invoke({"question": query,"messages":history.messages})
    history.add_user_message(query)
    history.add_ai_message(response)
    print(history.messages)
    return response
        
# Example usage:
if __name__ == "__main__":
    query="who are you"
    print(langchain_query_executor(query))
