# Genetic Ancestry Analysis for Acral Melanoma Study

## Overview

This analysis pipeline estimates the genetic ancestry of the acral melanoma cohort by merging germline genotypes with the 1000 Genomes Project reference panel. The principal components and the ancestral populations are computed using only the 1000 Genomes samples, and the cohort samples are projected onto them. It produces the Principal Component Analysis (PCA) and ADMIXTURE plots, and the per-sample ancestry proportions table, using the cohort blood samples.

## Analysis Scripts

#### `scripts/plink.md`
- **Purpose**: Merge cohort genotypes with 1000 Genomes and prepare data for PCA and admixture

#### `scripts/admixture.md`
- **Purpose**: Estimate ancestry proportions (K = 5)

#### `scripts/create_plots.py`
- **Purpose**: Generate figures and the Supplementary table 12 (SNP array tab)
  - ADMIXTURE stacked barplots for the cohort and each 1000 Genomes superpopulation (Fig. 1E) (`admixture/admixture.pdf`)
  - PCA plot of PC1 vs PC2 with % variance explained (Fig. S1D) (`pca/pca_plot.pdf`)
  - Per-sample ancestry proportions of the cohort and mean ancestry proportions of each 1000 Genomes superpopulation (Supplementary table 12) (`admixture/admixture_table.csv` and `admixture/admixture_superpop_table.csv`)

## Setup & Reproducibility

### Software

- [PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) (available as `plink`)
- [ADMIXTURE](https://dalexander.github.io/admixture/download.html) (available as `admixture`)
- [uv](https://docs.astral.sh/uv/), which installs Python and the exact package versions in `uv.lock`

### Running the pipeline

All steps should be run from the root of the repository. The intermediate results that make it possible to run the plot creation are included in the repository (`data/1000g_panel.tsv`, `admixture/genotype_1000g_nopal_prune.5.Q`, `pca/genotype_1000g_nopal_prune.eigenvec`, `pca/genotype_1000g_nopal_prune.eigenval`, `data/genotype_samples_metadata.csv`), but if the user wishes to run the complete pipeline using the genotype data, the instructions are as follows:

1. Place the source PLINK files (`data/genotype_samples_2024.*`, `data/genotype_samples_2026.*` and `data/1000g.*`) in `data/`
2. Follow the steps in [`scripts/plink.md`](scripts/plink.md)
3. Follow the steps in [`scripts/admixture.md`](scripts/admixture.md)
4. Generate the figures and table:
   ```bash
   uv run scripts/create_plots.py
   ```

## Repository Structure
```
├── data/
│   ├── 1000g.{bed,bim,fam}                 # BED-files for 1000 Genomes data
│   ├── genotype_samples_2024.{bed,bim,fam} # BED-files for the cohort genotypes (2024 batch)
│   ├── genotype_samples_2026.{ped,map}     # PED/MAP-files for the cohort genotypes (2026 batch)
│   ├── genotype_1000g_nopal_prune.fam      # Sample IDs after QC (input to ADMIXTURE)
│   ├── 1000g_panel.tsv                     # 1000 Genomes sample metadata (superpopulation labels)
│   ├── genotype_samples_metadata.csv       # Cohort sample metadata (sample type and excluded samples)
├── admixture/
│   ├── genotype_1000g_nopal_prune.5.Q      # ADMIXTURE output, K = 5
│   ├── admixture.pdf                       # Output: Fig. 1E
│   ├── admixture_table.csv                 # Output: cohort ancestry proportions (Supplementary table 12)
│   └── admixture_superpop_table.csv        # Output: 1000 Genomes mean ancestry proportions (Supplementary table 12)
├── pca/
│   ├── genotype_1000g_nopal_prune.eigenval # Output of PLINK PCA process
│   ├── genotype_1000g_nopal_prune.eigenvec # Output of PLINK PCA process
│   └── pca_plot.pdf                        # Output: Fig. S1D
├── scripts/
│   ├── plink.md
│   ├── admixture.md
│   └── create_plots.py
├── pyproject.toml                          # Python dependencies
└── uv.lock                                 # Exact versions of the Python dependencies
```

## Data Sources

1. **1000 Genomes Project**:
Reference genotypes from the [International Genome Sample Resource (IGSR)](https://www.internationalgenome.org/), and sample metadata (`1000g_panel.tsv`) from the [phase 3 release](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel).

2. **Cohort genotypes**:
Germline genotypes of the acral melanoma cohort, genotyped in two batches (2024 and 2026).
