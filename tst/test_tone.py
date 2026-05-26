import pytest
from src.tone import Tone


def test_numerical_pitch():
	tone = Tone(440.0, 0.5, 0.8)

	assert tone.frequency == pytest.approx(440.0)
	assert tone.duration == pytest.approx(0.5)
	assert tone.get_duration() == pytest.approx(0.5)
	assert tone.amplitude == pytest.approx(0.8)
	assert tone.data() == (pytest.approx(440.0), pytest.approx(0.5), pytest.approx(0.8))


def test_symbol_pitch():
	tone = Tone("A4", 0.25, 0.4)

	assert tone.frequency == pytest.approx(440.0)
	assert tone.duration == pytest.approx(0.25)
	assert tone.get_duration() == pytest.approx(0.25)
	assert tone.amplitude == pytest.approx(0.4)
	assert tone.data() == (pytest.approx(440.0), pytest.approx(0.25), pytest.approx(0.4))


@pytest.mark.parametrize("amplitude", [-0.01, 1.01])
def test_invalid_amplitude(amplitude):
	with pytest.raises(ValueError, match="Amplitude must be between 0.0 and 1.0!"):
		Tone(440.0, 0.5, amplitude)


def test_tones_list():
	tone = Tone(261.63, 1.0, 0.6)

	assert tone.tones() == [tone]

