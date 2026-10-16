# ADMIXTURE

To run the admixture analysis, [ADMIXTURE software](https://dalexander.github.io/admixture/download.html) needs to be available (for example through the `admixture` command). Expects the data obtained using the [plink steps](./plink.md), and should be run from the root of the repository.

Estimate ancestry proportions for K = 5, with cross-validation error.
```bash
cd admixture
admixture --cv ../data/genotype_1000g_geno_mind.bed 5
```
