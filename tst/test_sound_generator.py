from src.chord import Chord
from src.sound_generator import SoundGenerator
from src.tone import Tone


OUTPUT_FILE = "happy_birthday.wav"
AMPLITUDE = 0.32


def main():
	quarter = 0.38
	half = quarter * 2
	whole = quarter * 4

	score = [
		Tone("G4", quarter, AMPLITUDE),
		Tone("G4", quarter, AMPLITUDE),
		Tone("A4", half, AMPLITUDE),
		Chord([Tone("G4", half, AMPLITUDE), Tone("E4", half, AMPLITUDE * 0.75), Tone("C4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("C5", half, AMPLITUDE), Tone("G4", half, AMPLITUDE * 0.75), Tone("E4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("B4", whole, AMPLITUDE), Tone("G4", whole, AMPLITUDE * 0.75), Tone("D4", whole, AMPLITUDE * 0.75)]),

		Tone("G4", quarter, AMPLITUDE),
		Tone("G4", quarter, AMPLITUDE),
		Tone("A4", half, AMPLITUDE),
		Chord([Tone("G4", half, AMPLITUDE), Tone("F4", half, AMPLITUDE * 0.75), Tone("D4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("D5", half, AMPLITUDE), Tone("A4", half, AMPLITUDE * 0.75), Tone("F4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("C5", whole, AMPLITUDE), Tone("G4", whole, AMPLITUDE * 0.75), Tone("E4", whole, AMPLITUDE * 0.75)]),

		Tone("G4", quarter, AMPLITUDE),
		Tone("G4", quarter, AMPLITUDE),
		Chord([Tone("G5", half, AMPLITUDE), Tone("E5", half, AMPLITUDE * 0.75), Tone("C5", half, AMPLITUDE * 0.75)]),
		Chord([Tone("E5", half, AMPLITUDE), Tone("C5", half, AMPLITUDE * 0.75), Tone("G4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("C5", half, AMPLITUDE), Tone("A4", half, AMPLITUDE * 0.75), Tone("F4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("B4", half, AMPLITUDE), Tone("G4", half, AMPLITUDE * 0.75), Tone("D4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("A4", whole, AMPLITUDE), Tone("F4", whole, AMPLITUDE * 0.75), Tone("C4", whole, AMPLITUDE * 0.75)]),

		Tone("F5", quarter, AMPLITUDE),
		Tone("F5", quarter, AMPLITUDE),
		Chord([Tone("E5", half, AMPLITUDE), Tone("C5", half, AMPLITUDE * 0.75), Tone("G4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("C5", half, AMPLITUDE), Tone("A4", half, AMPLITUDE * 0.75), Tone("F4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("D5", half, AMPLITUDE), Tone("A4", half, AMPLITUDE * 0.75), Tone("F4", half, AMPLITUDE * 0.75)]),
		Chord([Tone("C5", whole, AMPLITUDE), Tone("G4", whole, AMPLITUDE * 0.75), Tone("E4", whole, AMPLITUDE * 0.75)]),
	]

	generator = SoundGenerator(bit_depth="16-bit")
	generator.write_wav(OUTPUT_FILE, score)
	print(f"Saved {OUTPUT_FILE}")


if __name__ == "__main__":
	main()
