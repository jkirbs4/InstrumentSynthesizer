from src.instrument import Instrument

"""
Define a standard library of instruments.
"""

instruments = {
    "trumpet": Instrument(
        partials=[
            (1.0, 1.00),
            (2.0, 0.90),
            (3.0, 0.80),
            (4.0, 0.70),
            (5.0, 0.60),
            (6.0, 0.50),
            (7.0, 0.40),
            (8.0, 0.32),
            (9.0, 0.25),
            (10.0, 0.20),
            (11.0, 0.16),
            (12.0, 0.12),
            (13.0, 0.09),
            (14.0, 0.07),
            (15.0, 0.05),
        ],
        default_dynamic="mf",
    )
}

