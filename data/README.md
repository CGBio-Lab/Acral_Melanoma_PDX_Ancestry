# data/

The following files are expected here:

### Source data (to run the full pipeline from [`scripts/plink.md`](../scripts/plink.md))
- `genotype_samples_2024.bed`, `genotype_samples_2024.bim`, `genotype_samples_2024.fam`: cohort germline genotypes, 2024 batch (PLINK binary)
- `genotype_samples_2026.ped`, `genotype_samples_2026.map`: cohort genotypes, 2026 batch (PLINK text)
- `1000g.bed`, `1000g.bim`, `1000g.fam`: 1000 Genomes reference genotypes (PLINK binary)
- `genotype_1000g_nopal_prune.bed`, `genotype_1000g_nopal_prune.bim`, `genotype_1000g_nopal_prune.fam`: QC'd and LD-pruned genotypes, input to PCA and ADMIXTURE (produced by `scripts/plink.md`)

### Required to generate the figures (`scripts/create_plots.py`)
- `1000g_panel.tsv`: 1000 Genomes sample metadata (superpopulation labels) from the [phase 3 release](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel)
- `genotype_samples_metadata.csv`: cohort sample metadata: sample type (`blood`, `tumour`, `cell_line`) and samples excluded from the analysis (`exclude_from_analysis` in `notes`). Cohort samples not listed are blood samples
- `genotype_1000g_nopal_prune.fam`: sample IDs after QC, in the order of the ADMIXTURE output (produced by `scripts/plink.md`)
- `pca/genotype_1000g_nopal_prune.eigenvec`, `pca/genotype_1000g_nopal_prune.eigenval`: Principal Component Analysis output
