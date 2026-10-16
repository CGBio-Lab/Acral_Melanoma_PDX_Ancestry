# PLINK pipeline

This set of instructions assumes that [PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) is available throught the `plink` command and should be run from the root of the repository.

The source data needs to be added to [../data/](../data/)

The first merge attempt is expected to fail, producing a list of mismatched SNPs in `data/genotype_1000g-merge.missnp`.
```bash
plink --bfile data/genotype_samples --bmerge data/1000g --make-bed --merge-mode 4 --out data/genotype_1000g
```

Flip the strand of the mismatched SNPs.
```bash
plink --bfile data/genotype_samples --flip data/genotype_1000g-merge.missnp --make-bed --out data/genotype_samples_flip
```

Once flipped, the merge could still find mismatched SNPs after flipping.
```bash
plink --bfile data/genotype_samples_flip --bmerge data/1000g --make-bed --merge-mode 4 --out data/genotype_1000g
```

Remove the SNPs still mismatched.
```bash
plink --bfile data/genotype_samples_flip --exclude data/genotype_1000g-merge.missnp --make-bed --out data/genotype_samples_flip_filter
```

Merge the clean file with 1000 Genomes.
```bash
plink --bfile data/genotype_samples_flip_filter --bmerge data/1000g --make-bed --merge-mode 4 --out data/genotype_1000g
```

Remove SNPs with more than 1% missing genotypes.
```bash
plink --bfile data/genotype_1000g --geno 0.01 --make-bed --out data/genotype_1000g_geno
```

Remove samples with more than 10% missing genotypes.
```bash
plink --bfile data/genotype_1000g_geno --make-bed --mind 0.1 --out data/genotype_1000g_geno_mind
```

Remove palindromic (A/T, C/G) SNPs.
```bash
awk '($5=="A"&&$6=="T")||($5=="T"&&$6=="A")||($5=="C"&&$6=="G")||($5=="G"&&$6=="C") {print $2}' data/genotype_1000g_geno_mind.bim > data/at_cg.txt
plink --bfile data/genotype_1000g_geno_mind --exclude data/at_cg.txt --make-bed --out data/genotype_1000g_nopal
```

Find SNPs in linkage disequilibrium (window 50, step 5, r² 0.5).
```bash
plink --bfile data/genotype_1000g_nopal --indep-pairwise 50 5 0.5 --out data/plink
```

Keep the pruned SNPs (not in the logs). This pruned file is used for computing the principal components (data).
```bash
plink --bfile data/genotype_1000g_nopal --extract data/plink.prune.in --make-bed --out data/genotype_1000g_nopal_prune
```

Compute the first 10 principal components.
```bash
plink --bfile data/genotype_1000g_nopal_prune --pca 10 --out pca/genotype_1000g_nopal_prune
```
