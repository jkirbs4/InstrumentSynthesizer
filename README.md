# InstrumentSynthesizer
An open source tool to convert musical scores represented by `.json` files to `.wav` audio format. Define instruments based on custom harmonics and timbres

---
## Helpful Definitions

- **_Fundamental Frequency:_** The frequency that serves as a base freqency in which harmonics and timbre stem off of. A note 'owns' a specific frequency, but instruments by definition play a collection of frequencies. The fundamental frequency is processed to produce this set of output frequencies.
- **_Harmonics:_** Integer frequencies that are integer multiples of a fundamental frequency.
- **_Timbre:_** The percieved color or quality of a sound which makes different instruments and vocals distinguishable from one another.
- **_Partials:_** Variations of the fundamental frequency described by scaled frequencies paired with amplitude scales to apply a weight. When integer multiples of the fundamental frequency are applied as partials, harmonics are created. A critical factor in creating timbre is by applying appropriate weights to these derived frequencies.
- **_Chord:_** When multiple musical notes are played together, a harmonious sound is generated. This can be digitally replicated by superimposing waveforms that correspond to partials to create a composite waveform. In addition to a loudness defined by the waveforms amplitude and the sound defined by the embedded frequencies, a chord has a duration.

---
## Music Files
The `InstrumentSynthesizer` tool ingests `.json` files as input, processes them, then outputs `.wav` audio files which can be directly played on a device. It is important to understand the format and rules of writing the files to help a person or AI agent be most effective in creating one. The general format of one of these files is as such:

```
{
  "instruments": {
    "trumpet": [
      [1.0, 1.0], [2.0, 0.9], [3.0, 0.8], [4.0, 0.7],
      [5.0, 0.6], [6.0, 0.5], [7.0, 0.4], [8.0, 0.32],
      [9.0, 0.25], [10.0, 0.2], [11.0, 0.16], [12.0, 0.12],
      [13.0, 0.09], [14.0, 0.07], [15.0, 0.05]
    ],
    "piano": [
      [1.0, 1.0], [2.0, 0.55], [3.0, 0.35], [4.0, 0.25],
      [5.0, 0.18], [6.0, 0.13], [7.0, 0.1], [8.0, 0.075],
      [9.0, 0.055], [10.0, 0.04], [11.0, 0.03], [12.0, 0.022],
      [13.0, 0.016], [14.0, 0.012], [15.0, 0.009]
    ],
    "flute": [
      [1.0, 1.0], [2.0, 0.28], [3.0, 0.12], [4.0, 0.06],
      [5.0, 0.03], [6.0, 0.018], [7.0, 0.011], [8.0, 0.007],
      [9.0, 0.004], [10.0, 0.0025], [11.0, 0.0015], [12.0, 0.001],
      [13.0, 0.0007], [14.0, 0.0005], [15.0, 0.0003]
    ]
  },
  "tracks": [
    {
      "name": "Track A",
      "instrument": "trumpet",
      "dynamic": "mf",
      "notes": [
        "C4Q@mf", "E4Q@mf", "G4Q@f", "E4Q@mf",
        "D4Q@mp", "F4Q@mf", "A4Q@f", "G4Q@mf",
        "E4Q@mf", "G4Q@f", "C5H@ff", "A4Q@mf",
        "G4H@mf", "E4H@mf", "C4H@mp", "C4H@mp"
      ]
    },
    {
      "name": "Track B",
      "instrument": "piano",
      "dynamic": "mp",
      "notes": [
        "C3H@mp", "G3H@mp", "E3Q@mf", "A3Q@mp",
        "D3H@mp", "A3H@mp", "G4H@mf", "G4Q@mp",
        "E3H@mp", "C4H@mp", "G2H@mf", "G3H@mf"
      ]
    },
    {
      "name": "Track C",
      "instrument": "flute",
      "dynamic": "p",
      "notes": [
        "E5E@p", "G5E@p", "C6Q@mp", "G5Q@p",
        "F5E@p", "A5E@p", "D6Q@mp", "A5Q@p",
        "G5E@mp", "E5E@mp", "C5Q@p", "E5Q@mp",
        "G5H@p", "E5H@p", "C5H@mp", "G5H@p",
        "E5H@p", "C5H@mp"
      ]
    }
  ]
}
```
### Features
It is important to make some noteworthy observations regarding this music file:
- **Top-Level Hierarchy:** Everything within the file exists within an object with two keys, which are `"instruments"` and `"tracks"`.
- **Instrument Definition:** The `"instruments"` key refers to the object in which a nonempty collection of sound generation tools can be defined. Each instrument must be defined with a unique key with a value as an array of arrays. The subarrays represent partials defined by ordered pairs of `[pitch_weight, amplitude_weight]`. These values are multiplied by the fundamental frequency and amplitude of each note to produce the instrument's unique sound.
- **Track Definition:** Tracks utilize the defined instruments to create sequences of sound, serving as a programatic musical score. Each track has a `"name"` which serves as a unique identifier. Tracks are assigned a single `"instrument"` from the existing bank of instruments already defined. A default `"dynamic"` is assigned which corresponds to the loudness assigned to each note if a specific loudness is not explicitly provided. Most importantly, the sequence of `"notes"` is structured as an array of string values.

### Note Syntax
A note within `"notes"` is represented as a string value consisting of a letter pitch, an optional flat or sharp, an octave number, the duration, and lastly an optional dynamic specifier. It is specifically recognized by the regular expression `"([A-G])([b#]?)([0-8])([WHQES])(@(pp|mp|mf|ff|p|f))?"`. A flat is represented with the character `"b"` and a sharp is represented by the character `"#"`. Nine octaves are achievable `0-9`, where each step up applies double the pitch. Five potential durations may be selected from, which are represented by the characters `"W"` for a whole note, `"H"` for a half note, `"Q"` for a quarter note, `"E"` for a eighth note, and `"S"` for a sixteenth note. The dynamics and their weight scales are presented below in tabular form:

<div align="center">

<table>
  <tr>
    <th>Dynamic Marking</th>
    <th>Meaning</th>
    <th>Amplitude Multiplier</th>
  </tr>
  <tr>
    <td><code>pp</code></td>
    <td>pianissimo, very soft</td>
    <td>0.20</td>
  </tr>
  <tr>
    <td><code>p</code></td>
    <td>piano, soft</td>
    <td>0.35</td>
  </tr>
  <tr>
    <td><code>mp</code></td>
    <td>mezzo-piano, moderately soft</td>
    <td>0.50</td>
  </tr>
  <tr>
    <td><code>mf</code></td>
    <td>mezzo-forte, moderately loud</td>
    <td>0.65</td>
  </tr>
  <tr>
    <td><code>f</code></td>
    <td>forte, loud</td>
    <td>0.80</td>
  </tr>
  <tr>
    <td><code>ff</code></td>
    <td>fortissimo, very loud</td>
    <td>1.00</td>
  </tr>
</table>

</div>

---
## Chord Implementation

<div align="center">
  <img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/47f50ef5-e028-46fb-8087-53605d443dfc" />
  <br>
  <em>A superposition of two waves forming a resulting waveform.</em>
</div>

---
This project is licensed under the MIT License. See the LICENSE file for details.
