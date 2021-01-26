#!/usr/bin/env python
# coding: utf-8

# # Probabilistic Tractography Pipeline
# 
# Here we are mostly follwing the user guide from FSLs BEDPOSTX method for running probabilistic tractography. Although this is set up to be run after having run the deterministic pipeline, with a few changes to the paths and inputs the pipeline can easily be changed to run on any dwi dataset. 
# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/UserGuide

# In[1]:


# Import all libraries needed

import os
import pandas as pd
import numpy as np
import glob
import seaborn as sns
from matplotlib import pyplot as plt
import statistics


# In[2]:


# Collect some useful path and file info. 

folder_path = '/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/'
subject_folders = sorted(glob.glob(folder_path))
print(subject_folders)

subjects = []
for file in sorted(glob.glob(folder_path)):
    name = file.split(os.path.sep)[-3]
    subjects.append(name)
    
print(subjects)


# ## Create folders and files for BEDPOSTX analysis
# 
# Find whether the BEDPOSTX-ready folder exists (here called 'probabilistic') and if not create the folder and place the appropriate files there. This will only work 'out-the-box' if you have already run the deterministic pipeline. Otherwise you only need the bval, bvec, DWI data, and a b0 mask of each participant, so you can easily alter the script below to find these for each of your subjects. Check https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/UserGuide#BEDPOSTX for a guide.

# In[ ]:


def create_bedpostx_folders (subjects, subject_folders):
    for subj, subj_folder in zip(subjects, subject_folders):
        prob_folder_location = '/cubric/data/c1639425/Monkey_Brains/derivatives/' + subj + '/dwi/probabilistic/'
        does_it_exist = glob.glob(prob_folder_location)
        if does_it_exist:
            print(subj + '\'s folder already exists')
            continue
        else:
            print(subj + '\s folder does not exist')
            print('Creating ' + subj + ' folder')
            cmd = 'mkdir ' + prob_folder_location
            print(cmd)
            os.system(cmd)

        cmd = 'cp ' + subj_folder + 'space-subject_desc-eddy_dwi_updated.bval ' + prob_folder_location + 'bvals'
        print(cmd)
        os.system(cmd)

        cmd = 'cp ' + subj_folder + 'space-subject_desc-eddy_dwi_updated.bvec ' + prob_folder_location + 'bvecs'
        print(cmd)
        os.system(cmd)

        cmd = 'cp ' + subj_folder + subj + '_dwi_bet_shuffled_FP.nii ' + prob_folder_location + 'data.nii'
        print(cmd)
        os.system(cmd)

        cmd = 'gzip ' + prob_folder_location + 'data.nii'
        print(cmd)
        os.system(cmd)

        cmd = 'rm ' + prob_folder_location + 'data.nii'
        print(cmd)
        os.system(cmd)

        cmd = 'cp ' + subj_folder + subj + '_dwi_nodif_bet_mask.nii.gz ' + prob_folder_location + 'nodif_brain_mask.nii.gz'
        print(cmd)
        os.system(cmd)

    
# create_bedpostx_folders(subjects,subject_folders)

# Note, for subject 2 of the monkey dataset, part of the data is corrupted so you must use the 'trimed file' to 
# create the data.nii image as per the step above.


# # Run BedPostX  
# 
# this will take a while....

# In[ ]:


def runbedpostx(subject_folders):
    for subj_path in subject_folders:
        subject_prob_folder = subj_path + 'probabilistic/'
        os.chdir(subject_prob_folder)
        os.system('pwd')
        os.system('bedpostx ' + subj_path + 'probabilistic/')
    
#runbedpostx(subject_folders)

# Collect new bedpostx folders
bedpostx_folders = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/probabilistic.bedpostX/'))


# # Run PROBTRACKX - Single Mask
# 
# Single mask: This is the most common setting, where the seed region is defined by a user-provided mask. Streamlines are seeded from each voxel in the mask. This mask can either be a volumetric (i.e., NIFTI) file or a surface file. On the command line this is achieved by passing on a NIFTI or surface filename to the -x,--seed flag
# (

# In[5]:


# list_of_bst_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/*registered_labels_BST_central.nii.gz'))
subic_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_subiculum_all.nii'))
bedpostx_folders = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/probabilistic.bedpostX/'))
output_name = 'prob_tract_single_mask_subic'

def run_prob_trackx_single_mask(list_of_masks,bedpostx_folders,output_name):
    for folder,mask in zip(bedpostx_folders,list_of_masks):
        os.chdir(folder)
        cmd = 'probtrackx2 -x ' + mask + ' -l --onewaycondition -c 0.2 -S 2000 --steplength=0.2 -P 5000 --fibthresh=0.01 --distthresh=0.0 --sampvox=0.0 --forcedir --opd -s merged -m ' + folder + 'nodif_brain_mask.nii.gz --dir=' + folder + './' + output_name 
        print(cmd)
        os.system(cmd)
        
    
run_prob_trackx_single_mask(subic_masks,bedpostx_folders,output_name)    


# # PROBTRACKX - Multiple ROIs

# In[3]:


bst_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_BST_central.nii.gz'))
ncc_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_accumbcore_all_accum_nuc.nii'))
subic_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_subiculum_all.nii'))
hippocampus_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_hippocampus.nii'))
caudate_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_caudate_nucleus.nii'))
anterior_thalamus = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_anteromedial_thalamic_all_anterior_thalamic.nii'))
ext_glob_pal = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/ROIS/sub-*_registered_labels_ext_GP.nii'))


bedpostx_folders = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-*/dwi/probabilistic.bedpostX/'))
rois = 'bst','ncc','subic', 'ant_thal', 'ext_glob_pal'
output_name = 'bst_ncc_subic_antthal_extglobpal_distance_uncorrected'

list_of_masks = list(zip(bst_masks,ncc_masks,subic_masks, anterior_thalamus, ext_glob_pal))
# Make sure the order of these two match
print(rois)
print(list_of_masks[0])


# In[48]:


#add or remove -pd option in cmd for distance correction
def run_multiple_roi_probtrackx(list_of_masks,bedpostx_folders,output_name):
    for counter,file in enumerate(bedpostx_folders):
        print(file)
        os.chdir(file)
        masks = list_of_masks[counter]
        with open(output_name + '_masks.txt', 'w') as filehandle:
            for listitem in masks:
                filehandle.write('%s\n' % listitem)
        cmd = 'probtrackx2 --network -x ' + output_name + '_masks.txt -l --onewaycondition -c 0.2 -S 2000 --steplength=0.2 -P 5000 --fibthresh=0.01 --distthresh=0.0 --sampvox=0.0 --forcedir --pd --opd -s merged -m nodif_brain_mask --dir=' + output_name
        print(cmd)
        os.system(cmd)
        
run_multiple_roi_probtrackx(list_of_masks,bedpostx_folders,output_name)


# In[ ]:




