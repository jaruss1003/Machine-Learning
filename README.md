# Machine Learning

My coursework and projects in machine learning and deep learning, with a focus on biomedical AI and computational neuroscience.

## Repository Contents

| Folder | What it holds |
| --- | --- |
| [Deep-Learning/](Deep-Learning) | Deep Learning course work: homework notebooks and the course project. Has its own README with details. |
| [Deep-Learning/Homework/](Deep-Learning/Homework) | HW1 — first neural network implementations. HW2 — autoencoder bottleneck dimensions and reconstruction analysis. |
| [Projects/](Projects) | Independent projects, starting with brain-age estimation below. |

## Projects

### [EEG Seizure Classification](Deep-Learning/Projects/Seizure-Classification) — Completed

Deep Learning course project. A PyTorch MLP classifies 16-channel EEG recordings from the BEED dataset into four classes: Healthy, Generalized, Focal, and Seizure Event. Data is split at the patient level, so no patient appears in more than one of the training, validation, and test sets. Final held-out test accuracy: **81.33%**, macro F1 **0.8045**. The project folder holds the development notebook, the dataset, the trained model, and its own README.

### [Brain-Age Estimation from Structural MRI](Projects/Brain-Age) — In Progress

Predicts brain age from T1-weighted MRI (IXI dataset, 563 subjects) using regional brain volumes as interpretable features. Each region's volume is measured by registering a standard brain atlas to the subject's own scan, and regions are compared as fractions of total intracranial volume, so the model's reasoning can be traced back to anatomy. The feature-extraction pipeline is complete (Notebooks 01–04: data exploration, atlas registration, batch processing with intracranial volume, and a full-cohort run with quality control). Model development and interpretation are next.

## Focus Areas

Machine Learning · Artificial Intelligence · Deep Learning · Biomedical AI · Computational Neuroscience
