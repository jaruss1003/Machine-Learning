import random
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset


def get_data_loaders(csv_path='BEED_Data.csv', seed=42, batch_size=64):
  """Loads BEED dataset, performs stratified patient-level splitting (70/15/15),

  applies Z-score standardization, and returns PyTorch DataLoaders.
  """
  # Set random seeds for reproducibility
  torch.manual_seed(seed)
  np.random.seed(seed)
  random.seed(seed)

  # 1. Load Data & Assign Patient IDs (100 rows per patient across 80 patients)
  df = pd.read_csv(csv_path)
  df['Patient_ID'] = df.index // 100 + 1
  target_column = 'y'

  # 2. Patient-Level Stratified Partitioning (56 Train / 12 Val / 12 Test)
  patient_df = df.groupby('Patient_ID')[target_column].first().reset_index()

  train_val_patients, test_patients = train_test_split(
      patient_df, test_size=12, random_state=seed, stratify=patient_df['y']
  )
  train_patients, val_patients = train_test_split(
      train_val_patients,
      test_size=12,
      random_state=seed,
      stratify=train_val_patients['y'],
  )

  # Map patients back to full record rows
  train_df = df[df['Patient_ID'].isin(train_patients['Patient_ID'])].reset_index(
      drop=True
  )
  val_df = df[df['Patient_ID'].isin(val_patients['Patient_ID'])].reset_index(
      drop=True
  )
  test_df = df[df['Patient_ID'].isin(test_patients['Patient_ID'])].reset_index(
      drop=True
  )

  # 3. Z-Score Standardization across 16 EEG channels
  X_cols = [c for c in df.columns if c not in ['Patient_ID', target_column]]

  scaler = StandardScaler()
  X_train = scaler.fit_transform(train_df[X_cols])
  X_val = scaler.transform(val_df[X_cols])
  X_test = scaler.transform(test_df[X_cols])

  y_train = train_df[target_column].values
  y_val = val_df[target_column].values
  y_test = test_df[target_column].values

  # 4. Wrap into TensorDatasets & DataLoaders
  train_loader = DataLoader(
      TensorDataset(
          torch.tensor(X_train, dtype=torch.float32),
          torch.tensor(y_train, dtype=torch.long),
      ),
      batch_size=batch_size,
      shuffle=True,
  )
  val_loader = DataLoader(
      TensorDataset(
          torch.tensor(X_val, dtype=torch.float32),
          torch.tensor(y_val, dtype=torch.long),
      ),
      batch_size=batch_size,
      shuffle=False,
  )
  test_loader = DataLoader(
      TensorDataset(
          torch.tensor(X_test, dtype=torch.float32),
          torch.tensor(y_test, dtype=torch.long),
      ),
      batch_size=batch_size,
      shuffle=False,
  )

  return train_loader, val_loader, test_loader
