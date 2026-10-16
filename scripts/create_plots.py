import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D

# This data dictionary contains the samples from the 1000 Genomes 
# Project with their corresponding Superpopulation
labels_kg = (
    pd.read_csv('data/igsr_samples.tsv',sep='\t')[['Sample name','Superpopulation code']]
    .rename(columns={'Sample name':'ID','Superpopulation code':'superpop'})
    .query('superpop in ["AFR","AMR","EAS","EUR","SAS"]')
)

admixture = (
    pd.concat([
        pd.read_csv('data/genotype_1000g_geno_mind.fam',sep=' ',header=None, names=['FID','ID','a','b','c','d'])[['ID']],
        pd.read_csv('admixture/genotype_1000g_geno_mind.5.Q',sep=' ',header=None, names=['pop1','pop2','pop3','pop4','pop5'])],axis=1)
    .merge(labels_kg, on='ID',how='left')
    .sort_values(['superpop','pop1'])
    .assign(superpop=lambda x: x.superpop.mask(x.ID.str[0:2] == "PD",'BRA'))
    .dropna(subset='superpop')
)

# Create the plot use in Fig 1E
fig, axes = plt.subplots(1,6,figsize=(17,5),sharey=True,tight_layout=True)
cluster_names = list(admixture.columns)

for i, sp in enumerate(['BRA','EUR','AFR','AMR','EAS','SAS']):
    print(sp)
    adm_sp = admixture.query('superpop == @sp')
    cluster_names = list(adm_sp.columns[adm_sp.columns.str.startswith('pop')])
    main_pop = adm_sp[cluster_names].mean().idxmax()
    cluster_names.remove(main_pop)

    (
        adm_sp
        .assign(sort_order=adm_sp[cluster_names].mean(axis=1))
        .sort_values('sort_order')
        .drop(columns=['ID','superpop','sort_order'])
        .plot(kind='bar',stacked=True,width=1,ax=axes[i],rasterized=True,
              sharey=True,title=sp + " - cohort" if sp == "BRA" else sp,
              legend=False,ylim=(0,1))
    )
    axes[i].set_xticklabels([])
    axes[i].tick_params(axis='both', which='both', length=0)
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
## save as pdf
plt.savefig('admixture/admixture.pdf',bbox_inches='tight')

# Save the admixture table used in Supplementary Table 12
(
    admixture
    .assign(sort_order=adm_sp[cluster_names].mean(axis=1))
    .sort_values(['superpop','sort_order'])
    .drop(columns=['sort_order'])
    .to_csv('admixture/admixture_table.csv',index=False)
)

# Create the PCA plot used in Fig 1D
pca = (
    pd.read_csv('pca/genotype_1000g_nopal_prune.eigenvec',sep=r'\s+',header=None)
    .set_axis(['FID','ID'] + [f'PC{i}' for i in range(1,11)], axis=1)
    .merge(labels_kg, on='ID',how='left')
    .assign(superpop=lambda x: x.superpop.mask(x.ID.str[0:2] == "PD",'BRA'))
    .dropna(subset='superpop')
    # PC signs are arbitrary; flip them to match the orientation in the paper
    .assign(PC1=lambda x: -x.PC1, PC2=lambda x: -x.PC2)
)

# Percentage of variance explained by each PC (relative to the top 10 PCs)
eigenval = pd.read_csv('pca/genotype_1000g_nopal_prune.eigenval',header=None)[0]
var_exp = 100 * eigenval / eigenval.sum()

pop_colors = {'AFR':'#E41A1C','AMR':'#FDAE61','EAS':'#4DAF4A','EUR':'#377EB8','SAS':'#984EA3'}

fig, ax = plt.subplots(figsize=(5,4.5),tight_layout=True)
for sp, color in pop_colors.items():
    pca_sp = pca.query('superpop == @sp')
    ax.scatter(pca_sp.PC1, pca_sp.PC2, s=3, color=color, alpha=0.6,
               linewidths=0, rasterized=True, label=sp)
pca_bra = pca.query('superpop == "BRA"')
ax.scatter(pca_bra.PC1, pca_bra.PC2, s=25, marker='D', color='black',
           edgecolors='white', linewidths=0.4, label='BRA')

ax.set_xlabel(f'PC1 ({var_exp[0]:.1f}%)')
ax.set_ylabel(f'PC2 ({var_exp[1]:.1f}%)')
legend_handles = (
    [Line2D([],[],marker='s',ls='',color=c,markersize=8,label=sp) for sp, c in pop_colors.items()]
    + [Line2D([],[],marker='D',ls='',color='black',markersize=6,label='BRA')]
)
ax.legend(handles=legend_handles, loc='lower right', handletextpad=0.3)
## save as pdf
plt.savefig('pca/pca_plot.pdf',bbox_inches='tight')
