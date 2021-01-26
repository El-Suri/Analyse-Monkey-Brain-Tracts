#!/usr/bin/env python
# coding: utf-8

# # Process multiple ROI results
# 
# 
# The multiple ROI analysis produces a n*n matrix detailing the number of waypoints between each ROI. To make these numbers more meaningful, you can rescale the results in a couple of different ways. Its important to note that these methods are for scaling, the pattern of results should stay the same.
# 
# ### The simplest way of doing this, the [Gschwind method](https://academic.oup.com/cercor/article/22/7/1564/291933):
# 
# "... fiber tracking was initiated in both directions (from seed to target and vice versa), and these values were subsequently averaged. To obtain a measure of connectivity probability between ROIs (analysis 2), we used this average number of streamlines per seed voxel reaching the target (Croxson et al. 2005), expressed as a proportion of all successful samples in all pairwise connections in both hemispheres (see also Croxson et al. 2005; Eickhoff et al. 2010)."
# 
# So take the average waytotal (n connections) for each ROI pairing in both directions. Then express as a proportion of the total waytotal of all connections. 
# 
# ### A second more complex way of calculating it is the [Eickhoff method](https://pubmed.ncbi.nlm.nih.gov/20445067/):
# 
# 1. Waytotal of the connection (avereaged both ways) / Summed way total of seed to all other ROIs
# 
# 2. Multiplied by the mean total waytotal of all seeds and target combinations. They call this a connection density value.
# 
# 3. Divide by the size of the target ROI.
# 
# 4. Multiply by the mean size of all target ROIs.
# 
# 
# This way has the advantage of correcting for both ROI mask sizes. 

# In[12]:


# Import all libraries needed

import os
import pandas as pd
import numpy as np
import glob
import seaborn as sns
from matplotlib import pyplot as plt
import statistics


# In[13]:


# Collect some useful path and file info. 

folder_path = '/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/'
subject_folders = sorted(glob.glob(folder_path))
print(subject_folders)

subjects = []
for file in sorted(glob.glob(folder_path)):
    name = file.split(os.path.sep)[-3]
    subjects.append(name)
    
print(subjects)


# ## Determine the number of voxels for each participants ROI masks.
# 
# Counts the total and creates a file for each subject.

# In[14]:


# this needs to be in the same order as it was processed. 
#The folder of the results will be named in this order. This roi argument is used extensively elsewhere.
rois = 'bst','ncc','subic', 'ant_thal', 'ext_glob_pal'
bst_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_BST_central.nii.gz'))
ncc_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_accumbcore_all_accum_nuc.nii'))
subic_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_subiculum_all.nii'))
hippocampus_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_hippocampus.nii'))
caudate_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_caudate_nucleus.nii'))
anterior_thalamus = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_anteromedial_thalamic_all_anterior_thalamic.nii'))
ext_glob_pal = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_ext_GP.nii'))

list_of_masks = list(zip(bst_masks,ncc_masks,subic_masks, anterior_thalamus, ext_glob_pal))


def get_mask_voxel_count (list_of_masks,rois, subject_folders):    
    for counter,folder in enumerate(subject_folders):
        os.chdir(folder)
        for roi_counter, roi in enumerate(rois):
            cmd = 'fslstats ' + list_of_masks[counter][roi_counter] + ' -V > ' + roi + '_voxel_size'
            print(cmd)
            os.system(cmd)
        
get_mask_voxel_count(list_of_masks,rois,subject_folders)  


# ## Create DF of ROI voxel sizes. 
# 
# This also calculates the mean size of each seeds target ROIS, which is used later in some scaling methods.

# In[15]:


# This is used later in some scaling methods

# Collect the number of voxels for each ROI you have used.
bst_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/bst_voxel_size'))
ncc_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ncc_voxel_size'))
subic_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/subic_voxel_size'))
hippocampus_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/hippocampus_voxel_size'))
caudate_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/caudate_voxel_size'))
anterior_thalamus_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ant_thal_voxel_size'))
ext_glob_pal_mask_voxels = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ext_glob_pal_voxel_size'))
print(ext_glob_pal_mask_voxels)

list_of_mask_voxels = list(zip(bst_mask_voxels,ncc_mask_voxels,subic_mask_voxels,anterior_thalamus_mask_voxels, ext_glob_pal_mask_voxels))
#print(list_of_mask_voxels)

