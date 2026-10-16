# Genetic Ancestry Analysis for Acral Melanoma Study - Figures

## Overview
This analysis pipeline estimates the genetic ancestry of the acral melanoma cohort by merging germline genotypes with the 1000 Genomes Project reference panel. It produces the Principal Component Analysis (PCA) and ADMIXTURE plots, and the per-sample ancestry proportions table.

## Analysis Scripts

#### `scripts/plink.md`
- **Purpose**: Merge cohort genotypes with 1000 Genomes and prepare data for PCA and admixture

#### `scripts/admixture.md`
- **Purpose**: Estimate ancestry proportions

#### `scripts/create_plots.py`
- **Purpose**: Generate figures and the supplementary table
  - ADMIXTURE stacked barplots for the cohort and each 1000 Genomes superpopulation (Fig. 1E) → `admixture.pdf`
  - PCA plot of PC1 vs PC2 with % variance explained (Fig. 1D) → `pca/pca_plot.pdf`
  - Per-sample ancestry proportions (Supplementary Table 12) → `data/admixture_table.csv`

## Setup & Reproducibility

### Software
- [PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) (available as `plink`)
- [ADMIXTURE](https://dalexander.github.io/admixture/download.html) (available as `admixture`)
- Python 3 with `pandas` and `matplotlib`

```bash
pip install pandas matplotlib
```

### Running the pipeline
All steps should be run from the root of the repository:

1. Place the source PLINK files (`data/genotype_samples.*` and `data/1000g.*`) in `data/`
2. Follow the steps in [`scripts/plink.md`](scripts/plink.md)
3. Follow the steps in [`scripts/admixture.md`](scripts/admixture.md)
4. Generate the figures and table:
   ```bash
   python scripts/create_plots.py
   ```

## Repository Structure
```
├── data/
│   ├── 1000g.{bed,bim,fam}                 # BED-files for 1000 Genomes data
│   ├── genotype_samples.{bed,bim,fam}      # BED-files for 1000 Genomes data
│   ├── genotype_1000g_geno_mind.fam        # Sample IDs after QC (input to ADMIXTURE)
│   ├── igsr_samples.tsv                    # 1000 Genomes sample metadata (superpopulation labels)
├── admixture/
│   └── genotype_1000g_geno_mind.5.Q        # ADMIXTURE output, K = 5
│   └── admixture.pdf                       # Output: Fig. 1E
│   └── admixture_table.csv                 # Output: ancestry proportions (Supplementary Table 12)
├── pca/
│   ├── genotype_1000g_nopal_prune.eigenval # Output of PLINK PCA process
│   ├── genotype_1000g_nopal_prune.eigenvec # Output of PLINK PCA process
│   └── pca_plot.pdf                        # Output: Fig. 1D
├── scripts/
│   ├── plink.md
│   ├── admixture.md
│   └── create_plots.py
```

## Data Sources

1. **1000 Genomes Project**:
Reference genotypes and sample metadata (`igsr_samples.tsv`) from the [International Genome Sample Resource (IGSR)](https://www.internationalgenome.org/).

2. **Cohort genotypes**:
Germline genotypes of the acral melanoma cohort.
