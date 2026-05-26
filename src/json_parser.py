import json

class JsonParser:

    @classmethod
    def parse(cls, filename: str):
        """
        Parse a JSON file and convert to a python dict.

        @param filename (str): The file name of a .json file.

        return (dict): The dict representation of the .json file.
        """
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string value.")
        if ".json" not in filename:
            raise ValueError("File must be of .json format.")
        
        with open(filename, "r") as file:
            return json.load(file)

