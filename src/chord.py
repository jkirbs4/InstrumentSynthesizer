from src.tone import Tone


class Chord:

    def __init__(self, tones: list[Tone]):
        """
        Create a chord from tones.

        @param tones (list[Tone]): The tones that comprise the chord.
        """
        if (len(tones) < 2):
            raise ValueError("A chord must be comprised of at least two tones.")
        for tone in tones:
            if not isinstance(tone, Tone):
                raise ValueError("A chord must only be comprised of tones.")
            
        self._tones = tones
        self.duration = max(tone.duration for tone in tones)


    def tones(self) -> list[Tone]:
        """
        Get the tones of the chord.

        return (list[Tone]): The tones that comprise the chord.
        """
        return self._tones

    def get_duration(self) -> float:
        """
        Get the duration of the chord.

        return (float): The duration of the chord.
        """
        return self.duration

