import pytest
from pathlib import Path
from src.json_parser import JsonParser
from src.music_file import MusicFile


TEST_DIR = Path(__file__).parent
INPUTS_DIR = TEST_DIR / "inputs"


def test_correct():
	
	json_path = str(INPUTS_DIR / "good.json")
	music_file = JsonParser.parse(json_path)
	
	# test music file attributes
	assert isinstance(music_file, MusicFile)
	assert music_file.instruments() == ["trumpet", "piano", "flute"]
	assert music_file.pitches("trumpet") == [
		1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0
	]
	assert music_file.pitches("piano") == [
		1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0
	]
	assert music_file.pitches("flute") == [
		1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0
	]
	assert music_file.amplitudes("trumpet") == [
		1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.32, 0.25, 0.2, 0.16, 0.12, 0.09, 0.07, 0.05
	]
	assert music_file.amplitudes("piano") == [
		1.0, 0.55, 0.35, 0.25, 0.18, 0.13, 0.1, 0.075, 0.055, 0.04, 0.03, 0.022, 0.016, 0.012, 0.009
	]
	assert music_file.amplitudes("flute") == [
		1.0, 0.28, 0.12, 0.06, 0.03, 0.018, 0.011, 0.007, 0.004, 0.0025, 0.0015, 0.001, 0.0007, 0.0005, 0.0003
	]
	assert music_file.track_names() == ["Track A", "Track B", "Track C"]
	assert music_file.track_notes("Track A") == [
        "C4Q@mf", "E4Q@mf", "G4Q@f", "E4Q@mf",
        "D4Q@mp", "F4Q@mf", "A4Q@f", "G4Q@mf",
        "E4Q@mf", "G4Q@f", "C5H@ff", "A4Q@mf",
        "G4H@mf", "E4H@mf", "C4H@mp", "C4H@mp"
    ]
	assert music_file.track_notes("Track B") == [
        "C3H@mp", "G3H@mp", "E3Q@mf", "A3Q@mp",
        "D3H@mp", "A3H@mp", "G4H@mf", "G4Q@mp",
        "E3H@mp", "C4H@mp", "G2H@mf", "G3H@mf"
    ]
	assert music_file.track_notes("Track C") == [
        "E5E@p", "G5E@p", "C6Q@mp", "G5Q@p",
        "F5E@p", "A5E@p", "D6Q@mp", "A5Q@p",
        "G5E@mp", "E5E@mp", "C5Q@p", "E5Q@mp",
        "G5H@p", "E5H@p", "C5H@mp",
        "G5H@p", "E5H@p", "C5H@mp"
    ]
	assert music_file.track_instrument("Track A") == "trumpet"
	assert music_file.track_instrument("Track B") == "piano"
	assert music_file.track_instrument("Track C") == "flute"
	assert music_file.track_dynamic("Track A") == "mf"
	assert music_file.track_dynamic("Track B") == "mp"
	assert music_file.track_dynamic("Track C") == "p"


def test_key_error_outer():

	json_path = str(INPUTS_DIR / "key_error_outer.json")
	with pytest.raises(KeyError) as error_info:
		JsonParser.parse(json_path)
	
	assert error_info.value.args[0] == [
		"Field 'instruments' must exist in top level of music generation JSON file.",
		"Field 'tracks' must exist in top level of music generation JSON file.",
		"Field 'tempo' must exist in top level of music generation JSON file.",
		"First level fields must only be 'instruments', 'tracks', and 'tempo'."
	]


def test_key_error_inner():

	json_path = str(INPUTS_DIR / "key_error_inner.json")
	with pytest.raises(KeyError) as error_info:
		JsonParser.parse(json_path)
	
	assert error_info.value.args[0] == [
        "Field 'name' must exist in all tracks.",
        "Field 'instrument' must exist in all tracks.",
        "Field 'dynamic' must exist in all tracks.",
        "Field 'notes' must exist in all tracks."
    ]


def test_value_error_general():

	json_path = str(INPUTS_DIR / "value_error_general.json")
	with pytest.raises(ValueError) as error_info:
		JsonParser.parse(json_path)
	
	assert error_info.value.args[0] == [
    	"Partial must include [pitch_weight, amplitude_weight] only.",
    	"Amplitude weight must be a float.",
    	"Pitch weight must be a float.",
        "Partial must include [pitch_weight, amplitude_weight] only.",
        "Partial must include [pitch_weight, amplitude_weight] only.",
        "Amplitude weight must be normalized between 0.0 and 1.0.",
        "At least one partial must exist for the instrument.",
        "At least one partial must exist for the instrument.",
		"Tempo must be a positive value.",
        "Symbol must be note, flat or sharp, octave, duration, [@ dynamic]. (ex: Ab4W, B#3Q, C5E@pf)",
        "Track 'name' must be a string value.",
        "Track 'instrument' must be a string value.",
        "Track 'dynamic' must be a string value.",
        "Track 'notes' must be a list of strings.",
        "Instrument '2.0' must be defined in file.",
        "Track must have at least one note.",
        "Instrument 'trumpets' must be defined in file.",
		"Tracks must have unique names.",
     	"All tracks must share the same length. Be sure that note durations sum to the same total duration for all tracks.\nTrack Lengths = [8, 0, 0]"
    ] 


def test_value_error_track_length():

	json_path = str(INPUTS_DIR / "value_error_track_length.json")
	with pytest.raises(ValueError) as error_info:
		JsonParser.parse(json_path)

	assert error_info.value.args[0] == [
		"Tempo must be an integer value.",
    	"All tracks must share the same length. Be sure that note durations sum to the same total duration for all tracks.\nTrack Lengths = [84, 84, 76]"
    ] 