# Create dataframes. I was before also multiplying the ROI size * streamlines. This part has been commented out.

#ROI_total_size_mult_streamlines_df = pd.DataFrame()
#ROI_total_size_mult_streamlines_df['Subjects'] = subjects
ROI_total_size_df = pd.DataFrame()
ROI_total_size_df['Subjects'] = subjects

def create_mask_vox_df(subject_folders, rois, list_of_mask_voxels,ROI_total_size_df):
    for r,roi in enumerate(rois):
        current_roi_voxels = list()
        current_roi_voxels_mult = list()
        for s,subj in enumerate(subject_folders):
            ## total number of streamlines = Number of voxels within in seed mask * number of streamlines you randomly seed from it (should be 5000)
            current_roi_voxels.append(np.loadtxt(list_of_mask_voxels[s][r])[0])
            #current_roi_voxels_mult.append(current_roi_voxels[s] * 5000)
            #print(current_roi_voxels_mult)
        #ROI_total_size_mult_streamlines_df[roi + '_total_streamlines'] = current_roi_voxels_mult
        ROI_total_size_df[roi + '_size'] = current_roi_voxels
        #print(total_streamlines_df)
    # This is to get the mean size of all the target ROIS of each seed. Used in calculations later.     
    for r,roi in enumerate(rois):
        calc_mean_df = ROI_total_size_df.drop(columns=[roi + '_size'])
        #print(calc_mean_df)
        ROI_total_size_df[roi + '_target_ROI_sizes'] = calc_mean_df.mean(axis = 1)
    return ROI_total_size_df


ROI_total_size_df = create_mask_vox_df(subject_folders, rois, list_of_mask_voxels,ROI_total_size_df)   

print(ROI_total_size_df)


# # Read in connectivity matrices

# Now read in the connectivity matrix (output of the multiple ROI bedpostx) for each subject, creating a list of matricies.

# In[17]:


number_of_subjects = 9
connection_matricies = [[] for _ in range(number_of_subjects)]

# remember to change this to your new output folder
matrix_outputs = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/probabilistic.bedpostX/bst_ncc_subic_antthal_extglobpal_distance_uncorrected/fdt_network_matrix'))

# Put each subjects output of the multiple ROI analysis into a list of matricies.
def create_list_of_matricies(number_of_subjects,matrix_outputs):
    for i in range(number_of_subjects):
        connection_matricies[i-1] = np.loadtxt(matrix_outputs[i]) 
        #connection_matricies[i-1] = np.matrix(connection_matricies[i-1])
        print(connection_matricies[i-1])
        
create_list_of_matricies(number_of_subjects,matrix_outputs)       


# ## Put matrices into a dataframe and collect useful stats along the way
# 
# This loop reads in the matricies and saves and calculates data for use in the normalisation calculations later on. 

# In[18]:


# Go through the list of matricies and create a column for each connection with a row for every subject. Avereage 
# the connection each way (e.g amyg - hippocampus, hippocampus - amyg).

#Create some vars for the loop below

number_of_rois = len(rois)
# Where the avereaged waytotals go
connections_df = pd.DataFrame()
connections_df['Subjects'] = subjects
# Where the the average of waytotal for a connection in both directions, corrected by seed ROI sizes go.
connections_df_rois_size_corrected = pd.DataFrame()
connections_df_rois_size_corrected['Subjects'] = subjects
# Where the non-avereaged waytotals go for each connection. So just each seed to target.
all_non_averaged_connections = pd.DataFrame()
all_non_averaged_connections['Subjects'] = subjects
# The sum of the waytotals for a seed to each of its targets
total_seed_to_all_other_ROIS = pd.DataFrame()
total_seed_to_all_other_ROIS['Subjects'] = subjects
# The mean of all of the seed-target combinations
mean_of_all_connections = pd.DataFrame()
mean_of_all_connections['Subjects'] = subjects

