from src.instrument import Instrument

"""
Define a standard library of instruments.
"""

instruments = {
    "trumpet": Instrument(
        harmonics=[1, 2, 3, 4],
        weights=[0.75, 0.2, 0.12, 0.06],
        default_dynamic="mf"
    )
}