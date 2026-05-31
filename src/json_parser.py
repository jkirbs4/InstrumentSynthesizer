import json
import re
from src.music_file import MusicFile


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
            json_data: dict = json.load(file) # checks valid JSON format

        errors = [] # collect erros as they are caught
        
        # check first level categories
        if not "instruments" in list(json_data.keys()):
            errors.append("Field 'instruments' must exist in top level of music generation JSON file.")
        if not "tracks" in list(json_data.keys()):
            errors.append("Field 'tracks' must exist in top level of music generation JSON file.")
        
        # check instruments
        instruments = json_data["instruments"]
        if (len(set(instruments.keys())) != len(list(instruments.keys()))):
            errors.append("Duplicate instrument names cannot exist.")
        for instrument, partials in instruments.items():
            if (len(partials) == 0):
                errors.append("At least one partial must exist for the instrument.")
            for p, partial in enumerate(partials):
                if (len(partial) != 2):
                    errors.append("Partial must include [pitch_weight, amplitude_weight] only.")
                json_data["instruments"][instrument][p] = tuple(partial) # convert partial lists to tuples
                try:
                    if not isinstance(partial[0], float):
                        errors.append("Pitch weight must be a float.")
                    if not isinstance(partial[1], float):
                        errors.append("Amplitude weight must be a float.")
                    if not (0.0 <= partial[1] <= 1.0):
                        errors.append("Amplitude weight must be normalized between 0.0 and 1.0.")
                except IndexError, TypeError:
                    pass # error already handled by checking length
                
        # check tracks
        tracks = json_data["tracks"]
        for track in tracks:

            # keys
            if "name" not in list(track.keys()):
                errors.append("Field 'name' must exist in all tracks.")
            if "instrument" not in list(track.keys()):
                errors.append("Field 'instrument' must exist in all tracks.")
            if "dynamic" not in list(track.keys()):
                errors.append("Field 'dynamic' must exist in all tracks.")
            if "notes" not in list(track.keys()):
                errors.append("Field 'notes' must exist in all tracks.")
            
            # value types
            if not isinstance(track["name"], str):
                raise TypeError("Track 'name' must be a string value.")
            if not isinstance(track["instrument"], str):
                raise TypeError("Track 'instrument' must be a string value.")
            if not isinstance(track["dynamic"], str):
                raise TypeError("Track 'dynamic' must be a string value.")
            if not isinstance(track["notes"], list):
                raise TypeError("Track 'notes' must be a list of strings.")
            for note in track["notes"]:
                if not isinstance(note, str):
                    raise TypeError("Track note must be a string value.")
                
            # ensure instrument has been defined
            if track["instrument"] not in list(instruments.keys()):
                errors.append(f"Instrument '{track['instrument']}' must be defined in file.")

            # ensure correct note format
            for note in track["notes"]:
                if not re.fullmatch(r"([A-G])([b#]?)([0-8])([WHQES])(@(pp|mp|mf|ff|p|f))?", note):
                    errors.append(f"Symbol must be note, flat or sharp, octave, duration, [@ dynamic]. (ex: Ab4W, B#3Q, C5E@pf)")

            # ensure nonempty track
            if (len(track["notes"]) == 0):
                errors.append("Track must have at least one note.")

            # raise errors
            if (len(errors) > 0):
                raise ValueError(errors)

        return MusicFile(json_data)

