# ADMIXTURE

To run the admixture analysis, [ADMIXTURE software](https://dalexander.github.io/admixture/download.html) needs to be available (for example through the `admixture` command). Expects the data obtained using the [plink steps](./plink.md), and should be run from the root of the repository.

The ancestral populations are estimated using only the 1000 Genomes samples, and the cohort samples are then projected onto them.

Keep only the 1000 Genomes samples.
```bash
plink --bfile data/genotype_1000g_nopal_prune --keep data/1000g.fam --make-bed --out data/genotype_1000g_nopal_prune_ref
```

Estimate ancestry proportions of the 1000 Genomes samples for K = 5, with cross-validation error.
```bash
cd admixture
admixture --cv ../data/genotype_1000g_nopal_prune_ref.bed 5 -j4
```

Project all samples onto the ancestral populations estimated with the 1000 Genomes samples.
```bash
cp genotype_1000g_nopal_prune_ref.5.P genotype_1000g_nopal_prune.5.P.in
admixture -P ../data/genotype_1000g_nopal_prune.bed 5 -j4
```
