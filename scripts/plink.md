# PLINK pipeline

This set of instructions assumes that [PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) is available throught the `plink` command and should be run from the root of the repository.

The source data needs to be added to [../data/](../data/)

## Quality control of each dataset

Convert the 2026 cohort genotypes from PED/MAP to binary format.
```bash
plink --file data/genotype_samples_2026 --make-bed --out data/genotype_samples_2026
```

Keep autosomal SNPs with A/C/G/T alleles, removing SNPs and samples with more than 20% missing genotypes, and then those with more than 3% missing genotypes.
```bash
for ds in 1000g genotype_samples_2024 genotype_samples_2026; do
  plink --bfile data/$ds --autosome --snps-only just-acgt --geno 0.2 --mind 0.2 --make-bed --out data/${ds}_loose
  plink --bfile data/${ds}_loose --geno 0.03 --mind 0.03 --make-bed --out data/${ds}_qc
done
```

Rename the SNPs as `CHR:POS` so they match across datasets, and remove the duplicated positions.
```bash
for ds in 1000g genotype_samples_2024 genotype_samples_2026; do
  awk '$4>0 {print $2, $1":"$4}' data/${ds}_qc.bim > data/${ds}_ids.txt
  plink --bfile data/${ds}_qc --update-name data/${ds}_ids.txt --make-bed --out data/${ds}_ids
  awk 'seen[$2]++ {print $2}' data/${ds}_ids.bim > data/${ds}_dups.txt
  plink --bfile data/${ds}_ids --exclude data/${ds}_dups.txt --make-bed --out data/${ds}_dedup
done
```

## Merge with 1000 Genomes

The first merge attempt is expected to fail, producing a list of mismatched SNPs in `data/genotype_1000g-merge.missnp`.
```bash
printf "data/genotype_samples_2024_dedup\ndata/genotype_samples_2026_dedup\n" > data/merge_list.txt
plink --bfile data/1000g_dedup --merge-list data/merge_list.txt --merge-mode 4 --make-bed --out data/genotype_1000g
```

Flip the strand of the mismatched SNPs in the cohort datasets.
```bash
for ds in genotype_samples_2024 genotype_samples_2026; do
  plink --bfile data/${ds}_dedup --flip data/genotype_1000g-merge.missnp --make-bed --out data/${ds}_flip
done
```

Once flipped, the merge could still find mismatched SNPs.
```bash
printf "data/genotype_samples_2024_flip\ndata/genotype_samples_2026_flip\n" > data/merge_list.txt
plink --bfile data/1000g_dedup --merge-list data/merge_list.txt --merge-mode 4 --make-bed --out data/genotype_1000g
```

Remove the SNPs still mismatched from all datasets. The flipped files are not used further, so the mismatched SNPs are removed instead of flipped.
```bash
for ds in 1000g_dedup genotype_samples_2024_dedup genotype_samples_2026_dedup; do
  plink --bfile data/$ds --exclude data/genotype_1000g-merge.missnp --make-bed --out data/${ds}_filter
done
```

The merge is expected to find the remaining mismatched SNPs (those fixed by flipping).
```bash
printf "data/genotype_samples_2024_dedup_filter\ndata/genotype_samples_2026_dedup_filter\n" > data/merge_list.txt
plink --bfile data/1000g_dedup_filter --merge-list data/merge_list.txt --merge-mode 4 --make-bed --out data/genotype_1000g
```

Remove them from all datasets.
```bash
for ds in 1000g_dedup_filter genotype_samples_2024_dedup_filter genotype_samples_2026_dedup_filter; do
  plink --bfile data/$ds --exclude data/genotype_1000g-merge.missnp --make-bed --out data/${ds}2
done
```

Merge the clean files.
```bash
printf "data/genotype_samples_2024_dedup_filter2\ndata/genotype_samples_2026_dedup_filter2\n" > data/merge_list.txt
plink --bfile data/1000g_dedup_filter2 --merge-list data/merge_list.txt --merge-mode 4 --make-bed --out data/genotype_1000g
```

## Preparation for PCA and ADMIXTURE

Keep only the SNPs genotyped in all samples (present in the three datasets).
```bash
plink --bfile data/genotype_1000g --geno 0.001 --make-bed --out data/genotype_1000g_geno
```

Remove palindromic (A/T, C/G) SNPs.
```bash
awk '($5=="A"&&$6=="T")||($5=="T"&&$6=="A")||($5=="C"&&$6=="G")||($5=="G"&&$6=="C") {print $2}' data/genotype_1000g_geno.bim > data/at_cg.txt
plink --bfile data/genotype_1000g_geno --exclude data/at_cg.txt --make-bed --out data/genotype_1000g_nopal
```

Find SNPs in linkage disequilibrium (window 50, step 5, r² 0.5).
```bash
plink --bfile data/genotype_1000g_nopal --indep-pairphase 50 5 0.5 --out data/plink
```

Keep the pruned SNPs (not in LD). This pruned file is used for computing the principal components and the ancestry proportions.
```bash
plink --bfile data/genotype_1000g_nopal --extract data/plink.prune.in --make-bed --out data/genotype_1000g_nopal_prune
```

## PCA

Label the 1000 Genomes samples as the reference (`REF`) and the cohort samples as `BRA`.
```bash
awk 'NR==FNR {ref[$2]; next} {print $1, $2, ($2 in ref) ? "REF" : "BRA"}' data/1000g.fam data/genotype_1000g_nopal_prune.fam > data/pca_clusters.txt
```

Compute the first 10 principal components using only the 1000 Genomes samples, and project the cohort samples onto them.
```bash
plink --bfile data/genotype_1000g_nopal_prune --pca 10 --within data/pca_clusters.txt --pca-cluster-names REF --out pca/genotype_1000g_nopal_prune
```
