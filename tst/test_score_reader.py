import pytest

from src.score_reader import ScoreReader


def test_read_scores():
    reader = ScoreReader("mf")
    score = ["C4Q", "F#4H@f", "Bb3E@pp", "RQ", "E5S", "Db4W@mp", "RW"]

    parsed_score = reader.read_score(score)

    assert parsed_score == [
        pytest.approx(("C4", 1.0, 0.65), abs=0.0),
        pytest.approx(("F#4", 2.0, 0.80), abs=0.0),
        pytest.approx(("Bb3", 0.5, 0.20), abs=0.0),
        pytest.approx((None, 1.0, 0.0), abs=0.0),
        pytest.approx(("E5", 0.25, 0.65), abs=0.0),
        pytest.approx(("Db4", 4.0, 0.50), abs=0.0),
        pytest.approx((None, 4.0, 0.0), abs=0.0)
    ]


def test_bad_scores():
    reader = ScoreReader("mf")

    with pytest.raises(ValueError, match="A musical score must be formatted as a list."):
        reader.read_score("C4Q")

    with pytest.raises(ValueError, match="All musical notes must be string values."):
        reader.read_score(["C4Q", 42])

    with pytest.raises(ValueError, match=r"Symbol must be note, flat or sharp, octave, duration, \[@ dynamic\] or a rest R, duration\. \(ex: Ab4W, B#3Q, C5E@pf, RH\)"):
        reader.read_score(["H4Q"])

    with pytest.raises(ValueError, match=r"Symbol must be note, flat or sharp, octave, duration, \[@ dynamic\] or a rest R, duration\. \(ex: Ab4W, B#3Q, C5E@pf, RH\)"):
        reader.read_score(["C4T"])

    with pytest.raises(ValueError, match=r"Symbol must be note, flat or sharp, octave, duration, \[@ dynamic\] or a rest R, duration\. \(ex: Ab4W, B#3Q, C5E@pf, RH\)"):
        reader.read_score(["Bb9Q@mf"])

    with pytest.raises(ValueError, match=r"Symbol must be note, flat or sharp, octave, duration, \[@ dynamic\] or a rest R, duration\. \(ex: Ab4W, B#3Q, C5E@pf, RH\)"):
        reader.read_score(["RR"])

