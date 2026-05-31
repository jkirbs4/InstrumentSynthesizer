from json_parser import JsonParser
from sound_generator import SoundGenerator

def main(filename: str):
    """
    Convert a JSON music file to its .wav counterpart.

    @param filename (str): The JSON file that describes the music.
    """
    # extract data from JSON
    music_file = JsonParser.parse(filename)

    # extract instruments and parse scores
    # combine instruments into one stream

    # output wave file
    output_file = filename.replace(".json", ".wav")
    SoundGenerator.write_wav(output_file, ...) # this only takes a list of tones/chords right now


if __name__ == "__main__":
    main()

