import re


class ScoreReader:

    def __init__(self, default_dynamic: str):
        """
        Configure the score reader's base behavior.

        @param default_dynamic (str): The default loudness of a note if one is not defined for a note. 
        """
        self.DYNAMICS = {
            "pp": 0.20,
            "p": 0.35,
            "mp": 0.50,
            "mf": 0.65,
            "f": 0.80,
            "ff": 1.00,
        }
        self.DURATIONS = {
            "W": 1.0,
            "H": 0.5,
            "Q": 0.25,
            "E": 0.125,
            "S": 0.0625
        }

        if not isinstance(default_dynamic, str):
            raise ValueError("Default dynamic must be a string value.")
        if default_dynamic not in list(self.DYNAMICS.keys()):
            raise ValueError(f"Default dynamic must be of {list(self.DYNAMICS.keys())}.")
        self.default_dynamic = default_dynamic


    def read_score(self, score: list) -> list[tuple[str, float, float]]:
        """
        Read the notes of a score and parse information.
        
        @param score (list): The list of notes to parse.

        return (list[tuple[str, float, float]]): The parsed information as a list of (pitch, duration, loudness).
        """
        if not isinstance(score, list):
            raise ValueError("A musical score must be formatted as a list.")
        
        return [self._read_note(note) for note in score]

    
    def _read_note(self, note: str) -> tuple[str, float, float]:
        """
        Read a note and parse information 

        return (tuple[str, float, float]]): The parsed information as (pitch, duration, loudness).
        """
        if not isinstance(note, str):
            raise ValueError("All musical notes must be string values.")
        
        if not re.fullmatch(r"([A-G])([b#]?)([0-8])([WHQES])(@(pp|mp|mf|ff|p|f))?", note):
            raise ValueError(f"Symbol must be note, flat or sharp, octave, duration, [@ dynamic]. (ex: Ab4W, B#3Q, C5E@pf)")

        # extract pitch
        if ('b' in note or '#' in note):
            pitch = note[0:3] # includes a flat or sharp
            pitchless_note = note[3:]
        else:
            pitch = note[0:2] # just the letter and octave
            pitchless_note = note[2:]

        # extract duration
        duration_fraction = pitchless_note[0]
        duration = self.DURATIONS[duration_fraction] # convert to number

        # extract dynamic
        if '@' in pitchless_note:
            dynamic = pitchless_note[2:] # extract last one or two characters
        else:
            dynamic = self.default_dynamic # resort to default if none provided
        loudness = self.DYNAMICS[dynamic] # convert to number

        return (pitch, duration, loudness)


        