def construct_connections_dfs(rois, ROI_total_size_df):
    for row in range(number_of_rois):
        current_seed = rois[row]
        # DF to collect each seeds results for each of its targets.
        target_waypoint_collector = pd.DataFrame()
        target_waypoint_collector['Subjects'] = subjects        
        for col in range(number_of_rois):
            if col == row:
                continue
            else:
                current_target = rois[col]
                #print('Current seed is ' + current_seed)
                #print('Current target is ' + current_target)
                current_connection_rois = rois[row] + '_' + rois[col]
                seed_roi_size = list(ROI_total_size_df[rois[row] + '_size'])
                target_roi_size = list(ROI_total_size_df[rois[col] + '_size'])
                # Collec the seed to target waytotal
                curr_connection = list()
                # Collect the target to seed waytotal (same rois, but in the opposite direction).
                avrg_with = list()
                for subj in range(len((subjects))):
                    curr_connection.append(connection_matricies[subj][row][col])
                    # Avereage with the same connection in the opposite direction.
                    avrg_with.append(connection_matricies[subj][col][row])
                # Put the waytotal of the connection (one way) into a df
                all_non_averaged_connections[current_connection_rois] = curr_connection
                # Correct the waytotal of the current connection by the size of the seed roi
                corrected_values = [i / j for i, j in zip(curr_connection, seed_roi_size)]
                # Correct the waytotal of the same connection in the opposite direction by its seed roi.
                avrg_with_corrected_values = [i / j for i, j in zip(avrg_with, target_roi_size)]
                # Take the mean of the connection in both directions (not avereaged by ROI size)
                mean_connection = [statistics.mean(k) for k in zip(curr_connection, avrg_with)]
                # Take the mean of the connection in both directions, accounting for ROI sizes.
                mean_connection_roi_size_corrected  = [statistics.mean(k) for k in zip(corrected_values,avrg_with_corrected_values)]
                connections_df[current_connection_rois] = mean_connection
                connections_df_rois_size_corrected[current_connection_rois] = mean_connection_roi_size_corrected
                #print(connections_df)
                # For each target, append into a list the total number of connections to the seed
                target_waypoint_collector[current_connection_rois] = curr_connection        
        #For each seed, sum the total of all connections to all targets.
        #print(target_waypoint_collector)
        target_waypoint_collector.drop(columns=['Subjects'])
        total_seed_to_all_other_ROIS[current_seed + '_total'] = target_waypoint_collector.sum(axis = 1)
        #print(total_seed_to_all_other_ROIS)
                

construct_connections_dfs(rois, ROI_total_size_df)            

print('The df with averaged connections is ')
display(connections_df)
print('The df with averaged connections, corrected for ROI size is ')
display(connections_df_rois_size_corrected)
print('The df with all connections, not averaged is ')
display(all_non_averaged_connections)


# In[19]:


#Only one seed, just testing this atm
#just_subic_seed_data = all_non_averaged_connections[['Subjects','subic_bst','subic_ncc','subic_hippocampus','subic_caudate','subic_ant_thal']]
#print(just_subic_seed_data)

#all_non_averaged_connections = just_subic_seed_data

# Find out what the summed number of all connections is for each subject
all_non_averaged_connections['Total'] = all_non_averaged_connections.sum(axis=1, skipna = True)



# Calculate the mean of all seed and target combinations
all_non_averaged_connections['Mean_total'] = all_non_averaged_connections.mean(axis = 1, skipna = True)
display(all_non_averaged_connections)

all_non_averaged_connections.to_csv('/cubric/data/c1639425/Monkey_Brains/results_df/distance_corrected_raw_data_bst_subic_ncc_ant_thal_extGP_df', index = False)

# Add the total column to the df with averaged connections.

connections_df['Total'] = all_non_averaged_connections['Total']
connections_df['Mean_total'] = all_non_averaged_connections['Mean_total']
display(connections_df)


# # Eickhoff method
# 
# 1) Waytotal of the connection (avereaged both ways)
# 
# 2) Divide by summed way total of seed to all other ROIs
# 
# 3) Multiplied by the mean total waytotal of all seeds and target combinations. They call this a connection density value.
# 
# 4) Divide by the size of the target ROI.
# 
# 5) Multiply by the mean size of all target ROIs.
# 
# 

# In[20]:


eickhoff_df = pd.DataFrame()
eickhoff_df['Subjects'] = subjects

