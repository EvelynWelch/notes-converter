import argparse


def get_terminal_args():
    '''handles setting up argparse, and returns the results'''
    arg_parser = argparse.ArgumentParser(description="A script to send a note file to an groq for processing.")
    arg_parser.add_argument("file_path", help="the note file path")
    arg_parser.add_argument("--output_file_path", help="the file you wish to output the response to")
    args = arg_parser.parse_args()
    return args

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

def output_handler(args, output):
    '''prints output unless an output_file_path is provided'''   
    if args.output_file_path:
        write_data_to_file(args.output_file_path, output)
        print(f"results written to {args.output_file_path}")
    else:
        print(output)

      
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class ObserverHandler:
    def __init__(self):
        print("ObserverHandler __init__")
        self._observers = {}

    def subscribe(self, observable_name, observer):
        if observable_name not in self._observers.keys():
            self._observers[observable_name] = []
        self._observers[observable_name].append(observer)

    def unsubscribe(self, observable_name, observer):
        self._observers[observable_name].remove(observer)

    def notify(self, observable_name, *args, **kwargs):
        if observable_name in self._observers.keys():
            for func in self._observers[observable_name]:
                func(args, kwargs)