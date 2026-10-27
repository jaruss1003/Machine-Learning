# Interpretable Brain-Age Estimation from Structural MRI

> **Status: In Progress.** The MRI pipeline (registration → regional
> volumes → head-size normalisation) works and is validated on a pilot
> batch. **No age-prediction model has been trained yet**, so there are
> no prediction, gap, or visualisation results to report. Anything
> below marked *planned* is intended method, not completed work.

Predict a person's age from a T1-weighted MRI scan — their **brain
age** — then go one step further than most brain-age work: show
*which regions* make that brain look older or younger than it is,
as deviations from what is typical for that age, rendered on a 3D
brain with a "this brain vs typical brain" toggle.

Example of the intended output: a 50-year-old whose brain is
predicted at 57 has a **brain-age gap of +7 years** — their brain
*looks* older than typical. What that does and doesn't mean is
covered under [The obvious questions](#the-obvious-questions).

| | |
|---|---|
| Data | IXI — 581 T1 scans, 563 subjects with usable ages (20–86) |
| Features | Volumes of 48 Harvard–Oxford cortical regions, as fractions of intracranial volume |
| Model (*planned*) | Ridge regression — simple and interpretable first |
| Outputs (*planned*) | Predicted age, brain-age gap, per-region deviation (z-scores), 3D deviation map |
| Phase 2 (*planned*) | Longitudinal follow-up on OASIS — rate of aging over time |

---

## Status

| Stage | State |
|---|---|
| Cohort construction + exploration (Notebook 01) | ✅ Done |
| Registration + first regional volumes (Notebook 02) | ✅ Done |
| ICV normalisation + batch function (Notebook 03) | ✅ Done — pilot batch of 8 |
| Full-cohort batch run | Next |
| Baseline model + age-bias correction (Notebook 04) | Planned |
| Per-region age norms + deviation maps | Planned |
| Real-data 3D visualisation | Planned — existing prototype uses simulated data only |
| Phase 2: longitudinal OASIS | Not started |

---

## Data

- **IXI dataset** (Biomedical Image Analysis Group, Imperial College
  London): MRI of ~600 healthy adults from three London hospitals.
  This project uses the **T1 scans and ages only**.
  https://brain-development.org/ixi-dataset/ — open download,
  CC BY-SA 3.0.
- Subjects are healthy volunteers — "subjects", not patients.
- **No MRI data is in this repo.** Scans exceed GitHub's 100 MB
  per-file limit (~4.5 GB total); download IXI from the source above
  and anyone reproduces from identical data.
- The cohort roster (`subjects.csv`: `subject, age, file`) is built
  by `make_subjects.py` from `IXI.xls` + the T1 filenames.

---

## Pipeline

Steps 1–7 are implemented; 8–10 are planned.

1. **Cohort.** `make_subjects.py` maps each T1 file to its subject's
   age from `IXI.xls`.
2. **Explore.** Age distribution and 3-plane slice views (nibabel,
   matplotlib). Orientation is always read from the scan's own affine
   (`aff2axcodes`) — IXI scans here are `('P', 'S', 'R')`, never assumed.
3. **Register.** Affine registration to the MNI152 template (ANTsPy).
   Affine is deliberate: it aligns the head while preserving the
   subject's own regional size differences — the signal being measured.
4. **Measure regions.** Inverse-warp the Harvard–Oxford cortical
   atlas (48 regions) into subject space (`invtransforms`,
   `genericLabel` interpolation) and count voxels per region × voxel
   volume → mL.
5. **Measure head size (ICV).** Warp the MNI152 brain mask into
   subject space with the *same* registration and count its voxels.
   The shortcut of estimating ICV from the affine determinant was
   tested and **rejected** — ANTsPy affines aren't run-to-run
   deterministic, and it gave implausible ICVs (≈800–911 mL, vs
   1,327 mL by mask propagation for IXI002).
6. **Normalise.** Use `fraction = region mL / ICV mL`, with region and
   ICV always from the same registration run. All comparisons and all
   future model features use fractions, never raw mL (see Caveats).
7. **Batch.** Steps 3–6 wrapped in `process_subject(path)`. Pilot:
   8 age-spread subjects → `regional_volumes_batch.csv`. QC: ICVs
   outside the plausible range flag a suspect registration.
8. **Model** *(planned).* Ridge regression from the 48 fractions to
   chronological age, participant-level train/test split, reported
   as MAE on held-out subjects. An **age-bias correction** (models
   over-predict the young and under-predict the old) is fitted on
   training data only, then applied to test predictions.
9. **Interpret** *(planned).* Brain-age gap per subject, plus a
   per-region z-score against age norms (next section).
10. **Visualise** *(planned).* The z-scores coloured onto the atlas
    in 3D, with the this-brain / typical-brain toggle.

**Rules throughout:** participant-level splits; corrections and
norms fitted on training data only; baselines before anything
complex; failures flagged, not silently dropped; no clinical claims.

---

## The obvious questions

**Where does the "typical brain" at a given age come from?**
Nowhere external — it's built from this cohort. For each region, fit
the expected fraction as a function of age across the reference
(training) subjects: that fit, plus the spread of residuals around
it, defines what's typical at any age. A subject's z-score is
`(observed − expected at their age) / residual spread`. The "typical
brain" in the visualisation is that same fit rendered — every region
at its expected value (z = 0), on the same atlas geometry; the toggle
changes colours only. It is not a downloaded scan, not one "typical
person", and not the MNI152 template (an average of mostly young
adults — used here only as a spatial reference). Published brain
charts aren't interchangeable: different features, different
parcellation. This is also why norms need the full cohort — 8 pilot
subjects can't define "typical" at any age.

