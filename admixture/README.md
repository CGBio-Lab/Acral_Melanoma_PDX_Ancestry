# admixture/

The following files are expected here:

- `genotype_1000g_nopal_prune.5.Q` — ancestry proportions per sample for K = 5, all samples projected onto the 1000 Genomes ancestral populations (produced by `scripts/admixture.md`)
- `genotype_1000g_nopal_prune_ref.5.Q`, `genotype_1000g_nopal_prune_ref.5.P` — ancestry proportions and allele frequencies estimated with the 1000 Genomes samples only (produced by `scripts/admixture.md`, not used by the plots)
- `admixture.pdf` — ADMIXTURE barplots, Fig. 1E (produced by `scripts/create_plots.py`)
- `admixture_table.csv` — ancestry proportions of the cohort blood samples, Extended Data Table 12 (produced by `scripts/create_plots.py`)
- `admixture_superpop_table.csv` — mean ancestry proportions of each 1000 Genomes superpopulation, Extended Data Table 12 (produced by `scripts/create_plots.py`)
