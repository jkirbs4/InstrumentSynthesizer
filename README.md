# InstrumentSynthesizer
An open source tool to convert musical scores represented by `.json` files to `.wav` audio format. Define instruments based on custom harmonics and timbres

<div align="center">
  <img width="600" alt="image" src="https://github.com/user-attachments/assets/3fc7d7c3-f3b6-47ac-9d1a-f523be834abc" />
</div>

---
## Build

_The `InstrumentSynthesizer` is a terminal-based project at this point without a frontend._

1. Clone the repo to your directory.
2. Run `./build.sh` to install dependencies to be able to run the synthesizer.
3. Run `./run.sh` with `music_file.json` as the only argument. The file `music_file.wav` will be the output.

---
## Helpful Definitions
- **_Sinusoid:_** A sine waveform that is continuous, periodic, and can be defined by an amplitude, phase shift, and frequency.
- **_Fundamental Frequency:_** The frequency that serves as a base freqency in which harmonics and timbre stem off of. A note 'owns' a specific frequency, but instruments by definition play a collection of frequencies. The fundamental frequency is processed to produce this set of output frequencies.
- **_Harmonics:_** Integer frequencies that are integer multiples of a fundamental frequency.
- **_Timbre:_** The percieved color or quality of a sound which makes different instruments and vocals distinguishable from one another.
- **_Partials:_** Variations of the fundamental frequency described by scaled frequencies paired with amplitude scales to apply a weight. When integer multiples of the fundamental frequency are applied as partials, harmonics are created. A critical factor in creating timbre is by applying appropriate weights to these derived frequencies.
- **_Superposition:_** The act of summing sinusoides to create a composite sinusoid.
- **_Decomposition:_** The act of breaking down a composite sinusoid into base sinusoids that cannot be further decomposed.
- **_Chord:_** When multiple musical notes are played together, a harmonious sound is generated. This can be digitally replicated by superimposing waveforms that correspond to partials to create a composite waveform. In addition to a loudness defined by the waveforms amplitude and the sound defined by the embedded frequencies, a chord has a duration.
- **_ADC:_** An analog-to-digital converter is a mechanism that transforms real world continuous signals to discrete signals in the virtual world by sampling, quantization, and encoding. This mechanism is built in to the audio codec chip on a modern computer's motherboard.
- **_DAC:_** A digital-to-analog converter is a mechanism that transforms discrete signals in the virtual world to continuous signals in the real world. It operates by generating voltages that map to a binary stream. This mechanism is built in to the audio codec chip on a modern computer's motherboard.

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
- **Track Definition:** Tracks utilize the defined instruments to create sequences of sound, serving as a programatic musical score. Each track has a `"name"` which serves as a unique identifier. Tracks are assigned a single `"instrument"` from the existing bank of instruments already defined. A default `"dynamic"` is assigned which corresponds to the loudness assigned to each note if a specific loudness is not explicitly provided. Most importantly, the sequence of `"notes"` is structured as an array of string values. It is important not to add any more keys or structure to the `.json` file. If any violation is detected by the parser, an error will be raised and the `.wav` file will not be generated.

### Note Syntax
A note within `"notes"` is represented as a string value consisting of a letter pitch, an optional flat or sharp, an octave number, the duration, and lastly an optional dynamic specifier. It is specifically recognized by the regular expression `"([A-G])([b#]?)([0-8])([WHQES])(@(pp|mp|mf|ff|p|f))(R([WHQES]))?"`. Notes `A-G` are accepted, or a rest denoted by `R`. A flat is represented with the character `"b"` and a sharp is represented by the character `"#"`. Nine octaves are achievable `0-9`, where each step up applies double the pitch. Five potential durations may be selected from, which are represented by the characters `"W"` for a whole note, `"H"` for a half note, `"Q"` for a quarter note, `"E"` for a eighth note, and `"S"` for a sixteenth note. The dynamics and their weight scales are presented below in tabular form:

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

The dynamic must succeed a `"@"` character to communicate to the parser correctly. This pattern must be applied to both individual notes and the base `"dynamic"` key defined for a track.

---
## Chord Implementation and Processing

<div align="center">
  <img width="900" height="350" alt="image" src="https://github.com/user-attachments/assets/c1e0b866-0279-44b2-af2d-2ed88d040edf" />
  <br>
  <em>The signal processing flow of a chord.</em>
</div>
<br>

Chords exist when multiple tones are played simultaneously, but how exactly can this be created digitaly? First, it must be acknowledged what a wave is and how to represent it mathematically. The equation of a sinusoid is $y(t) = A \sin(2\pi f t + \phi)$ where $A$ is the amplitude, $f$ is the frequency, $t$ is time, and $\phi$ is the phase shift.

<div align="center">
  <img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/f9b822ea-3df0-4b80-befa-9b6f3c9f00ce" />
  <br>
  <em>A graph of a standard sinusoidal function.</em>
</div>
<br>

> [!Note]
> Rests can also be thought of as a sinusoid, but with zero amplitude. Samples generated for the rest duration will be attributed a value of zero independent of the frequency value.

