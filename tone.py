from pitch import PitchConverter

class Tone:

    def __init__(self, pitch: float, duration: float, amplitude: float):

        if isinstance(pitch, float): self.frequency = pitch
        elif isinstance(pitch, str): self.frequency = PitchConverter.symbol_to_pitch(pitch)
        self.duration = duration
        if not 0.0 <= amplitude <= 1.0:
            raise ValueError("Amplitude must be between 0.0 and 1.0!")
        self.amplitude = amplitude


    def tones(self):
        return [self]

    def get_duration(self):
        return self.duration

    def data(self):

        return (self.frequency, self.duration, self.amplitude)
    
