import pytest
from src.instrument import Instrument
from src.chord import Chord


def test_music_generation():

    instrumentA = Instrument(
        partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
        default_dynamic="pp"
    )
    musicA = instrumentA(["Ab1Q", "B2Q", "C#3H", "Db4Q@pf"])
    instrumentB = Instrument(
        partials=[(1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (5.0, 1.0)],
        default_dynamic="pf"
    )
    musicB = instrumentB(["G#3S", "G2S", "F2E", "F#3E", "C#6Q", "C7W"])
    instrumentC = Instrument(
        partials=[(1.0, 0.9), (2.0, 0.8), (3.0, 0.7), (4.0, 0.6), (1.2, 0.8), (0.8, 0.6), (0.6, 0.4)],
        default_dynamic="mf"
    )
    musicC = instrumentC(["A3W", "Bb3H", "B3W", "C3S", "Db3S", "D3S", "Eb3E", "E3Q", "F3Q", "Gb3H", "G3W"])
    
    assert isinstance(musicA, list)
    for chord in musicA:
        assert isinstance(chord, Chord)

        # test frequencies and amplitudes of each music

    assert isinstance(musicB, list)
    for chord in musicB:
        assert isinstance(chord, Chord)

        # test frequencies and amplitudes of each music

    assert isinstance(musicC, list)
    for chord in musicC:
        assert isinstance(chord, Chord)

        # test frequencies and amplitudes of each music

def test_instrument_data():

    instrument = Instrument(
        partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
        default_dynamic="pp"
    )

    assert instrument.data() == ([(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)], "pp")


def test_bad_partials():

    with pytest.raises(ValueError, match="partials"):
        Instrument(
            partials="hello",
            default_dynamic="pp"
        )
    with pytest.raises(ValueError, match="partials"):
        Instrument(
            partials=[[1.0, 0.8]],
            default_dynamic="pp"
        )
    with pytest.raises(ValueError, match="partials"):
        Instrument(
            partials=[("hello", 0.8)],
            default_dynamic="pp"
        )


def test_bad_dynamic():

    with pytest.raises(ValueError, match="default_dynamic"):
        Instrument(
            partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
            default_dynamic=1
        )
    with pytest.raises(ValueError, match="default_dynamic"):
        Instrument(
            partials=[(1.0, 0.8), (1.2, 0.6), (0.7, 0.5), (2.0, 0.4)],
            default_dynamic="hello"
        )

