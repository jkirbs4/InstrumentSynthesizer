import wave
import math
import struct

sample_rate = 44100
amplitude = 0.4
output_file = "melody.wav"

notes = [
    (440.0, 0.4),  # A4
    (493.88, 0.4), # B4
    (523.25, 0.4), # C5
    (587.33, 0.4), # D5
    (659.25, 0.8), # E5
]

with wave.open(output_file, "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for frequency, duration in notes:
        num_samples = int(sample_rate * duration)

        for i in range(num_samples):
            t = i / sample_rate
            sample = math.sin(2 * math.pi * frequency * t)

            # Simple fade in/out to avoid clicks
            fade_samples = int(sample_rate * 0.01)
            if i < fade_samples:
                sample *= i / fade_samples
            elif i > num_samples - fade_samples:
                sample *= (num_samples - i) / fade_samples

            sample_int = int(sample * amplitude * 32767)
            wav.writeframes(struct.pack("<h", sample_int))

print(f"Saved {output_file}")