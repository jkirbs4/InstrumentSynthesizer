import pytest
from src.chord import Chord
from src.tone import Tone


def test_valid_chord():
	tone_a = Tone("C4", 0.5, 0.8)
	tone_b = Tone("E4", 0.75, 0.6)
	chord = Chord([tone_a, tone_b])

	assert chord.tones() == [tone_a, tone_b]
	assert chord.duration == pytest.approx(0.75)
	assert chord.get_duration() == pytest.approx(0.75)


def test_monotone():
	with pytest.raises(ValueError, match="A chord must be comprised of at least two tones."):
		Chord([Tone("C4", 0.5, 0.8)])


@pytest.mark.parametrize("invalid_tones", [[Tone("C4", 0.5, 0.8), "E4"], [Tone("C4", 0.5, 0.8), 440.0]])
def test_invalid_tone_types(invalid_tones):
	with pytest.raises(ValueError, match="A chord must only be comprised of tones."):
		Chord(invalid_tones)