Second, the base concept of a Fourier Transform must be understood, which is that any complex wave can ultimately be decomposed into a sum of sinusoids. This transform is described by the equation $x(t) = \int_{-\infty}^{\infty} X(f)e^{i2\pi ft}df$, but will not be directly used for the digital synthesis of sound. As described above, pitch names `A-G` are interpreted by instruments which use a collection of partials to create harmony and timbre. These partials help create new waveforms that stem from the fundamental frequency provided to the instrument which are superimposed to create a composite waveform. After `InstrumentSynthesizer` performs further processing, each track is merged together and the quantized samples of the composite sinusoids are superimposed. This is so that sound data from all tracks is elogantly overlayed at the proper time when writing the samples to the binary `.wav` file.

<div align="center">
  <img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/47f50ef5-e028-46fb-8087-53605d443dfc" />
  <br>
  <em>A superposition of two waves forming a resulting waveform.</em>
</div>
<br>

Third, it is important to understand the rules of sampling. The Nyquist–Shannon sampling theorem states that a continuous signal can be converted into a digital signal if the sample rate is at least double the highest frequency of the sinusoid. Also, an analog waveform can be reconstructed from a digital signal that has been sampled as such. The formula for this theorem is $f_s > 2f_{max}$ where $f_s$ is the sampling rate frequency and $f$ is the highest frequency in a the composite sinusoid being sampled from. Human hearing receives upper frequencies of around 20,000Hz. This implies that the sampling rate must equal 40,000Hz by applying the formula. In practice, `InstrumentSynthesizer` uses a default sampling rate of 40,100Hz to account for some error in the `SoundGenerator` class. This is the first and most crucial step of the ADC (Analog-to-Digital) conversion process.

<div align="center">
  <img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/78de66dd-e36b-4cf0-a6af-233af9489ae8" />
  <br>
  <em>The Nyquist-Shannon sampling theorem visualized.</em>
</div>
<br>

> [!Caution]
> If the samples for chords are not post-processed with an envelope, then a "popping" sound will occur between notes. This is because of the quick switching behavior of the amplitudes of different chords. Natural instruments do not suffer this sound because there is a mechanical change in vibration that exists due to physical law. In order to compensate for this in the digital world, the boundaries of chords must be softened. This softening can be applied with an envelope, in which the samples at the beginning and end of every chord are shrunk to gradually increase or dampen the amplitude.

<div align="center">
  <img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/a8ca1b14-2976-4c6b-b1ec-a8610e0f86fd" />
  <br>
  <em>Popping behavior and envelope application to sinusoids.</em>
</div>
<br>

Fourth, the sampled values must be quantized. Quantization involves subjecting each sample to a discrete amplitude level. The number of levels is defined by the `bit_depth` of the audio. Four depths are supported by `InstrumentSynthesizer`, which are 8-bit, 16-bit, 24-bit, and 32-bit. A greater `bit_depth` produces a smoother and more granular sound while a lower level sounds more grainy and less articulate. Since samples from a sinusoid are normalized within the continuous range of $[0.0, 1.0]$, multiplication by the maximum integer can be applied to this range to span a new range with greater processable granularity.

<div align="center">

<table>
  <thead>
    <tr>
      <th>Integer Type</th>
      <th>Number of Possible Values</th>
      <th>Minimum</th>
      <th>Maximum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>8-bit</td>
      <td>2<sup>8</sup></td>
      <td>0</td>
      <td>255</td>
    </tr>
    <tr>
      <td>16-bit</td>
      <td>2<sup>16</sup></td>
      <td>0</td>
      <td>65,535</td>
    </tr>
    <tr>
      <td>24-bit</td>
      <td>2<sup>24</sup></td>
      <td>0</td>
      <td>16,777,215</td>
    </tr>
    <tr>
      <td>32-bit</td>
      <td>2<sup>32</sup></td>
      <td>0</td>
      <td>4,294,967,295</td>
    </tr>
  </tbody>
</table>

</div>

Fifth, the samples from each track must be superimposed by summing integer arrays, then each element must be re-normalized to be between zero and the maximum value. This adds further complexity by summing already composite waveforms, but is critical to be able to write the data for all instruments to the `.wav` file in a single stream. Tracks must be superimposed at the sample level rather than at the `Chord` object level because chord durations may not be equivalent, leading to disalignment.

<div align="center">
  <img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/861ac172-d7de-45b2-99d6-e997e3583d4f" />
  <br>
  <em>Superposition and re-normalization of audio sample arrays.</em>
</div>
<br>

Sixth, the final stage of ADC must be applied as quantized samples must be encoded into binary values that can be written to a `.wav` file. At this stage of the processing pipeline, each sample integer now contains the information of all instruments at a given time step. These samples can be written in binary to the audio file which can be played back by a computer. Modern computers have a `audio codec chip` on the motherboard with a built-in DAC to play the audio.

<div align="center">
  <img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/c6e2c24e-98b1-4116-aab7-ab5ff0f22357" />
  <br>
  <em>Superposition and re-normalization of audio sample arrays.</em>
</div>
<br>

---
This project is licensed under the MIT License. See the LICENSE file for details.
