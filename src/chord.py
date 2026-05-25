from src.tone import Tone


class Chord:

    def __init__(self, tones: list):

        if (len(tones) < 2):
            raise ValueError("A chord must be comprised of at least two tones.")
        for tone in tones:
            if not isinstance(tone, Tone):
                raise ValueError("A chord must only be comprised of tones.")
            
        self._tones = tones
        self.duration = max(tone.duration for tone in tones)


    def tones(self):
        return self._tones

    def get_duration(self):
        return self.duration
