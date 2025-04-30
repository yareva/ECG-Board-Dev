# 🛠️ ECG Board Assembly Notes

## Overview

This board was assembled as part of a hands-on project to understand analog signal processing and bio-sensing using an ECG (Electrocardiogram) amplifier circuit. While I’m a Software Engineering student, this project allowed me to explore circuit soldering and low-level signal capture.

## Assembly Summary

- Followed the official schematic and instruction packet (included in this repo).
- Soldered all components manually, including resistors, capacitors, ICs, and headers.
- Verified correct placement of polarized components (diodes, LEDs, and electrolytic capacitors).
- Fixed PCB labeling issues noted in the instructions (duplicate R17 → R18).
- Used flux and fine-tip soldering for small components to prevent bridges.

## Testing Results

- Power was supplied using a 9V battery as outlined in the guide.
- The LED heartbeat indicator and buzzer worked after calming down and attaching electrodes.
- Signal verified with an oscilloscope — waveform showed expected ECG pattern with visible heartbeat pulses.
- Noise reduced significantly by the 60Hz notch filter.

## Next Steps

- Connect the output to a Raspberry Pi using an MCP3008 ADC.
- Begin capturing and plotting ECG signals digitally.
- Expand this into a live patient dashboard with optional AI-based trend detection.
