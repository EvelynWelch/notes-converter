# from langchain_core.messages import HumanMessage, SystemMessageimport os
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import private

# set private key as a environment for langchain.
os.environ["GROQ_API_KEY"] = private.groq_api_key



from langchain_groq import ChatGroq

model = ChatGroq(model="llama3-8b-8192")


# model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

result = model.invoke(messages)

print(result)

parser = StrOutputParser()
print(parser.invoke(result))
