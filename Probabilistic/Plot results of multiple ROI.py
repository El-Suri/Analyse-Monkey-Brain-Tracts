#!/usr/bin/env python
# coding: utf-8

# # Plot & analyse results

# In[21]:


import os
import pandas as pd
import numpy as np
import glob
import seaborn as sns
from matplotlib import pyplot as plt
import statistics


# In[22]:


# Read in data

df_gschwind = pd.read_csv('/cubric/data/c1639425/Monkey_Brains/results_df/proportion_gschwind_bst_ncc_subic_antthal_globpal_df')
display(df_gschwind)

#df_eickhoff = pd.read_csv('/cubric/data/c1639425/Monkey_Brains/proportion_eickhoff_distance_corrected_just_subiculum_streamline_corrected_hipp_ant_thal_caudate_df')
#display(df_eickhoff)

df_eickhoff = pd.read_csv('/cubric/data/c1639425/Monkey_Brains/results_df/proportion_eickhoff_streamline_corrected_bst_subic_ncc_ant_thal_extglobpal_df')
display(df_eickhoff)

df_raw_data = pd.read_csv('/cubric/data/c1639425/Monkey_Brains/results_df/distance_corrected_raw_data_bst_subic_ncc_ant_thal_extGP_df')
display(df_raw_data)


# # Plot Raw Data

# In[23]:


raw_figure, axes = plt.subplots(figsize=(20,10))

# ax1 - Subic Connections
subic_data = df_raw_data[['subic_ant_thal','subic_bst','subic_ncc','subic_ext_glob_pal']]
ax1 = plt.subplot(1,3,1)
sns.boxplot(ax = ax1, x = "variable", y = "value", data = pd.melt(subic_data))
ax1.set_xticklabels(['Ant Thal','BNST','NCC','Ext-GP'], fontsize = 11)
ax1.set_title('Subiculum')
ax1.set_xlabel('Target Regions')
ax1.set_ylabel('\"Connections\"')


raw_figure.tight_layout()
raw_figure.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/raw_data_dist_corrected.png')


# ## Plot Gschwind 

# In[8]:


list(df_gschwind.columns)


# In[24]:


# PLOT GSCHWIND

axis_names = list(df_gschwind.columns.values)[1:] 
gschwind_figure, axes = plt.subplots(figsize=(20,10))


# ax1 - Subic Connections
subic_data = df_gschwind[['bst_subic','subic_ant_thal','ncc_subic','subic_ext_glob_pal',]]
ax1 = plt.subplot(2,3,1)
sns.boxplot(ax = ax1, x = "variable", y = "value", data = pd.melt(subic_data))
ax1.set_xticklabels(['BNST', 'Ant Thal','NCC','Glob Pal',], fontsize = 11)
ax1.set_title('Subiculum')
ax1.set_xlabel('ROIs')
ax1.set_ylabel('Connection Proportion')
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

gschwind_figure.tight_layout()
gschwind_figure.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/gschwind_bst_ncc_subic_antthal_globpal.png')


# ## Run t-tests

# In[28]:


test_df = df_gschwind[['Subjects','bst_subic','subic_ant_thal','ncc_subic','subic_ext_glob_pal',]]
test_long = pd.melt(test_df, id_vars=['Subjects'], value_vars=['bst_subic','subic_ant_thal','ncc_subic','subic_ext_glob_pal'])
print(test_long)


# In[23]:


from scipy import stats
subic_result = stats.wilcoxon(x = subic_data['bst_subic'], y=subic_data['ncc_subic'], zero_method='wilcox', correction=False)
print(subic_result)


# ## Plot Eickhoff Method, subic only

# In[18]:


axis_names = list(df_eickhoff.columns.values)[1:] 

eickhoff_figure, axes = plt.subplots(figsize=(20,10))


# ax1 - Subic Connections
subic_data = df_eickhoff[['subic_bst','subic_ant_thal','subic_ncc','subic_ext_glob_pal']]
ax1 = plt.subplot(1,3,1)
sns.boxplot(ax = ax1, x = "variable", y = "value", data = pd.melt(subic_data))
ax1.set_xticklabels(['BNST','Ant Thal','NCC','Glob Pal'], fontsize = 11)
ax1.set_title('Subiculum')
ax1.set_xlabel('Target Regions')
ax1.set_ylabel('Connection Proportion')
#ax1.set_ylim(0,0.6)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

eickhoff_figure.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/eickhoff_bst_ncc_subic_antthal_globpal.png')


# # Eickhoff, all ROIS

# In[35]:


eickhoff_figure, axes = plt.subplots(figsize=(20,10))


