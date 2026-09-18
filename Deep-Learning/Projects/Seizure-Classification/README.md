# EEG-Based Seizure Classification Using an MLP

A systematic deep learning project evaluating Multi-Layer Perceptron (MLP) architectures for classifying multi-channel continuous Electroencephalogram (EEG) signals into four distinct diagnostic seizure states.

---

## Overview

* **Author:** Jacob Russ

* **Dataset:** Bangalore EEG Epilepsy Dataset (BEED) — UCI Machine Learning Repository

* **Task:** 4-Class Classification

* **Framework:** PyTorch

---

## Research Goals & Objectives

* **Research Question:** Can an MLP effectively classify patient EEG data into four distinct diagnostic states, and how do systematic structural and optimization adjustments impact performance?

* **Model Inputs:** 16 continuous numerical EEG feature channels ($X_1 \dots X_{16}$) capturing brain wave activity.

* **Desired Outputs:** 4-class target variable:
  * `0`: Healthy
  * `1`: Generalized Seizure
  * `2`: Focal Seizure
  * `3`: Seizure Event

---

## Data Engine & Preprocessing Pipeline

* **Dataset Scale:** 8,000 signal instances, 16 continuous features, evenly balanced across all 4 target classes (2,000 samples per class).

* **Patient-Based Partitioning:** Strict 70/15/15 split (Train/Validation/Test) partitioned by patient block reconstruction (200 rows per patient across 80 patients) to prevent cross-validation data leakage.

* **Channel Standardization:** Channel-wise $z$-score standardization ($X_{\text{norm}} = \frac{X - \mu}{\sigma}$) computed strictly on the training set and applied to validation and test splits.

---

## Architecture & Hyperparameter Exploration Space

* **Core Architecture:** Fully-connected MLP using **LeakyReLU** hidden activations ($\alpha = 0.01$) and **Softmax** outputs, trained via `CrossEntropyLoss` with the **AdamW** optimizer.

* **Systematic Decision Chain:**
  1. **Network Depth:** Evaluate 1, 2, and 3 hidden layers (holding learning rate constant at $10^{-3}$).

  2. **Dropout Regularization:** Apply dropout ($p = 0.3$) to the best depth architecture to mitigate neuron co-adaptation and limit memorization. 

  3. **Learning Rate Tuning:** Fine-tune learning rate log-scale ($\eta \in [10^{-4}, 10^{-2}]$) based on loss curve behavior.

---

## Evaluation Metrics

* **Multi-Class Accuracy**
* **Macro F1-Score**
* **Training vs. Validation Loss Curves**
* **4x4 Confusion Matrix**
---