from src.pitch_converter import PitchConverter

class Tone:

    def __init__(self, pitch: float, duration: float, amplitude: float):
        """
        Create a tone from a pitch, duration, and amplitude.

        @param pitch (float): The pitch of the tone.
        @param duration (float): The duration of the tone.
        @param amplitude (float): The amplitude of the tone.
        """
        if isinstance(pitch, float): self.frequency = pitch
        elif isinstance(pitch, str): self.frequency = PitchConverter.symbol_to_pitch(pitch)
        self.duration = duration
        if not 0.0 <= amplitude <= 1.0:
            raise ValueError("Amplitude must be between 0.0 and 1.0!")
        self.amplitude = amplitude


    def tones(self) -> list:
        """
        Get the tone as a list.

        return (list[Tone]): The tone inserted into a list.
        """
        return [self]

    def get_duration(self) -> float:
        """
        Get the duration of the tone.

        return (float): The duration of the tone.
        """
        return self.duration

    def data(self) -> tuple[float, float, float]:
        """
        Get the frequency, duration, and amplitude of the tone.

        return (tuple[float, float, float]): The frequency, duration, and amplitude of the tone.
        """
        return (self.frequency, self.duration, self.amplitude)
    
