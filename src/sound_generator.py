import wave
import math
import struct
import os

INT_MIN_8, INT_MAX_8 = -128, 127
INT_MIN_16, INT_MAX_16 = -32768, 32767
INT_MIN_24, INT_MAX_24 = -8388608, 8388607 
INT_MIN_32, INT_MAX_32 = -2147483648, 2147483647

SAMP_WIDTH_8 = 1
SAMP_WIDTH_16 = 2
SAMP_WIDTH_24 = 3
SAMP_WIDTH_32 = 4

class SoundGenerator:

    def __init__(self, sample_rate: int = 44100, bit_depth: str = "32-bit"):
        """
        Create a sound generator.

        @param sample_rate (int): The sample rate of the sine wave.
        @param bit_depth (str): The granularity of the muisc.
        """
        self.sample_rate = sample_rate # 44100 is the traditional CD-quality audio sample rate
        self.channels = 1 # only supports mono
        if bit_depth not in ("8-bit", "16-bit", "24-bit", "32-bit"):
            raise ValueError("Bit depth must be '8-bit', '16-bit', '24-bit', or '32-bit'.")
        elif (bit_depth == "8-bit"): self.sample_width = SAMP_WIDTH_8
        elif (bit_depth == "16-bit"): self.sample_width = SAMP_WIDTH_16
        elif (bit_depth == "24-bit"): self.sample_width = SAMP_WIDTH_24
        elif (bit_depth == "32-bit"): self.sample_width = SAMP_WIDTH_32

        
    def write_wav(self, filename: str, notes: list) -> None:
        """
        Convert the music to the WAV file.

        @param filename (str): The WAV file name.
        @param 
        
        more
        """
        if os.path.exists(filename):
            os.remove(filename)

        with wave.open(filename, "w") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(self.sample_width)
            wav.setframerate(self.sample_rate)

            for note in notes:
                tones = note.tones()
                samples = self._note_sample_count(note.get_duration())

                for s in range(samples):
                    time = self._current_time(s, self.sample_rate) # how far into the sound we are

                    sample = 0.0
                    active_tones = 0

                    for tone in tones:
                        frequency, tone_duration, amplitude = tone.data()

                        if time < tone_duration:
                            sample += self._compute_sample(frequency, time, amplitude, tone_duration) # take one sample from the sinusoid
                            active_tones += 1

                    if active_tones > 0:
                        sample /= active_tones

                    sample_int = self._sample_to_int(sample) # make the sample discrete
                    self._write_sample(wav, sample_int) # write sample bytes to .wav file


    def _current_time(self, sample_num: int, sample_rate: int) -> float:
        """
        Get the current time in the sequence.

        @param sample_num (int): The current sample number.
        @param sample_rate (int): The sample rate.
        """
        return sample_num / sample_rate
    

    def _compute_sample(self, frequency: float, time: float, amplitude: float, duration: float) -> float:
        """
        Compute the next sample from the sine wave.

        @param frequency (float): The frequency of the current tone.
        @param time (float): The time of the next sample.
        @param amplitude (float): The amplitude of the current tone.
        @param duration (float): The duration of the current tone.

        return (float): The next sample.
        """
        raw_sample = math.sin(2 * math.pi * frequency * time)
        envelope = self._envelope(time, duration)
        return raw_sample * amplitude * envelope


    def _sample_to_int(self, sample: float) -> int:
        """
        Convert a sample to integer form according to the width.

        @param sample (float): The computed sample from the sine wave.

        return (int): The sample integer.
        """
        sample = max(-1.0, min(1.0, sample))

        if self.sample_width == SAMP_WIDTH_8:
            sample_int = int((sample + 1.0) * 127.5)
            return max(0, min(255, sample_int))
        elif self.sample_width == SAMP_WIDTH_16:
            sample_int = int(sample * INT_MAX_16)
            return max(INT_MIN_16, min(INT_MAX_16, sample_int))
        elif self.sample_width == SAMP_WIDTH_24:
            sample_int = int(sample * INT_MAX_24)
            return max(INT_MIN_24, min(INT_MAX_24, sample_int))
        elif self.sample_width == SAMP_WIDTH_32:
            sample_int = int(sample * INT_MAX_32)
            return max(INT_MIN_32, min(INT_MAX_32, sample_int))
    

    def _note_sample_count(self, duration: float) -> int:
        """
        Get the number of samples.

        @param duration (float): The length of the tone.

        return (int): The number of samples.
        """
        return int(self.sample_rate * duration)
    

    def _envelope(self, time: float, duration: float, fade_time: float = 0.02) -> float:
        """
        Determine a multiplier the sample to dampen the beginning and end amplitudes.

        @param time (float): The current time.
        @param duration (float): The duration of the sample.
        @param fade_time (float): The duration of the dampening on both sides.

        return (float): The multiplier.
        """
        if (time < fade_time): # beginning clip
            return time / fade_time
        if (time > duration - fade_time): # end clip
            return max(0.0, (duration - time) / fade_time)
        
        return 1.0 # no scale for main segment of tone
    

    def _write_sample(self, wav, sample: int) -> None:
        """
        Write a sample to the WAV file.

        @param wav (Wave_write): The wave file being written.
        @param sample (int): The sample to write.
        """
        if (self.sample_width == SAMP_WIDTH_8): wav.writeframes(struct.pack("<B", sample))
        elif (self.sample_width == SAMP_WIDTH_16): wav.writeframes(struct.pack("<h", sample))
        elif (self.sample_width == SAMP_WIDTH_24): wav.writeframes(sample.to_bytes(3, byteorder="little", signed=True)) # no native size for 24-bit in wave lib
        elif (self.sample_width == SAMP_WIDTH_32): wav.writeframes(struct.pack("<i", sample))

