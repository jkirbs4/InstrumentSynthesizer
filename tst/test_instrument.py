import pytest
from src.instrument import Instrument
from src.chord import Chord
from src.score_reader import ScoreReader


def assert_music(music: list[Chord], score: list[str]):

    assert isinstance(music, list)
    for chord in music:
        assert isinstance(chord, Chord)
    SCORE_READER = ScoreReader("f")
    score_info: list = SCORE_READER.read_score(score)
    pitches = [pitch for pitch, _, _ in score_info]

    for pitch in pitches:
        ...
        ### keep producing info here to fix


def test_music_generation():

    scoreA = ["Ab1Q", "B2Q", "C#3H", "Db4Q@f"]
    scoreB = ["G#3S", "G2S", "F2E", "F#3E", "C#6Q", "C7W"]
    scoreC = ["A3W", "Bb3H", "B3W", "C3S", "Db3S", "D3S", "Eb3E", "E3Q", "F3Q", "Gb3H", "G3W"]

    instrumentA = Instrument(
        partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
        default_dynamic="pp"
    )
    musicA = instrumentA(scoreA)
    instrumentB = Instrument(
        partials=[(1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (5.0, 1.0)],
        default_dynamic="f"
    )
    musicB = instrumentB(scoreB)
    instrumentC = Instrument(
        partials=[(1.0, 0.9), (2.0, 0.8), (3.0, 0.7), (4.0, 0.6), (1.2, 0.8), (0.8, 0.6), (0.6, 0.4)],
        default_dynamic="mf"
    )
    musicC = instrumentC(scoreC)
    
    assert_music(musicA, scoreA)
    assert_music(musicB, scoreB)
    assert_music(musicC, scoreC)


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

