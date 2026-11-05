# Machine Learning

Coursework and projects in machine learning and deep learning, with a focus on biomedical AI and computational neuroscience. Work is organized for reproducibility: code, data notes, and documentation live together, and results are reported with their methods.

**Tools:** Python · PyTorch · scikit-learn · NumPy · pandas · nibabel · ANTsPy

## Repository Contents

| Folder | What it holds |
| --- | --- |
| [Deep-Learning/](Deep-Learning) | Deep Learning course work: homework notebooks and the course project. Has its own README with details. |
| [Deep-Learning/Homework/](Deep-Learning/Homework) | HW1 — first neural network implementations. HW2 — autoencoder bottleneck dimensions and reconstruction analysis. |
| [Projects/](Projects) | Independent projects, starting with brain-age estimation below. |

## Projects

### [EEG Seizure Classification](Deep-Learning/Projects/Seizure-Classification) — Completed

A PyTorch MLP classifies 16-channel EEG recordings from the BEED dataset into four classes: Healthy, Generalized, Focal, and Seizure Event. Data is split at the patient level, so no patient appears in more than one of the training, validation, and test sets. Final held-out test accuracy: **81.33%**, macro F1 **0.8045**. Key findings and full method are in the project README.

### [Brain-Age Estimation from Structural MRI](Projects/Brain-Age) — In Progress

Predicts brain age from T1-weighted MRI (IXI dataset, 563 subjects) using regional brain volumes as interpretable features, measured by registering a standard atlas to each subject's scan and expressed as fractions of intracranial volume. The feature-extraction pipeline is complete through the full-cohort run; model development and interpretation are next. Status and method are tracked in the project README.

## Focus Areas

Machine Learning · Artificial Intelligence · Deep Learning · Biomedical AI · Computational Neuroscience
