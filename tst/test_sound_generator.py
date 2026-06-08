import wave
from pathlib import Path
from src.sound_generator import SoundGenerator
from src.json_parser import JsonParser


TEST_DIR = Path(__file__).parent
INPUTS_DIR = TEST_DIR / "inputs"


def test_write_wav(tmp_path):

	music_file = JsonParser.parse(str(INPUTS_DIR / "good.json"))
	output_file = tmp_path / "output.wav"
	sample_rate = 8000
	generator = SoundGenerator(sample_rate=sample_rate, bit_depth="16-bit")

	try:
		generator.write_wav(str(output_file), music_file)

		assert output_file.exists()
		assert output_file.stat().st_size > 44

		with wave.open(str(output_file), "rb") as wav_file:
			assert wav_file.getnchannels() == 1
			assert wav_file.getsampwidth() == 2
			assert wav_file.getframerate() == sample_rate
			assert wav_file.getnframes() > 0
			assert len(wav_file.readframes(wav_file.getnframes())) > 0
	finally:
		if output_file.exists():
			output_file.unlink()

	assert not output_file.exists()

