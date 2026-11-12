# NeuroContour

Whole-tumor segmentation of glioma MRI with a U-Net, tuned in stages: every
experiment changes exactly one setting, each stage's choice made from the
stage before it — learning rate first, then a baseline, then loss, then
augmentation, then an ablation that removes the skip connections.

**Status:** In progress — Deep Learning course project (MTH 4320); notebook built, experiments not yet run
**Dataset:** BraTS 2020 (Brain Tumor Segmentation challenge), accessed through Kaggle
**Framework:** PyTorch

## Overview

- **Data:** pre-operative glioma MRI from 19 institutions. Each case is one patient: four co-registered volumes (T1, T1ce, T2, FLAIR) at 240×240×155, plus a manual outline approved by neuro-radiologists.
- **Labels:** the outline's three sub-regions (labels 1, 2, 4) collapse into one binary whole-tumor mask — any label above zero is tumor.
- **Subset:** the first 75 of 369 labeled cases; only slices carrying at least 50 tumor pixels are used — **4,724 slices**, measured from the masks themselves.
- **Splits:** patient-level 52 train / 11 validation / 12 test. Adjacent slices of one brain look nearly identical, so slices follow their patient and no patient appears in two splits.
- **Preprocessing:** slices resized to 128×128 (masks with nearest-neighbor, so they stay 0/1) and z-scored by each slice's own mean and standard deviation — nothing is fit across slices, so nothing can leak.

## Key Findings

*So far — from data preparation, before any training:*

- **The dataset is bigger than estimated.** The 75-case subset was expected to yield 2,000–3,000 usable slices; counting the actual masks gives 4,724 (32–90 per case, mean 63.0).
- **The honest baseline scores zero.** A predictor that outputs "no tumor anywhere" earns a Dice of exactly 0.00 — while its pixel accuracy sits near 98%, because a brain slice is mostly not-tumor. That gap is why this project is scored by Dice and never headlines accuracy.
- **The split is provably clean.** Patient counts 52 / 11 / 12, zero overlap, and the per-split slice counts sum back to exactly 4,724.

*Experimental findings — the winning configuration, the staged comparisons, and the final per-patient test Dice — will be added here as the runs complete.*

## The model

- **Architecture:** U-Net — encoder widths 32→256 with a 512-wide bottleneck, mirrored decoder, and skip connections that can be switched off for the ablation. About 7.77M parameters with skips, 6.98M without.
- **Input → output:** one slice as (4, 128, 128) → one outline map (1, 128, 128).
- **Training:** Adam optimizer, batch size 8, fixed seed, early stopping on validation Dice with the best weights kept.
- **Losses on trial:** binary cross-entropy with logits vs. Dice loss.
- **Experiments, in order:** (1) three short learning-rate runs (3×10⁻⁴, 1×10⁻³, 3×10⁻³) on a training subset; (2) the full baseline; (3) Dice loss, one change; (4) left-right flip augmentation, one change; (5) skip connections removed, one change. Failed runs stay in the results table.
- **Metric:** Dice coefficient between predicted and expert outlines, computed per patient and then averaged. The test set is touched exactly once, at the end, with the winning configuration.

## Run it

```bash
./setup.sh   # creates this project's .venv and installs torch, nibabel, numpy, matplotlib
```

Then place the case folders directly in `data/` (so `data/BraTS20_Training_001`
exists — see `data/PUT-DATA-HERE.txt`), open the folder in VS Code, and run
`unet_brats_segmentation.ipynb` top to bottom. Checkpoints in the notebook
verify each stage: 75 cases found, slice index 4,724, split 52/11/12 with no
overlap, honest baseline Dice 0.0.

## Repository contents

| Path | What it is |
|---|---|
| `unet_brats_segmentation.ipynb` | The whole project: data preparation, model, staged experiments, final test evaluation, figures |
| `requirements.txt` | torch, nibabel, numpy, matplotlib |
| `setup.sh` | One-time environment setup — creates `.venv` and installs the requirements |
| `data/` | BraTS case folders (not tracked — too large for GitHub) |
| `<run>_best.pt`, `overlay_figure.png`, `wrong_pixels.png` | Produced by the notebook as it runs: best weights per run, and the two closing figures |

## Limitations

Two-dimensional slices: the model never sees neighboring slices, though tumors
are three-dimensional. The subset is 75 of 369 available cases, chosen for
compute, not at random. One seed and one split — results carry no error bars.
This is a course project on a public research dataset — a learning build, not
a clinical tool.