**How do we tell if a brain is aging rapidly?**
In Phase 1, we don't — and the wording matters. One scan gives a
*gap*, not a *rate*: +7 means "looks 7 years older than typical",
which could be a lifelong difference. Nothing about speed can be
inferred from a single time point, so Phase 1 language is
"older-appearing / younger-appearing", never "aging fast".
A rate requires repeat scans — that's Phase 2 (OASIS): compute the
gap at each visit with the same pipeline, then the **slope of gap
over time** (e.g. brain age advancing 1.5 years per chronological
year) is the aging rate, compared against the cohort's distribution
of slopes, and only trusted where it exceeds our measurement noise.

**How big does a gap have to be to mean anything?**
Bigger than the model's error. A gap is judged against the held-out
MAE and expressed as a percentile / z-score within the healthy
cohort's own gap distribution — descriptive bands, not a diagnostic
cutoff. It also has to look real regionally: a broad, consistent
pattern across age-sensitive regions is evidence; a gap driven by
one odd region on a QC-flagged registration is a processing problem.

**Why fractions instead of actual volumes?**
Because raw volumes aren't stable enough to compare. The same
subject re-registered gave raw region volumes ~19% apart, while
same-run fractions agreed to 4 significant figures (IXI002 Frontal
Pole: 0.0656 in both runs). Fractions cancel the registration's
scale wobble and the subject's head size in one step.

**Why such a simple model?**
Ridge regression's coefficients are directly readable — which
regions push the prediction up or down is the point of the project.
A fancier model is only justified after this baseline exists and
its error is known.

**Can this diagnose anything?**
No. This is a research prototype on a healthy cohort. It makes no
clinical claims, and a brain-age gap by itself is not a diagnosis
of anything.

---

## Results so far

Pipeline validation only — no model results exist yet.

- **Normalisation works at pilot scale:** total cortical fraction
  was 0.551–0.561 across all 8 pilot subjects, despite differing
  ages and head sizes.
- **Fractions are the stable unit** (see above): raw mL wobbles
  ~19% between runs, fractions don't.
- **QC catches bad registrations:** 3 of 8 pilot subjects were
  flagged by ICV — IXI191 (973 mL) and IXI495 (944 mL) too low,
  IXI326 (1,865 mL) too high.

## Caveats

- **Two registration scale families:** affine fits on un-stripped
  heads settle ~19% apart (IXI002 ICV: 1,327 vs 1,118 mL across
  runs). Internally consistent each time, not comparable across
  runs in raw mL — hence the same-run, fractions-only rule.
- **Pilot thresholds are provisional.** The suspect-ICV band comes
  from n=8; ICVs in the 1,100s are the small-scale family, not
  failures. Thresholds get revisited after the full-cohort run.
- **Notebook 02's IXI002 table is superseded** (an under-scaled fit).
  Cite Notebook 03's numbers (Frontal Pole 87.07 mL, fraction 0.0656).
- **Age only, for now.** Norms and the model use age; sex is in
  `IXI.xls` but not yet modelled — a known simplification.
- **Coarse features.** 48 atlas regions capture regional volume
  only — no cortical thickness, white matter, or fine anatomy —
  and results depend on the atlas and registration choices above.

---

## Reproducing this work

```bash
# 1. Download IXI (link above) into:
#    data/IXI-T1/*.nii.gz   and   data/IXI.xls
#    (data/ is gitignored, along with venv/ and caches)

# 2. Environment — installs go in the terminal, not in notebooks
python -m venv venv
source venv/bin/activate
pip install nibabel numpy pandas matplotlib jupyter antspyx nilearn scikit-learn xlrd
python -m ipykernel install --user --name brain-age --display-name "brain-age"

# 3. Build the cohort, then run the notebooks in order
python make_subjects.py
# 01_explore.ipynb → 02_registration.ipynb → 03_batch_and_icv.ipynb
```

```text
Projects/Brain-Age/
├── README.md                  # this file
├── 01_explore.ipynb           # cohort exploration + slice viewer
├── 02_registration.ipynb      # registration + first regional volumes
├── 03_batch_and_icv.ipynb     # ICV normalisation + batch processing
├── make_subjects.py           # builds subjects.csv
├── subjects.csv               # cohort roster (subject, age, file)
├── regional_volumes_batch.csv # pilot batch output (8 subjects)
├── slice.png                  # example slice view (Notebook 01)
└── .gitignore                 # data/ venv/ __pycache__/ .ipynb_checkpoints/
```

## Roadmap

- [x] Cohort roster + exploration
- [x] Registration + regional volumes for a first subject
- [x] ICV normalisation + 8-subject pilot batch
- [ ] Full-cohort batch run, with ICV quality control
- [ ] Baseline ridge model (Notebook 04) + age-bias correction
- [ ] Brain-age gap + per-region deviation from age norms
- [ ] Real-data 3D visualisation (this-brain vs typical-brain)
- [ ] Phase 2 — longitudinal rate of aging on OASIS

Parked, not planned: disease stratification, cross-dataset
generalisation, a clinical-style report mockup.

---

> IXI Dataset, Biomedical Image Analysis Group, Imperial College
> London. https://brain-development.org/ixi-dataset/ — © the IXI
> contributors, CC BY-SA 3.0. No MRI data is redistributed here.
