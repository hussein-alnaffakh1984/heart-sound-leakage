# Cross-Database Evaluation Reveals Performance Inflation in Heart Sound Classification

This repository contains the code, evaluation splits, and result files for the paper:

> **Cross-Database Evaluation Reveals Performance Inflation in Heart Sound Classification on PhysioNet/CinC 2016**
> Hussein Ali Hussein Al-Naffakh
> *(Under review)*

## Overview

Automated phonocardiogram (PCG) classification on the PhysioNet/CinC 2016 dataset has reported rapidly rising performance, with several recent studies exceeding 98% accuracy. This work asks whether those gains reflect genuine diagnostic capability or increasingly permissive evaluation protocols.

Using a single lightweight convolutional neural network (~23,600 parameters) held constant across conditions, we isolate the effect of the data-split unit alone:

| Evaluation protocol | Record-level AUC |
|---|---|
| Segment-level (leakage-prone) | 0.978 |
| Record-level (assumed safe) | 0.964 |
| Cross-database / leave-one-database-out (LODO) | **0.515** (near-chance) |

A source-identity probe predicts the originating database from the same features with AUC 0.996, while within-database performance stays high (mean AUC 0.871). Together these show that the model learns the recording source rather than cardiac pathology, and that the cross-database collapse is not due to insufficient model capacity or task difficulty.

## Quick start

```bash
pip install -r requirements.txt
python src/train.py
python src/evaluate.py
```

## Repository structure

```
heart-sound-leakage/
├── README.md                 This file
├── LICENSE                   MIT license
├── requirements.txt          Python dependencies
├── src/                      Source code for preprocessing, training, evaluation, and figure generation
├── splits/                   Fixed train/validation/test split indices used in all experiments
├── results/                  Result CSV files (provided)
└── figures/                  Generated figures (provided)
```

## Data

This study uses two publicly available datasets, which are **not** redistributed here:

- **PhysioNet/CinC 2016** — available from the [PhysioNet Challenge 2016 page](https://physionet.org/content/challenge-2016/) or the Kaggle mirror used in this work (`swapnilpanda/heart-sound-database`).
- **PASCAL Classifying Heart Sounds Challenge** — used for external validation.

Download the raw audio from the original sources and place it where the scripts expect it (see `src/`).

## Results files (`results/`)

| File | Contents |
|---|---|
| `lodo_results.csv` | Leave-one-database-out AUC, F1, balanced accuracy per held-out database |
| `within_database.csv` | Within-database AUC (mean over seeds) per source |
| `source_probe.csv` | Source-identity probe AUC per database |
| `baseline_results.csv` | Classical baselines (Logistic Regression, Linear SVM) under all three protocols |
| `generalization_matrix.csv` | Train-on-one / test-on-another generalization matrix |
| `external_pascal.csv` | Zero-shot performance on the external PASCAL dataset |
| `coral_lodo.csv` | CORAL domain-adaptation results under LODO |
| `mitigation.csv` | Mitigation attempts (per-source standardization, CORAL variants) |
| `silhouette_scores.csv` | Silhouette scores for source clustering analysis |

## Figures (`figures/`)

Generalization matrix, confusion matrices, t-SNE and UMAP embeddings of mel features, and the graphical abstract.

## Reproducibility

All experiments were executed with fixed random seeds. The repository includes:
- preprocessing scripts
- model training code
- evaluation scripts
- exact split indices
- figure-generation scripts

This allows full reproduction of the reported results.

> **Note on split indices:** The `splits/` folder fixes which recordings fall into train/validation/test for each protocol. This is the key to reproducing the reported numbers, since the central finding concerns how the *split unit* (segment vs. record vs. database) changes measured performance.

## Citation

If you use this code or the evaluation protocol, please cite the paper (citation details will be added upon publication).

## License

Released under the MIT License (see `LICENSE`).
