from abc import ABC, abstractmethod
from src.score_reader import ScoreReader


class Instrument(ABC):

    def __init__(self, default_dynamic: str):
        """
        Initialize the hyperparameters of the instrument.

        @param default_dynamic (str): The dynamic to default to if one is not provided in the note.
        """
        self.score_reader = ScoreReader(default_dynamic)


    @abstractmethod
    def generate_music(score: list[str]):
        """
        Generate a sequence of chords according to the instrument type.

        @param score (list[str]): A sequence of notes.

        return (list[Chord]): A sequence of chords particular to the instrument.
        """
        return NotImplementedError("Please implement generate_music()")
    

    def _read_score(self, score):
        """
        Read the notes of a score and parse information.
        
        @param score (list): The list of notes to parse.

        return (list[tuple[str, float, float]]): The parsed information as a list of (pitch, duration, loudness).
        """
        # use in generate_music() for inheriting class
        return self.score_reader.read_score(score)

