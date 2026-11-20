# Deep Learning

Coursework for MTH4320 Deep Learning at Florida Institute of Technology — homework notebooks and two course projects, all implemented in PyTorch.

## Homework

| Path | Description |
| --- | — |
| [Homework/HW1.ipynb](Homework/HW1.ipynb) | Homework 1 — first neural network implementations. |
| [Homework/HW2.ipynb](Homework/HW2.ipynb) | Homework 2 — autoencoder bottleneck dimensions and reconstruction analysis. |

## Course Projects

| Path | Description |
| --- | — |
| [Projects/Seizure-Classification/](Projects/Seizure-Classification) | EEG seizure classification with an MLP. |
| [Projects/NeuroContour/](Projects/NeuroContour/) | Whole-tumor segmentation of glioma MRI with a U-Net. |

**[EEG Seizure Classification](Projects/Seizure-Classification)** — a PyTorch MLP that classifies 16-channel EEG recordings (BEED dataset) into Healthy, Generalized, Focal, and Seizure Event, developed through systematic architecture and hyperparameter experiments with leak-free, patient-level data splits. Method, key findings, results, and the trained model are in the project folder.

**[NeuroContour](Projects/NeuroContour)** — a PyTorch U-Net that outlines whole gliomas on brain MRI (BraTS 2020), tuned in stages where every experiment changes exactly one setting: learning rate, then loss, then augmentation, then a skip-connection ablation. Final test Dice 0.8113 across 12 unseen patients, reported per patient. Method, key findings, and results are in the project folder.
