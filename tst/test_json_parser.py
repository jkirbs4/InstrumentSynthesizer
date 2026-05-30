import pytest
from pathlib import Path
from src.json_parser import JsonParser
from src.music_file import MusicFile


def test_parse_correct_json():

	json_path = str(Path(__file__).with_name("good.json"))
	music_file = JsonParser.parse(json_path)
	
	# test music file attributes
	assert isinstance(music_file, MusicFile)


def test_parse_malformed_json():

	json_path = str(Path(__file__).with_name("bad.json"))
	with pytest.raises(ValueError) as error_info:
		JsonParser.parse(json_path)
	
	assert error_info.value.args[0] == [
		'Partial must include [pitch_weight, amplitude_weight] only.',
		'Amplitude weight must be a float.', 'Pitch weight must be a float.',
		'Partial must include [pitch_weight, amplitude_weight] only.',
		'Partial must include [pitch_weight, amplitude_weight] only.',
		'Amplitude weight must be normalized between 0.0 and 1.0.',
		'At least one partial must exist for the instrument.',
		'At least one partial must exist for the instrument.',
		'Symbol must be note, flat or sharp, octave, duration, [@ dynamic]. (ex: Ab4W, B#3Q, C5E@pf)'
	]

