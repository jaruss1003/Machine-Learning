# NeuroContour

Brain tumor segmentation with a U-Net, tuned in stages — MTH 4320 Project 2.

One notebook is the whole project: it prepares the BraTS 2020 data, trains a
U-Net in stages (learning-rate runs → baseline → loss comparison → flip
augmentation → no-skip ablation), and scores the winner once on untouched
test patients. The notebook does the work; the build guide lives outside
this repo on purpose.

## What's in this folder

| File / folder | What it is |
|---|---|
| `unet_brats_segmentation.ipynb` | The project notebook — the deliverable. All code cells start empty; you write them. |
| `data/` | The case folders live directly in here — see `data/PUT-DATA-HERE.txt`. |
| `requirements.txt` | `torch`, `nibabel`, `numpy`, `matplotlib`. |

The step-by-step build guide (PDF) is deliberately NOT in this repo. Keep
your copy anywhere outside this folder — or drop it in; `.gitignore` already
excludes it by name, so it can't be committed by accident.

Run outputs land in this folder as you work: one `<run_name>_best.pt` weights
file per training run, and the two figures (`overlay_figure.png`,
`wrong_pixels.png`) at the end.

## Setup in VS Code

1. **File → Open Folder…** and open this folder.
2. Create the project's own environment and install the packages — either
   run `./setup.sh` in the VS Code terminal (Terminal → New Terminal), or by
   hand: `python3 -m venv .venv`, then `pip install -r requirements.txt`.
   Either way you get a `.venv` that belongs to this project alone, and the
   folder's settings already point VS Code's Python at it. (Torch is a large
   download; give it a few minutes.)
4. Download the data (Kaggle: "BraTS2020 Dataset (Training + Validation)" by
   Awsaf), open its `MICCAI_BraTS2020_TrainingData` folder, and copy the case
   folders inside it directly into `data/` — so `data/BraTS20_Training_001`
   exists, with no folder in between.
5. Open the notebook. Top right, check the **kernel** says `.venv` — if cells
   can't import torch while the terminal can, the kernel is a different
   Python; switch it, don't reinstall.
6. Run cells 1–2: the device should print `mps` on an Apple-silicon Mac.

## Numbers that prove you're on track

- 75 case folders found, first `BraTS20_Training_001`, last `BraTS20_Training_075`
- Slice index total: **4,724** (slices with ≥ 50 tumor pixels, cases 001–075)
- Split: **52 train / 11 validation / 12 test** patients, no overlaps,
  split slice counts summing back to 4,724
- Honest baseline: Dice exactly **0.0**, accuracy ≈ 0.98
