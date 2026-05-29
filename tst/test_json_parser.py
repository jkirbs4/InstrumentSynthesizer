from pathlib import Path

from src.json_parser import JsonParser


def test_parse_json():

	json_path = Path(__file__).with_name("test.json")
	parsed = JsonParser.parse(str(json_path))

