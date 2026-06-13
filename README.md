# EncoreGuard 🎼

> Stop playlist fatigue before the skip button does.

EncoreGuard finds the optimal artist repetition threshold in a playlist
using precision–recall trade-off analysis. Built as a learning project
exploring how recommendation systems balance coverage vs accuracy.

## What it does
- Simulates a realistic music listening history
- Labels "fatigue moments" using a sliding window
- Sweeps detection thresholds and measures Precision, Recall, F1
- Visualizes the trade-off curve interactively

- SOON WILL SUPPORT REAL DATA

## Concepts I learned
- Sliding window algorithms
- Precision vs Recall (the core ML evaluation trade-off)
- F1 score as a balance metric
- Ground truth labeling

## Stack
Python 3.11+ · no ML libraries required · pure logic

## Run it
pip install -r requirements.txt
python src/data_generator.py
python src/fatigue_detector.py
python src/evaluator.py
