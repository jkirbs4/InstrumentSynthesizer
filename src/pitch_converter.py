import re


class PitchConverter:

    CONVERSIONS = {
        "C": 261.63,
        "B#": 261.63,
        "C#": 277.18,
        "Db": 277.18,
        "D": 293.66,
        "D#": 311.13,
        "Eb": 311.13,
        "E": 329.63,
        "Fb": 329.63,
        "F": 349.23,
        "E#": 349.23,
        "F#": 369.99,
        "Gb": 369.99,
        "G": 392.00,
        "G#": 415.30,
        "Ab": 415.30,
        "A": 440.00,
        "A#": 466.16,
        "Bb": 466.16,
        "B": 493.88,
        "Cb": 493.88
    }

    @classmethod
    def symbol_to_pitch(cls, symbol: str) -> str:
        """
        Convert a pitch symbol to a number.

        @param symbol (str): The symbol corresponding to a specific pitch number.

        return (str): A pitch number.
        """
        if not re.fullmatch(r"([A-G])([b#]?)([0-8])", symbol):
            raise ValueError("Symbol must be note, [flat or sharp], octave. (ex: Ab4, B#3, C5)")

        if ('b' in symbol or '#' in symbol):
            letter = symbol[0:2]
        else:
            letter = symbol[0]
        octave = int(symbol[-1])

        return cls.CONVERSIONS[letter] * (2 ** (octave - 4))
    
