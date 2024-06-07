from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

examples = [
        {
            "input": "I want to know about GM.",
            "query": "SELECT * FROM employees WHERE Designation = 'GM';",
        },
        {
            "input": "Find out who is Lisa.",
            "query": "SELECT * FROM employees WHERE Employee_Name = 'Lisa';",
        },
        {
            "input": "List down all designations in Meezan Bank.",
            "query": "SELECT Designation FROM employees;",
        },
        {
            "input": "I want to know about my leaves.",
            "query": "SELECT * FROM employees WHERE Employee_Name = 'John';",
        },
        {
            "input": "List down all the employees.",
            "query": "SELECT * FROM employees;",
        },
        {
            "input": "How many sick leaves do I have?",
            "query": "SELECT `Total Sick Leave` - `Utilized Sick Leave` AS `Remaining Sick Leave` FROM employees WHERE Employee_Name = 'Emily';",
        },
        {
            "input": "Kindly tell me about house finance and auto finance for the supervisor.",
            "query": "SELECT `House Finance`, `Auto Finance` FROM perks WHERE Designation = 'Supervisor';",
        },
        {
            "input": "I want to know about the mobile and petrol perks for the manager.",
            "query": "SELECT `Mobile`, `Petrol` FROM benefits WHERE Designation = 'Manager';",
        },
        {
            "input": "Who has the least number of leaves?",
            "query": "SELECT Employee_Name FROM employees ORDER BY `Remaining Annual Leave` + `Remaining Casual Leave` + `Remaining Sick Leave` ASC LIMIT 1;",
        },
        {
            "input": "Can you tell me the petrol allowance for officers?",
            "query": "SELECT `Petrol` FROM benefits WHERE Designation = 'Officer';",
        },
        {
            "input": "How many employees are there?",
            "query": "SELECT COUNT(*) FROM employees;",
        },
    ]

db = SQLDatabase.from_uri("sqlite:///Excel and databases/Data2.db")
db.dialect
db.get_usable_table_names()
db.run("SELECT * FROM employees;")
db.run("SELECT * FROM perks;")
db.run("SELECT * FROM benefits;")
db.run("SELECT * FROM insurance;")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
sql_memory = ConversationBufferMemory(return_messages=True)


def setup_sql_agent(user_input, llm, db, sql_memory, examples):

    system_prefix = """You are a Meezan Bank HR designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If the question does not seem related to the database, just return "The information you were asking for is not available in the database." as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:"""

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(), 
        FAISS, 
        k=5, 
        input_keys=["input"]
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        verbose=True,
        agent_type="openai-tools",
    )

    agent_response = agent.invoke({"input": user_input})
    output = agent_response['output']

    sql_memory.save_context({"input": user_input}, {"output": output})
    sql_memory.load_memory_variables({})

    return output


# Example usage:
query = "Who is Sarah and tell me her perks and benefits."
agent = setup_sql_agent(query, llm, db, sql_memory, examples)
print(agent)