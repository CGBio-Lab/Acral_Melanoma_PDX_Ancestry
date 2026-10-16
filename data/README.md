# data/

The following files are expected here:

### Source data (to run the full pipeline from [`scripts/plink.md`](../scripts/plink.md))
- `genotype_samples.bed`, `genotype_samples.bim`, `genotype_samples.fam` — cohort germline genotypes (PLINK binary)
- `1000g.bed`, `1000g.bim`, `1000g.fam` — 1000 Genomes reference genotypes (PLINK binary)

### Required to generate the figures (`scripts/create_plots.py`)
- `igsr_samples.tsv` — 1000 Genomes sample metadata from [IGSR](https://www.internationalgenome.org/) (superpopulation labels)
- `genotype_1000g_geno_mind.fam` — sample IDs after QC (produced by `scripts/plink.md`)
- `genotype_1000g_geno_mind.bed`, `genotype_1000g_geno_mind.bim` — QC'd genotypes, input to ADMIXTURE (produced by `scripts/plink.md`)
