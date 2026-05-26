from pathlib import Path

from src.json_parser import JsonParser


def test_parse_json():
	json_path = Path(__file__).with_name("test.json")
	parsed = JsonParser.parse(str(json_path))

	assert "trumpet@mf" in parsed
	assert "piano@mp" in parsed
	assert "flute@p" in parsed