# ax1 - Subic Connections
subic_data = df_eickhoff[['subic_bst','subic_ncc','subic_hippocampus','subic_caudate','subic_ant_thal']]
ax1 = plt.subplot(2,3,1)
sns.boxplot(ax = ax1, x = "variable", y = "value", data = pd.melt(subic_data))
ax1.set_xticklabels(['BNST','NCC','Hippocampus', 'Caudate','Ant Thal'], fontsize = 11)
ax1.set_title('Subiculum')
ax1.set_xlabel('Target Regions')
ax1.set_ylabel('Connection Proportion')
#ax1.set_ylim(0,0.6)
#plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)                    
  

# ax2 - BST Connections
bst_connections = df_eickhoff[['bst_subic','bst_ncc','bst_hippocampus','bst_caudate','bst_ant_thal']]
ax2 = plt.subplot(2,3,2, sharey = ax1)
sns.boxplot(ax = ax2, x = "variable", y = "value", data = pd.melt(bst_connections))
ax2.set_xticklabels(['Subiculum', 'NCC', 'Hippocampus', 'Caudate', ' Ant Thal'], fontsize = 11)
ax2.set_title('BNST')
ax2.set_xlabel('Target Regions')
ax2.set_ylabel('Connection Proportion')
#plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)                    
  

# ax3 - NCC Connections
ncc_connections = df_eickhoff[['ncc_subic','ncc_bst','ncc_hippocampus','ncc_caudate','ncc_ant_thal']]
ax3 = plt.subplot(2,3,3, sharey = ax1)
sns.boxplot(ax = ax3, x = "variable", y = "value", data = pd.melt(ncc_connections))
ax3.set_xticklabels(['Subiculum', 'BNST', 'Hippocampus', 'Caudate', 'Ant Thal'], fontsize = 11)
ax3.set_title('NCC')
ax3.set_xlabel('Target Regions')
ax3.set_ylabel('Connection Proportion')
#plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)                    
  

# ax4 - Hippocampus Connections
hippocampus_connections = df_eickhoff[['hippocampus_subic','hippocampus_bst','hippocampus_ncc','hippocampus_caudate','hippocampus_ant_thal']]
ax4 = plt.subplot(2,3,4,sharey = ax1)
sns.boxplot(ax = ax4, x = "variable", y = "value", data = pd.melt(hippocampus_connections))
ax4.set_xticklabels(['Subiculum','BNST','NCC','Caudate','Ant Thal'], fontsize = 11)
ax4.set_title('Hippocampus')
ax4.set_xlabel('Target Regions')
ax4.set_ylabel('Connection Proportion')
#plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)


# ax5 - Caudate Connections
caudate_connections = df_eickhoff[['caudate_subic','caudate_bst','caudate_ncc','caudate_hippocampus','caudate_ant_thal']]
ax5 = plt.subplot(2,3,5,sharey = ax1)
sns.boxplot(ax = ax5, x = "variable", y = "value", data = pd.melt(caudate_connections))
ax5.set_xticklabels(['Subiculum','BNST','NCC','Hippocampus','Ant Thal'], fontsize = 11)
ax5.set_title('Caudate')
ax5.set_xlabel('Target Regions')
ax5.set_ylabel('Connection Proportion')
#plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)


# ax6 - Ant Thal Connections
ant_thal_connections = df_eickhoff[['ant_thal_subic','ant_thal_bst','ant_thal_ncc','ant_thal_hippocampus','ant_thal_caudate']]
ax6 = plt.subplot(2,3,6,sharey = ax1)
sns.boxplot(ax = ax6, x = "variable", y = "value", data = pd.melt(ant_thal_connections))
ax6.set_xticklabels(['Subiculum','BNST','NCC','Hippocampus','Caudate'], fontsize = 11)
ax6.set_title('Ant Thal')
ax6.set_xlabel('Target Regions')
ax6.set_ylabel('Connection Proportion')
#plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45)                    
                     
                     
eickhoff_figure.tight_layout()
eickhoff_figure.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/eickhoff_all_distance_corrected.png')


# In[26]:


from scipy import stats
subic_result = stats.wilcoxon(x = subic_data['subic_bst'], y=subic_data['subic_ncc'], zero_method='wilcox', correction=False)
print(subic_result)
bnst_result = stats.wilcoxon(x = bst_connections['bst_ncc'], y=bst_connections['bst_subic'], zero_method='wilcox', correction=False)
print(bnst_result)
ncc_result = stats.wilcoxon(x = ncc_connections['ncc_subic'], y=ncc_connections['ncc_bst'], zero_method='wilcox', correction=False)
print(ncc_result)


# ## Plot mean ROI sizes

# In[27]:


gschwind_just_subic, axes = plt.subplots(figsize=(10,5))


