import json
import re
from src.music_file import MusicFile


class JsonParser:

    @classmethod
    def parse(cls, filename: str) -> MusicFile:
        """
        Parse a JSON file and pack it into a music file object.

        @param filename (str): The file name of a .json file.

        return (MusicFile): The packaged form of the .json file.
        """
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string value.")
        if ".json" not in filename:
            raise ValueError("File must be of .json format.")
        
        with open(filename, "r") as file:
            json_data: dict = json.load(file) # checks valid JSON format

        # collect erros as they are caught
        value_errors = []
        key_errors = []
        
        # check first level categories
        if not "instruments" in list(json_data.keys()):
            key_errors.append("Field 'instruments' must exist in top level of music generation JSON file.")
        if not "tracks" in list(json_data.keys()):
            key_errors.append("Field 'tracks' must exist in top level of music generation JSON file.")

        # raise key errors
        if (len(key_errors) > 0):
            raise KeyError(key_errors)
        
        # check instruments
        instruments = json_data["instruments"]
        if (len(set(instruments.keys())) != len(list(instruments.keys()))):
            value_errors.append("Duplicate instrument names cannot exist.")
        for instrument, partials in instruments.items():
            if (len(partials) == 0):
                value_errors.append("At least one partial must exist for the instrument.")
            for p, partial in enumerate(partials):
                if (len(partial) != 2):
                    value_errors.append("Partial must include [pitch_weight, amplitude_weight] only.")
                json_data["instruments"][instrument][p] = tuple(partial) # convert partial lists to tuples
                try:
                    if not isinstance(partial[0], float):
                        value_errors.append("Pitch weight must be a float.")
                    if not isinstance(partial[1], float):
                        value_errors.append("Amplitude weight must be a float.")
                    if not (0.0 <= partial[1] <= 1.0):
                        value_errors.append("Amplitude weight must be normalized between 0.0 and 1.0.")
                except IndexError, TypeError:
                    pass # error already handled by checking length
                
        # check tracks
        tracks = json_data["tracks"]
        track_lengths = set()
        for track in tracks:

            # keys
            if "name" not in list(track.keys()):
                key_errors.append("Field 'name' must exist in all tracks.")
            if "instrument" not in list(track.keys()):
                key_errors.append("Field 'instrument' must exist in all tracks.")
            if "dynamic" not in list(track.keys()):
                key_errors.append("Field 'dynamic' must exist in all tracks.")
            if "notes" not in list(track.keys()):
                key_errors.append("Field 'notes' must exist in all tracks.")

            # raise key errors
            if (len(key_errors) > 0):
                raise KeyError(key_errors)
            
            # value types
            if not isinstance(track["name"], str):
                value_errors.append("Track 'name' must be a string value.")
            if not isinstance(track["instrument"], str):
                value_errors.append("Track 'instrument' must be a string value.")
            if not isinstance(track["dynamic"], str):
                value_errors.append("Track 'dynamic' must be a string value.")
            if not isinstance(track["notes"], list):
                value_errors.append("Track 'notes' must be a list of strings.")
            else: # track["notes"] is a list
                for note in track["notes"]:
                    if not isinstance(note, str):
                        value_errors.append("Track note must be a string value.")
                    # ensure correct note format
                    if not re.fullmatch(r"([A-G])([b#]?)([0-8])([WHQES])(@(pp|mp|mf|ff|p|f))?", note):
                        value_errors.append(f"Symbol must be note, flat or sharp, octave, duration, [@ dynamic]. (ex: Ab4W, B#3Q, C5E@pf)")
                
                # ensure nonempty track
                if (len(track["notes"]) == 0):
                    value_errors.append("Track must have at least one note.")

                # add to set for track length checking
                track_lengths.add(len(track["notes"]))

            # ensure instrument has been defined
            if track["instrument"] not in list(instruments.keys()):
                value_errors.append(f"Instrument '{track['instrument']}' must be defined in file.")

        # ensure tracks are all the same length
        ...

        # raise value errors
        if (len(value_errors) > 0):
            raise ValueError(value_errors)

        return MusicFile(json_data)

