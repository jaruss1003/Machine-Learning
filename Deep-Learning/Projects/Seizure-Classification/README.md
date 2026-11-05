# EEG Seizure Classification

Four-class classification of 16-channel EEG recordings with PyTorch MLPs, developed as a systematic study of architecture and hyperparameter choices.

**Status:** Completed — Deep Learning course project (MTH5320)
**Dataset:** Bangalore EEG Epilepsy Dataset (BEED), UCI Machine Learning Repository
**Framework:** PyTorch

## Overview

- **Data:** 8,000 recordings from 80 patients, 16 numerical EEG channels, balanced across four classes (2,000 each): Healthy, Generalized, Focal, Seizure Event.
- **Patient reconstruction:** the dataset does not ship with patient IDs; they are recovered from its structure (every 100 consecutive recordings belong to one patient).
- **Splits:** patient-level stratified 70/15/15 train/validation/test — no patient appears in more than one split, so the test score cannot leak through patient identity.
- **Preprocessing:** channel-wise z-score standardization, fit on the training set only.

## Method

- **Model:** fully connected MLP (16 → 128 → 4), LeakyReLU activations, AdamW optimizer, cross-entropy loss, early stopping with best-checkpoint selection by validation loss.
- **Experiments:** controlled sweeps over network depth (1–3 hidden layers), learning rate, dropout, and weight decay, changing one factor at a time.

## Key Findings

- **Final model** (single hidden layer): held-out test accuracy **81.33%**, macro F1 **0.8045**.
- **Simpler beat deeper.** One hidden layer outperformed two and three on validation loss (0.457 vs. 0.489 and 0.627).
- **Best regularization:** dropout 0.1 with weight decay 0.01 (validation loss 0.432, the study's best).
- **Performance is uneven by class.** Healthy recordings are classified almost perfectly (F1 0.99), while Seizure Event is the hardest class (recall 0.53), most often confused with Generalized and Focal.
- **Next step:** the model sees per-recording channel features, not raw time series — temporal architectures (1D-CNN, LSTM) are the natural follow-up.

## Files

| File | Contents |
| --- | --- |
| `seizure_model_development.ipynb` | Full development notebook: data pipeline, experiments, evaluation |
| `BEED_Data.csv` | Dataset as used |
| `global_best_model.pt` | Trained final model checkpoint |
| `processed_test_data.pt` | Processed held-out test tensors |

*Educational project on a public benchmark dataset — a learning build, not a clinical tool.*