# ax1 - Subic Connections
subic_data = df_gschwind[['bst_subic','ncc_subic','subic_hippocampus','subic_caudate','subic_ant_thal']]
ax1 = plt.subplot(1,1,1)
sns.boxplot(ax = ax1, x = "variable", y = "value", data = pd.melt(subic_data))
ax1.set_xticklabels(['BNST', 'NCC','Hippocampus','Caudate','Ant Thal'], fontsize = 11)
ax1.set_title('Subiculum')
ax1.set_xlabel('ROIs')
ax1.set_ylabel('Connection Proportion')
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

gschwind_just_subic.tight_layout()


# In[80]:


means = connections_df.mean(axis = 0, numeric_only= True) 
sems = connections_df.sem(axis = 0, numeric_only=True)
z_score = 1.96
lcb = means - z_score* sems
ucb = means + z_score* sems

mean_vols =  before_multiplication_df.mean(axis = 0, numeric_only= True) 
stds_vols = before_multiplication_df.std(axis = 0, numeric_only=True)
plot_roi_sizes = before_multiplication_df.drop(['Subjects'], axis = 1)

fig, ax = plt.subplots(figsize = (12,8))
ax = sns.boxplot(ax = ax, data = plot_roi_sizes)
fig.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/subic_tracts_bst_sizes.png')


# In[38]:


# ax2 - BST Connections
bst_connections = df_gschwind[['bst_subic','bst_ncc','bst_hippocampus','bst_caudate','bst_ant_thal']]
ax2 = plt.subplot(2,3,2)
sns.boxplot(ax = ax2, x = "variable", y = "value", data = pd.melt(bst_connections))
ax2.set_xticklabels(['Subiculum', 'NCC','Hippocampus','Caudate','Ant Thal'], fontsize = 11)
ax2.set_title('BNST')
ax2.set_xlabel('ROIs')
ax2.set_ylabel('Connection Proportion')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)


# ax3 - NCC Connections
ncc_connections = df_gschwind[['ncc_subic','bst_ncc','ncc_hippocampus','ncc_caudate','ncc_ant_thal']]
ax3 = plt.subplot(2,3,3)
sns.boxplot(ax = ax3, x = "variable", y = "value", data = pd.melt(ncc_connections))
ax3.set_xticklabels(['Subiculum', 'BNST','Hippocampus','Caudate','Ant Thal'], fontsize = 11)
ax3.set_title('NCC')
ax3.set_xlabel('ROIs')
ax3.set_ylabel('Connection Proportion')
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)


# ax4 - Hippocampus Connections
hippocampus_connections = df_gschwind[['subic_hippocampus','bst_hippocampus','ncc_hippocampus','hippocampus_caudate','hippocampus_ant_thal']]
ax4 = plt.subplot(2,3,4)
sns.boxplot(ax = ax4, x = "variable", y = "value", data = pd.melt(hippocampus_connections))
ax4.set_xticklabels(['Subiculum','BNST','NCC','Caudate','Ant Thal'], fontsize = 11)
ax4.set_title('Hippocampus')
ax4.set_xlabel('ROIs')
ax4.set_ylabel('Connection Proportion')
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)


# ax5 - Caudate Connections
caudate_connections = df_gschwind[['subic_caudate','bst_caudate','ncc_caudate','hippocampus_caudate','caudate_ant_thal']]
ax5 = plt.subplot(2,3,5)
sns.boxplot(ax = ax5, x = "variable", y = "value", data = pd.melt(caudate_connections))
ax5.set_xticklabels(['Subiculum','BNST','NCC','Hippocampus','Ant Thal'], fontsize = 11)
ax5.set_title('Caudate')
ax5.set_xlabel('ROIs')
ax5.set_ylabel('Connection Proportion')
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)


# ax6 - Ant Thal Connections
ant_thal_connections = df_gschwind[['subic_ant_thal','bst_ant_thal','ncc_ant_thal','hippocampus_ant_thal','caudate_ant_thal']]
ax6 = plt.subplot(2,3,6)
sns.boxplot(ax = ax6, x = "variable", y = "value", data = pd.melt(ant_thal_connections))
ax6.set_xticklabels(['Subiculum','BNST','NCC','Hippocampus','Caudate'], fontsize = 11)
ax6.set_title('Ant Thal')
ax6.set_xlabel('ROIs')
ax6.set_ylabel('Connection Proportion')
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45)

gschwind_figure.tight_layout()

gschwind_figure.savefig('/home/c1639425/Desktop/Monkey_processing/Multiple_roi_results/gschwind_distance_corrected.png')
#stats.ttest_rel(plotting_data['Subic_BST'], plotting_data['Subic_NCC']) 

