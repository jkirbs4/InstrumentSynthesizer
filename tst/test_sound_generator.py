import wave
from src.chord import Chord
from src.sound_generator import SoundGenerator
from src.tone import Tone


def test_write_wav(tmp_path):
	output_file = tmp_path / "output.wav"
	sample_rate = 8000
	generator = SoundGenerator(sample_rate=sample_rate, bit_depth="16-bit")
	score = [
		Tone("C4", 0.10, 0.30),
		Chord([Tone("E4", 0.10, 0.25), Tone("G4", 0.10, 0.20)]),
		Tone("D4", 0.08, 0.35),
		Chord([Tone("F4", 0.12, 0.22), Tone("A4", 0.12, 0.18)]),
		Tone("E4", 0.06, 0.40),
		Chord([Tone("G4", 0.14, 0.28), Tone("B4", 0.14, 0.18)]),
		Tone("F4", 0.09, 0.32),
		Chord([Tone("A4", 0.11, 0.24), Tone("C5", 0.11, 0.16)]),
	]
	expected_frames = sum(int(sample_rate * note.get_duration()) for note in score)

	try:
		generator.write_wav(str(output_file), score)

		assert output_file.exists()
		assert output_file.stat().st_size > 44

		with wave.open(str(output_file), "rb") as wav_file:
			assert wav_file.getnchannels() == 1
			assert wav_file.getsampwidth() == 2
			assert wav_file.getframerate() == sample_rate
			assert wav_file.getnframes() == expected_frames
			assert len(wav_file.readframes(expected_frames)) > 0
	finally:
		if output_file.exists():
			output_file.unlink()

	assert not output_file.exists()

