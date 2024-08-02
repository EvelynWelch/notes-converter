import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import private

# set private key as a environment for langchain.
os.environ["OPENAI_API_KEY"] = private.open_ai_key


model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

result = model.invoke(messages)

parser = StrOutputParser()
parser.invoke(result)
