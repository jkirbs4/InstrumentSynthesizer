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
        if not "tempo" in list(json_data.keys()):
            key_errors.append("Field 'tempo' must exist in top level of music generation JSON file.")
        if not (len(list(json_data.keys())) == 3):
            key_errors.append("First level fields must only be 'instruments', 'tracks', and 'tempo'.")

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

        # check tempo
        tempo = json_data["tempo"]
        if not isinstance(tempo, int):
            value_errors.append("Tempo must be an integer value.")
        if (tempo <= 0):
            value_errors.append("Tempo must be a positive value.")
                
        # check tracks
        tracks = json_data["tracks"]
        track_lengths = [] # store length for each track
        track_length_scores = { # score proportionate lengths for each note
            "W": 16,
            "H": 8,
            "Q": 4,
            "E": 2,
            "S": 1
        }
        duration_chars = "WHQES"
        track_names = [] # to check for unique track names

        for t, track in enumerate(tracks):

            track_lengths.append(0) # initialize next track length score

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
            track_names.append(track["name"])
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
                    for char in note:
                        if char in duration_chars:
                            duration_char = char
                    track_lengths[t] += track_length_scores[duration_char] # accumulate track length score

                # ensure nonempty track
                if (len(track["notes"]) == 0):
                    value_errors.append("Track must have at least one note.")

            # ensure instrument has been defined
            if track["instrument"] not in list(instruments.keys()):
                value_errors.append(f"Instrument '{track['instrument']}' must be defined in file.")

        # ensure track names are unique
        if (len(track_names) != len(set(track_names))):
            value_errors.append("Tracks must have unique names.")

        # ensure tracks are all the same length
        if (len(set(track_lengths)) != 1):
            value_errors.append("All tracks must share the same length. Be sure that note durations sum to the same total duration for all tracks.\n"
            f"Track Lengths = {track_lengths}")

        # raise value errors
        if (len(value_errors) > 0):
            raise ValueError(value_errors)

        return MusicFile(json_data)

