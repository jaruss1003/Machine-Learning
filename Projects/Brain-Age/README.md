# Interpretable Brain-Age Estimation from Structural MRI

Predict a person's age from a T1-weighted MRI scan — their **brain age** — then show *which regions* make that brain look older or younger than typical for its age, as deviations from age norms. A 50-year-old predicted at 57 has a brain-age gap of +7: their brain *looks* older than typical. (A gap is not a rate, and not a diagnosis — see Limitations.)

> **Status: In Progress.** The feature-extraction pipeline is complete and validated on the full cohort. **No age-prediction model has been trained yet**, so no prediction or gap results are claimed. Anything marked *planned* is intended method, not completed work.

| | |
| --- | --- |
| Data | IXI dataset — 581 T1 scans; 563 subjects with usable ages |
| Features | Volumes of 48 Harvard–Oxford cortical regions, as fractions of intracranial volume (ICV) |
| Model (*planned*) | Ridge regression — simple and interpretable first |
| Outputs (*planned*) | Predicted age, brain-age gap, per-region deviation (z-scores vs. age norms), 3D deviation map |
| Tools | Python · nibabel · ANTsPy · nilearn · pandas · scikit-learn (*planned*) |

## Status

| Stage | State |
| --- | --- |
| Cohort construction + exploration (Notebook 01) | Done |
| Registration + first regional volumes (Notebook 02) | Done |
| ICV normalisation + batch function (Notebook 03) | Done |
| Full-cohort run, 563 subjects (Notebook 04) | Done |
| Quality control + modeling dataset (Notebook 05) | Next |
| Baseline model + age-bias correction | Planned |
| Per-region age norms + deviation maps | Planned |
| Real-data 3D visualisation | Planned (existing prototype uses simulated data only) |
| Phase 2: longitudinal aging rate on OASIS | Planned |

## Method

1. **Cohort.** `make_subjects.py` maps each T1 file to its subject's age from `IXI.xls`, producing `subjects.csv`.
2. **Register.** Affine registration to the MNI152 template (ANTsPy). Affine is deliberate: it aligns the head while preserving the subject's own regional size differences — the signal being measured.
3. **Measure regions.** Inverse-warp the Harvard–Oxford cortical atlas (48 regions) into subject space and count voxels per region × voxel volume.
4. **Measure head size (ICV).** Warp the MNI152 brain mask into subject space with the *same* registration and count its voxels. (Estimating ICV from the affine determinant was tested and **rejected** — it gave implausible values.)
5. **Normalise.** Features are `fraction = region volume / ICV`, with region and ICV always from the same registration run. Raw volumes are never compared across runs.
6. **Model** *(planned).* Ridge regression from the 48 fractions to age, participant-level train/test split, age-bias correction fitted on training data only.

**Rules throughout:** participant-level splits; norms and corrections fitted on training data only; baselines before anything complex; failures flagged, not silently dropped; no clinical claims.

## Findings So Far

Pipeline validation only — no model results exist yet.

- **Fractions are the stable unit.** The same subject re-registered gives raw region volumes ~19% apart, while same-run fractions agree to 4 significant figures.
- **Total cortical fraction is consistent** across the full cohort (≈ 0.555 of ICV) and roughly age-invariant, which is why the model will use the 48 regional fractions rather than the total.
- **Registration failures are detectable.** A small number of subjects show collapsed ICV or outlying total fraction; the quality-control rule for the modeling dataset excludes subjects whose total fraction falls outside median ± 5×IQR, or whose ICV is under 300 mL (mask-warp collapse).

## Data

- IXI (Biomedical Image Analysis Group, Imperial College London): MRI of ~600 healthy adults from three London hospitals. This project uses the T1 scans and ages only. https://brain-development.org/ixi-dataset/ — open download, CC BY-SA 3.0.
- Subjects are healthy volunteers — "subjects", not patients.
- **No MRI data is in this repo** (scans total ~4.5 GB). Download IXI from the source above; the cohort roster and all code needed to reproduce the features are here.

## Reproducing This Work

```bash
# 1. Download IXI into data/IXI-T1/*.nii.gz plus data/IXI.xls (data/ is gitignored)

# 2. Environment — installs go in the terminal, not in notebooks
python -m venv venv
source venv/bin/activate
pip install nibabel numpy pandas matplotlib jupyter antspyx nilearn scikit-learn xlrd
python -m ipykernel install --user --name brain-age --display-name "brain-age"

# 3. Build the cohort, then run the notebooks in order
python make_subjects.py
# 01_explore.ipynb → 02_registration.ipynb → 03_batch_and_icv.ipynb → 04_full_cohort.ipynb
```

```text
Projects/Brain-Age/
├── README.md                    # this file
├── 01_explore.ipynb             # cohort exploration + slice viewer
├── 02_registration.ipynb        # registration + first regional volumes
├── 03_batch_and_icv.ipynb       # ICV normalisation + batch processing
├── 04_full_cohort.ipynb         # full-cohort run (563 subjects)
├── make_subjects.py             # builds subjects.csv
├── subjects.csv                 # cohort roster (subject, age, file)
├── regional_volumes_batch.csv   # pilot batch output (8 subjects)
├── regional_volumes_all.csv     # full-cohort features
├── slice.png                    # example slice view (Notebook 01)
└── .gitignore                   # data/ venv/ __pycache__/ .ipynb_checkpoints/
```

## Limitations

- **A gap is not a rate.** One scan shows how old a brain *looks*, not how fast it is aging; rates require repeat scans (Phase 2).
- **Coarse features.** 48 atlas regions capture regional volume only — no cortical thickness, white matter, or fine anatomy — and results depend on the atlas and registration choices.
- **Age only, for now.** Sex is available in `IXI.xls` but not yet modelled — a known simplification.
- **Not a diagnostic tool.** Research prototype on a healthy cohort; a brain-age gap by itself diagnoses nothing.

## Roadmap

- [x] Cohort roster + exploration
- [x] Registration + regional volumes
- [x] ICV normalisation + pilot batch
- [x] Full-cohort run with quality control
- [ ] Modeling dataset (QC applied) + baseline ridge model
- [ ] Age-bias correction
- [ ] Brain-age gap + per-region deviation from age norms
- [ ] Real-data 3D visualisation (this brain vs. typical brain)
- [ ] Phase 2 — longitudinal rate of aging on OASIS

---

*IXI Dataset, Biomedical Image Analysis Group, Imperial College London. https://brain-development.org/ixi-dataset/ — © the IXI contributors, CC BY-SA 3.0. No MRI data is redistributed here.*
