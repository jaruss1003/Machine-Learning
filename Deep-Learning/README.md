# 🧠 Deep Learning Coursework & Projects

This directory serves as the central hub for all my homework assignments and project work completed during the Deep Learning course.

## 📁 Repository Structure

### 📝 Homework & Assignments
All homework notebooks are organized in the homework/ directory.

HW1.ipynb - Homework 1: Initial neural network implementations.

(Future HW notebooks will be added here)

### 🚀 Projects
All major course projects are organized in the `projects/` directory.

- **`projects/Seizure-Classification/`** — **EEG Epilepsy Classification (BEED Dataset)**
  - Systematic hyperparameter tuning and model architecture comparison (1, 2, and 3-layer MLPs) using PyTorch.
  - Implemented leak-free patient-stratified validation, early stopping, and automated global checkpointing to track model metadata (learning rate, dropout, weight decay).
  - Selected the optimal 1-layer MLP configuration ($LR = 0.003$, $WD = 0.01$, $Dropout = 0$) and achieved a validation loss of $0.4538$
