import pytest

from src.score_reader import ScoreReader


def test_read_scores():
    reader = ScoreReader("mf")
    score = ["C4Q", "F#4H@f", "Bb3E@pp", "E5S", "Db4W@mp"]

    parsed_score = reader.read_score(score)

    assert parsed_score == [
        pytest.approx(("C4", 0.25, 0.65), abs=0.0),
        pytest.approx(("F#4", 0.5, 0.80), abs=0.0),
        pytest.approx(("Bb3", 0.125, 0.20), abs=0.0),
        pytest.approx(("E5", 0.0625, 0.65), abs=0.0),
        pytest.approx(("Db4", 1.0, 0.50), abs=0.0),
    ]


def test_bad_scores():
    reader = ScoreReader("mf")

    with pytest.raises(ValueError, match="A musical score must be formatted as a list."):
        reader.read_score("C4Q")

    with pytest.raises(ValueError, match="All musical notes must be string values."):
        reader.read_score(["C4Q", 42])

    with pytest.raises(ValueError, match=r"Symbol must be note, \[flat or sharp\], octave\. \(ex: Ab4, B#3, C5\)"):
        reader.read_score(["H4Q"])

    with pytest.raises(ValueError, match=r"Symbol must be note, \[flat or sharp\], octave\. \(ex: Ab4, B#3, C5\)"):
        reader.read_score(["C4T"])

    with pytest.raises(ValueError, match=r"Symbol must be note, \[flat or sharp\], octave\. \(ex: Ab4, B#3, C5\)"):
        reader.read_score(["Bb9Q@mf"])

