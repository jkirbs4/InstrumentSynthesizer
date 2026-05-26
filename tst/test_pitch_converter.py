import pytest
from src.pitch_converter import PitchConverter


def test_pitch_conversions():
	assert PitchConverter.symbol_to_pitch("C4") == pytest.approx(261.63)
	assert PitchConverter.symbol_to_pitch("B#4") == pytest.approx(261.63)
	assert PitchConverter.symbol_to_pitch("C#4") == pytest.approx(277.18)
	assert PitchConverter.symbol_to_pitch("Db4") == pytest.approx(277.18)
	assert PitchConverter.symbol_to_pitch("D4") == pytest.approx(293.66)
	assert PitchConverter.symbol_to_pitch("D#4") == pytest.approx(311.13)
	assert PitchConverter.symbol_to_pitch("Eb4") == pytest.approx(311.13)
	assert PitchConverter.symbol_to_pitch("E4") == pytest.approx(329.63)
	assert PitchConverter.symbol_to_pitch("Fb4") == pytest.approx(329.63)
	assert PitchConverter.symbol_to_pitch("F4") == pytest.approx(349.23)
	assert PitchConverter.symbol_to_pitch("E#4") == pytest.approx(349.23)
	assert PitchConverter.symbol_to_pitch("F#4") == pytest.approx(369.99)
	assert PitchConverter.symbol_to_pitch("Gb4") == pytest.approx(369.99)
	assert PitchConverter.symbol_to_pitch("G4") == pytest.approx(392.00)
	assert PitchConverter.symbol_to_pitch("G#4") == pytest.approx(415.30)
	assert PitchConverter.symbol_to_pitch("Ab4") == pytest.approx(415.30)
	assert PitchConverter.symbol_to_pitch("A4") == pytest.approx(440.00)
	assert PitchConverter.symbol_to_pitch("A#4") == pytest.approx(466.16)
	assert PitchConverter.symbol_to_pitch("Bb4") == pytest.approx(466.16)
	assert PitchConverter.symbol_to_pitch("B4") == pytest.approx(493.88)
	assert PitchConverter.symbol_to_pitch("Cb4") == pytest.approx(493.88)


@pytest.mark.parametrize("symbol", ["H4", "A9", "4A", "Bb", "A#10"])
def test_invalid_symbols(symbol):
	with pytest.raises(ValueError, match="Symbol must be note, \[flat or sharp\], octave. \(ex: Ab4, B#3, C5\)"):
		PitchConverter.symbol_to_pitch(symbol)