number_of_seeds = 5
def get_eickhoff_df():    
    for row in range(number_of_seeds):
        #row = 2 # for selecting a particular seed 
        current_seed = rois[row]
        for col in range(number_of_rois):
            if col == row:
                continue
            else:
                current_target = rois[col]
                print('The current seed ROI is ' + current_seed)
                print('The current target ROI is ' + current_target)
                current_connection_rois = rois[row] + '_' + rois[col]
                seed_roi_size = list(ROI_total_size_df[rois[row] + '_size'])
                target_roi_size = list(ROI_total_size_df[rois[col] + '_size'])
                curr_connection = list()
                avrg_with = list()
                for subj in range(len((subjects))):
                    curr_connection.append(connection_matricies[subj][row][col])
                    # For averaging with the same connection in the opposite direction.
                    avrg_with.append(connection_matricies[subj][col][row])
                # Take the mean of the connection in both directions
                #step_one = [statistics.mean(k) for k in zip(curr_connection, avrg_with)]
                print(seed_roi_size)
                streamlines_mult_seed_roi = [i * 5000 for i in seed_roi_size]
                print(streamlines_mult_seed_roi)
                step_one = [i / j for i,j in zip(curr_connection, streamlines_mult_seed_roi)]
                print('Mean of both connections is = ')
                print(step_one[0])
                # Divide by summed waytotal of the seed to all other ROIs
                print(total_seed_to_all_other_ROIS[current_seed + '_total'][0])
                step_two = [i / j for i, j in zip(step_one, total_seed_to_all_other_ROIS[current_seed + '_total'])]
                print(step_two[0])
                # Multiply by mean total of all seeds and target combos
                print(all_non_averaged_connections['Mean_total'][0])
                step_three = [i * j for i , j in zip(step_two,all_non_averaged_connections['Mean_total'])]
                print(step_three[0])
                # Divide by the size of the ROI target
                print(target_roi_size[0])
                step_four = [i / j for i, j in zip(step_three, target_roi_size)]
                print(step_four[0])
                # Multiply by mean size of all target ROIs
                print(ROI_total_size_df[current_seed + '_target_ROI_sizes'][0])
                step_five = [i * j for i, j in zip(step_four, ROI_total_size_df[current_seed + '_target_ROI_sizes'])]
                print(step_five[0])
                # Put into dataframe
                eickhoff_df[current_connection_rois] = step_five

                
get_eickhoff_df()
print(eickhoff_df)


# In[21]:


#Save eickhoff df

eickhoff_df.to_csv('/cubric/data/c1639425/Monkey_Brains/results_df/proportion_eickhoff_streamline_corrected_bst_subic_ncc_ant_thal_extglobpal_df', index = False)


# # Gschwind Method
# 
# Remove duplicate columns, then divide each value by the total number of connections for each participant.

# In[23]:


# This function was downloaded from https://thispointer.com/how-to-find-drop-duplicate-columns-in-a-dataframe-python-pandas/

def getDuplicateColumns(df):
    '''
    Get a list of duplicate columns.
    It will iterate over all the columns in dataframe and find the columns whose contents are duplicate.
    :param df: Dataframe object
    :return: List of columns whose contents are duplicates.
    '''
    duplicateColumnNames = set()
    # Iterate over all the columns in dataframe
    for x in range(df.shape[1]):
        # Select column at xth index.
        col = df.iloc[:, x]
        # Iterate over all the columns in DataFrame from (x+1)th index till end
        for y in range(x + 1, df.shape[1]):
            # Select column at yth index.
            otherCol = df.iloc[:, y]
            # Check if two columns at x 7 y index are equal
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[y])
    return list(duplicateColumnNames)

connections_df_no_dupe = connections_df.drop(columns=getDuplicateColumns(connections_df))
connections_df_rois_size_corrected = connections_df_rois_size_corrected.drop(columns=getDuplicateColumns(connections_df_rois_size_corrected))
display(connections_df_no_dupe)
list(connections_df_no_dupe.columns) 
#display(connections_df_rois_size_corrected)


# In[24]:


# Next step - divide each value by the total number of connections

proportion_gschwind_df = connections_df_no_dupe[['bst_ncc','bst_subic','bst_ant_thal','bst_ext_glob_pal','ncc_subic','ncc_ant_thal','ncc_ext_glob_pal','subic_ant_thal','subic_ext_glob_pal','ant_thal_ext_glob_pal']].div(connections_df_no_dupe.Total, axis=0)
proportion_gschwind_df.insert(0,'Subjects', subjects)
display(proportion_gschwind_df)


# In[25]:


# Save dataframe

proportion_gschwind_df.to_csv('/cubric/data/c1639425/Monkey_Brains/results_df/proportion_gschwind_bst_ncc_subic_antthal_globpal_df', index = False)


# In[ ]:




