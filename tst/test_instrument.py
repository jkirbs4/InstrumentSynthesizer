import pytest
from src.instrument import Instrument
from src.chord import Chord
from src.score_reader import ScoreReader
from src.pitch_converter import PitchConverter


def assert_music(music: list[Chord], score: list[str], partials: list[tuple[float, float]], dynamic: str):

    SCORE_READER = ScoreReader(dynamic)
    PITCH_CONVERTER = PitchConverter()

    assert isinstance(music, list)
    for chord in music:
        assert isinstance(chord, Chord)

    score_info: list = SCORE_READER.read_score(score)
    pitches = [pitch for pitch, _, _ in score_info]
    amplitudes = [amplitude for _, _, amplitude in score_info]
    base_frequencies = [PITCH_CONVERTER.symbol_to_pitch(symbol) for symbol in pitches]

    all_frequencies = []
    for frequency in base_frequencies:
        for partial in partials:
            all_frequencies.append(partial[0] * frequency)

    all_amplitudes = []
    for amplitude in amplitudes:
        for partial in partials:
            all_amplitudes.append(partial[1] * amplitude)

    actual_frequencies = [tone.frequency for chord in music for tone in chord.tones()]
    actual_amplitudes = [tone.amplitude for chord in music for tone in chord.tones()]

    assert sorted(actual_frequencies) == pytest.approx(sorted(all_frequencies))
    assert sorted(actual_amplitudes) == pytest.approx(sorted(all_amplitudes))


def test_music_generation():

    scoreA = ["Ab1Q", "B2Q", "C#3H", "Db4Q@f"]
    scoreB = ["G#3S", "G2S", "F2E", "F#3E", "C#6Q", "C7W"]
    scoreC = ["A3W", "Bb3H", "B3W", "C3S", "Db3S", "D3S", "Eb3E", "E3Q", "F3Q", "Gb3H", "G3W"]

    partialsA = [(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)]
    partialsB = [(1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (5.0, 1.0)]
    partialsC = [(1.0, 0.9), (2.0, 0.8), (3.0, 0.7), (4.0, 0.6), (1.2, 0.8), (0.8, 0.6), (0.6, 0.4)]

    dynamicA = "pp"
    dynamicB = "f"
    dynamicC = "mf"

    instrumentA = Instrument(
        partials=partialsA,
        default_dynamic=dynamicA
    )
    musicA = instrumentA(scoreA)
    instrumentB = Instrument(
        partials=partialsB,
        default_dynamic=dynamicB
    )
    musicB = instrumentB(scoreB)
    instrumentC = Instrument(
        partials=partialsC,
        default_dynamic=dynamicC
    )
    musicC = instrumentC(scoreC)
    
    assert_music(musicA, scoreA, partialsA, dynamicA)
    assert_music(musicB, scoreB, partialsB, dynamicB)
    assert_music(musicC, scoreC, partialsC, dynamicC)


def test_instrument_data():

    instrument = Instrument(
        partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
        default_dynamic="pp"
    )

    assert instrument.data() == ([(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)], "pp")


def test_bad_partials():

    with pytest.raises(ValueError, match=r"Partials must be a list of tuples of floats\."):
        Instrument(
            partials="hello",
            default_dynamic="pp"
        )
    with pytest.raises(ValueError, match=r"Each partial must be a tuple of \(pitch_weight, amplitude_weight\)\."):
        Instrument(
            partials=[[1.0, 0.8]],
            default_dynamic="pp"
        )
    with pytest.raises(ValueError, match=r"The pitch weight must be a float\."):
        Instrument(
            partials=[("hello", 0.8)],
            default_dynamic="pp"
        )


def test_bad_dynamic():

    with pytest.raises(ValueError, match=r"Default dynamic must be a string value\."):
        Instrument(
            partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
            default_dynamic=1
        )
    with pytest.raises(ValueError, match=r"Default dynamic must be of \['pp', 'p', 'mp', 'mf', 'f', 'ff'\]\."):
        Instrument(
            partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
            default_dynamic="hello"
        )

