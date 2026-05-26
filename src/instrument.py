from src.score_reader import ScoreReader
from src.chord import Chord
from src.pitch_converter import PitchConverter
from src.tone import Tone


class Instrument():

    def __init__(self, harmonics: list, weights: list, default_dynamic: str):
        """
        Initialize the hyperparameters of the instrument.

        @param default_dynamic (str): The dynamic to default to if one is not provided in the note.
        """
        self.score_reader = ScoreReader(default_dynamic)
        if not isinstance(harmonics, list):
            raise ValueError("Harmonics must be a list of positive integer multiples.")
        for harmonic in harmonics:
            if (not isinstance(harmonic, int) or harmonic < 0):
                raise ValueError("Harmonics must be a list of positive integer multiples.")
        if not isinstance(weights, list):
            raise ValueError("Harmonic weights must be a list of float multipliers.")
        for weight in weights:
            if (not isinstance(weight, int) or weight < 0):
                raise ValueError("Harmonic weights must be a list of float multipliers.")
        if (len(harmonics) != len(weights)):
            raise ValueError("A matching pair must exist for each harmonic and weight.")
        self.harmonics = harmonics
        self.weights = weights


    def __call__(self, score: list[str]):

        return self._generate_music(score)
    

    def data(self):

        return (self.harmonics, self.weights, self.default_dynamic)
        

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

        tones = []
        for harmonic, weight in zip(self.harmonics, self.weights):
            tones.append(Tone(base_frequency * harmonic, duration, loudness * weight))

        return Chord(tones)

