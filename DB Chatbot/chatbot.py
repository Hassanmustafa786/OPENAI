import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

openai_api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo",
    openai_api_key=openai_api_key,
    max_tokens=100,
)
# Create a single memory instance for the entire conversation
memory = ConversationBufferMemory(return_messages=True)

def get_response(input_message, model, memory):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """  You are an helpful AI Assistant.
                        Your response should not be more than 2 to 3 sentences.
                        Your responses should be precise, complete, and consistently maintain a polite and professional tone.
                        """),
        MessagesPlaceholder(variable_name="history"),
        ("human", f"{input_message}"),
    ])

    chain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | model
    )

    inputs = {"input": input_message}
    response = chain.invoke(inputs)

    # Save the context for future interactions
    memory.save_context(inputs, {"output": response.content})
    memory.load_memory_variables({})

    return response.content


input_message = "Who are you?"
get_response(input_message, chat, memory)