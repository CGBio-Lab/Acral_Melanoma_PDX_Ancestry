import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42})

# This data dictionary contains the samples from the 1000 Genomes
# Project with their corresponding Superpopulation
labels_kg = (
    pd.read_csv('data/1000g_panel.tsv',sep='\t')[['sample','super_pop']]
    .rename(columns={'sample':'ID','super_pop':'superpop'})
)

# Cohort samples: sample type (blood, tumour, cell_line) and samples excluded from the analysis.
# Samples not in the metadata (2024 batch) are blood samples. Only blood samples in the final set.
metadata = pd.read_csv('data/genotype_samples_metadata.csv').rename(columns={'sampleID':'ID'})
excluded = metadata.loc[metadata.notes.str.contains('exclude', na=False), 'ID'].tolist()

def add_labels(df):
    """Label the samples by superpopulation (BRA for the cohort) and keep only the cohort blood samples."""
    return (
        df
        .merge(labels_kg, on='ID', how='left')
        .merge(metadata[['ID','sample_type']], on='ID', how='left')
        .fillna({'superpop':'BRA', 'sample_type':'blood'})
        .query('superpop != "BRA" or (sample_type == "blood" and ID not in @excluded)')
    )

clusters = ['K1','K2','K3','K4','K5']
admixture = add_labels(
    pd.concat([
        pd.read_csv('data/genotype_1000g_nopal_prune.fam',sep=' ',header=None, names=['FID','ID','a','b','c','d'])[['ID']],
        pd.read_csv('admixture/genotype_1000g_nopal_prune.5.Q',sep=' ',header=None, names=clusters)],axis=1)
)

# Create the plot used in Fig 1E
cluster_colors = ['#E41A1C','#377EB8','#4DAF4A','#FF7F00','#984EA3']
eur_cluster = admixture.query('superpop == "EUR"')[clusters].mean().idxmax()
superpops = ['AFR','AMR','EAS','EUR','SAS','BRA']

fig, axes = plt.subplots(1,6,figsize=(12,3.5),sharey=True)
for i, sp in enumerate(superpops):
    adm_sp = admixture.query('superpop == @sp')
    if sp == 'BRA':
        # Cohort samples sorted by European ancestry
        adm_sp = adm_sp.sort_values(eur_cluster)
    else:
        # Reference samples sorted by their main cluster, then by ancestry proportions
        adm_sp = (
            adm_sp
            .assign(main_cluster=adm_sp[clusters].idxmax(axis=1))
            .sort_values(['main_cluster'] + clusters, ascending=[True] + [False]*len(clusters))
        )
    (
        adm_sp[clusters].reset_index(drop=True)
        .plot(kind='bar',stacked=True,width=1,linewidth=0,ax=axes[i],color=cluster_colors,
              legend=False,ylim=(0,1),xlim=(-0.5,len(adm_sp)-0.5))
    )
    axes[i].set_title('Brazil' if sp == 'BRA' else sp, fontsize=10, fontweight='bold', pad=4)
    axes[i].set_xticks([])
    axes[i].tick_params(left=(i == 0), labelleft=(i == 0), bottom=False)
    axes[i].spines['left'].set_visible(i == 0)
    axes[i].spines['right'].set_visible(i == len(superpops) - 1)
axes[0].set_ylabel('Ancestry proportion', fontsize=11)
axes[0].legend([f'Cluster {i}' for i in range(1,6)], loc='upper center', bbox_to_anchor=(3, 1.35),
               fontsize=7, ncol=5, framealpha=0.9)
fig.subplots_adjust(wspace=0.05, bottom=0.18, top=0.82)
## save as pdf
plt.savefig('admixture/admixture.pdf',dpi=300,bbox_inches='tight')

# Save the admixture tables used in Extended Data Table 12 (SNP array):
# ancestry proportions of the cohort samples, and mean ancestry proportions of each 1000 Genomes superpopulation
(
    admixture
    .query('superpop == "BRA"')
    .rename(columns={'ID':'IID'})
    [['IID','sample_type'] + clusters]
    .to_csv('admixture/admixture_table.csv',index=False)
)
(
    admixture
    .query('superpop != "BRA"')
    .rename(columns={'superpop':'population'})
    .groupby('population')[clusters].mean()
    .to_csv('admixture/admixture_superpop_table.csv')
)

# Create the PCA plot used in Fig S1D
pca = add_labels(
    pd.read_csv('pca/genotype_1000g_nopal_prune.eigenvec',sep=r'\s+',header=None)
    .set_axis(['FID','ID'] + [f'PC{i}' for i in range(1,11)], axis=1)
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
