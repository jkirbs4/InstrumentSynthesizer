import sys
from src.json_parser import JsonParser
from src.sound_generator import SoundGenerator

def main(filename: str):
    """
    Convert a JSON music file to its .wav counterpart.

    @param filename (str): The JSON file that describes the music.
    """
    # extract data from JSON
    music_file = JsonParser.parse(filename)
    
    # output wave file
    output_file = filename.replace(".json", ".wav")
    generator = SoundGenerator(44100, music_file.bit_depth())
    generator.write_wav(output_file, music_file) # this only takes a list of tones/chords right now


if __name__ == "__main__":
    main(sys.argv[1]) # generate a .wav file from a .json music file

