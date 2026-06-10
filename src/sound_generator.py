import wave
import math
import struct
import os
from src.music_file import MusicFile
from src.instrument import Instrument

INT_MAX_8 = 127
INT_MAX_16 = 32767
INT_MAX_24 = 8388607 
INT_MAX_32 = 2147483647
INT_MIN_16 = -32768
INT_MIN_24 = -8388608
INT_MIN_32 = -2147483648

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

        
    def write_wav(self, filename: str, music_file: MusicFile) -> None:
        """
        Convert the music to the WAV file.

        @param filename (str): The WAV file name.
        @param music_file (MusicFile): The extracted data from the JSON music file.
        """
        if os.path.exists(filename):
            os.remove(filename) # replace current file

        with wave.open(filename, "w") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(self.sample_width)
            wav.setframerate(self.sample_rate)

            # pack music file with chord data according to defined instruments
            self._simulate_instrument_chords(music_file)

            # scale durations by factor according to BPM
            self._bpm_scale(music_file)

            # extract and quantize samples
            quantized_samples = self._sample_and_quantize(music_file)
                        
            # merge track data
            samples = self._collapse_tracks(quantized_samples)

            # write WAV file
            self._write_samples(wav, samples)


    def _simulate_instrument_chords(self, music_file: MusicFile) -> None:
        """
        Modify the music file to represent the chords according to the instruments.

        @param music_file (MusicFile): The synthesizable music data.
        """
        for track_name in music_file.track_names():
            instrument_name = music_file.track_instrument(track_name)
            instrument = Instrument(music_file.partials(instrument_name), music_file.track_dynamic(track_name))
            music_file.add_chords(track_name, instrument(music_file.track_notes(track_name)))


    def _sample_and_quantize(self, music_file: MusicFile) -> dict:
        """
        Sample from the chords and quantize them according to the bit depth.

        @param music_file (MusicFile): The synthesizable music data.

        return (dict): The quantized samples distributed across tracks.
        """
        quantized_samples: dict[str, list[int]] = {}

        for track_name in music_file.track_names():
            track_samples: list[int] = []
            track_chords = music_file.track_chords(track_name)

            elapsed_exact_samples = 0.0
            rendered_samples = 0

            for chord in track_chords:
                tones = chord.tones()

                elapsed_exact_samples += self.sample_rate * chord.get_duration()
                next_rendered_samples = round(elapsed_exact_samples)
                chord_sample_count = next_rendered_samples - rendered_samples

                for s in range(chord_sample_count):
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

                    track_samples.append(self._sample_to_int(sample)) # make the sample discrete
                
                rendered_samples = next_rendered_samples

            quantized_samples[track_name] = track_samples
        
        return quantized_samples
    

    def _bpm_scale(self, music_file: MusicFile) -> None:
        """
        Scale the durations of notes by a factor according to the BPM.
        """
        scalefactor = 60 / music_file.tempo()
        for track_name in music_file.track_names():
            track_chords = music_file.track_chords(track_name)
            for c in range(len(track_chords)):
                chord = track_chords[c]
                for tone in chord.tones():
                    tone.duration = tone.duration * scalefactor
                chord.duration = max(tone.duration for tone in chord.tones())
    

    def _collapse_tracks(self, quantized_samples: dict[str, list[int]]):
        """
        Transform samples from multiple tracks to become one condensed list of samples.

        @param quantized_samples (dict[str, list[int]]): Quantized samples for each track.

        return (list[int]): The condensed samples.
        """
        first_key = next(iter(quantized_samples))
        sample_count = len(quantized_samples[first_key])
        samples = [0] * sample_count # initialize all samples to zero

        for track in list(quantized_samples.keys()): # accumulate sample values
            for s, sample in enumerate(quantized_samples[track]):
                samples[s] += sample

        # divide by number of tracks
        track_count = len(list(quantized_samples.keys()))
        for s, sample in enumerate(samples):
            samples[s] = int(sample / track_count)

        return samples


    def _write_samples(self, wav, samples: list) -> None:
        """
        Write the sample to the WAV file.

        @param wav (Wave_write): The WAV file.
        @param samples (list[int]): A list of integer samples.
        """
        for sample in samples:
            self._write_sample(wav, sample) # write sample bytes to .wav file


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
        Quantize a sample to integer form according to the width.

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

