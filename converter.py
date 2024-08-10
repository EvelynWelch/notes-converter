import os
import argparse

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import private

# TODO: figure out what exactly i need to tell groq for my use case. right now it is the one from the tutorial
MESSAGE_CONTENT = "Give me a list of all the proper nouns, and where they are mentioned in the following text: "
# This is what it responded with, the numbers in the parentheses are what scentences that proper noun is mentioned.

# Here is the list of proper nouns with their corresponding mentions in the text:
# 
# * Ashgrove (Mentions: 1, 2, 3, 5, 7, 9)
# * Tom (Mentions: 1, 2, 5, 7, 9)
# * Ellis (Mentions: 1, 2, 5, 7, 9)
# * Lena (Mentions: 1, 2, 5, 7, 9)
# * Riversend (Mentions: 2, 5)
# * Silverwood Forest (Mentions: 4, 5, 7)
# 
# Note that some of these proper nouns may be mentioned multiple times in the text, but I have only listed each mention once in the above table.

# this is close to what i want, though it to be able to also know what chunks of text are talking about the proper noun without them being mentioned.

def read_file_as_string(file_path):
    '''function to read a file as a string'''
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        return "Error: The file was not found."
    except IOError:
        return "Error: An IOError occurred while reading the file."
    
def write_data_to_file(file_path, data):
    '''funtion to write data to a file'''
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        print(f"Data successfully written to {file_path}")
    except IOError:
        print("Error: An IOError occurred while writing to the file.")

def get_terminal_args():
    '''handles setting up argparse, and returns the results'''
    arg_parser = argparse.ArgumentParser(description="A script to send a note file to an groq for processing.")
    arg_parser.add_argument("file_path", help="the note file path")
    arg_parser.add_argument("--output_file_path", help="the file you wish to output the response to")
    args = arg_parser.parse_args()
    return args

def output_handler(args, parsed_result):
    '''prints output unless an output_file_path is provided'''   
    if args.output_file_path:
        write_data_to_file(args.output_file_path, parsed_result)
        print(f"results written to {args.output_file_path}")
    else:
        print(parsed_result)

def invoke_groq_request(model: ChatGroq, system_message: SystemMessage, human_message: HumanMessage):
    result = model.invoke([system_message, human_message])
    return result

if __name__ == "__main__":
    # set private key as a environment for langchain.
    os.environ["GROQ_API_KEY"] = private.GROQ_API_KEY
    # choose what model to use
    model = ChatGroq(model="llama3-8b-8192")
    # get passed args
    args = get_terminal_args()

    note = read_file_as_string(args.file_path)

    result = invoke_groq_request(
        model=model, 
        system_message=SystemMessage(content=MESSAGE_CONTENT), 
        human_message=HumanMessage(content=note)
        )

    parser = StrOutputParser()
    parsed_result = parser.invoke(result)
 
    output_handler(args, parsed_result)