from src.score_reader import ScoreReader
from src.chord import Chord
from src.pitch_converter import PitchConverter
from src.tone import Tone


class Instrument:

    def __init__(self, partials: list[tuple], default_dynamic: str):
        """
        Initialize the hyperparameters of the instrument.

        @param partials (list[tuple]): The collection of harmonics and inharmonics listed as (pitch_weight, amplitude_weight).
        @param default_dynamic (str): The dynamic to default to if one is not provided in the note.
        """
        self.score_reader = ScoreReader(default_dynamic)
        if not isinstance(partials, list):
            raise ValueError("Partials must be a list of tuples of floats.")
        for partial in partials:
            if not isinstance(partial, tuple):
                raise ValueError("Each partial must be a tuple of (pitch_weight, amplitude_weight).")
            if not isinstance(partial[0], float):
                raise ValueError("The pitch weight must be a float.")
            if not isinstance(partial[1], float):
                raise ValueError("The amplitude weight must be a float.")
        self.partials = partials


    def __call__(self, score: list[str]):

        return self._generate_music(score)
    

    def data(self):

        return (self.partials, self.default_dynamic)
        

    def _generate_music(self, score: list[str]):
        """
        Generate a sequence of chords according to the instrument type.

        @param score (list[str]): A sequence of notes.

        return (list[Chord]): A sequence of chords particular to the instrument.
        """
        score_info: list = self.score_reader.read_score(score)
        return [self._synthesize_note(pitch, duration, loudness) for pitch, duration, loudness in score_info]
    

    def _synthesize_note(self, pitch: str, duration: float, loudness: float):

        base_frequency = PitchConverter.symbol_to_pitch(pitch)

        tones = [
            Tone(
                base_frequency * pitch_weight,
                duration,
                loudness * amplitude_weight,
            )
            for pitch_weight, amplitude_weight in self.partials
        ]

        return Chord(tones)

