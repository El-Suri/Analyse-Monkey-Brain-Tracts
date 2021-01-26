#!/usr/bin/env python
# coding: utf-8

# # This script will register the atlas to monkey brain native space. 

# In[1]:


import os
import numpy as np
import pandas as pd
import glob


# subj_folders and subj_ids needs to be a list of the folders of each subjects where your b0 images are, and a list of the subject names. The folders and subject names lists should match exactly in terms of their order. E.g. subj_folders[0] = /my/folder/subj-01 and subj_names[0] = subj-01. Glob.glob is a great tool that searches for specified file names and puts them into a list.

# In[31]:


atlas_labels = '/cubric/data/c1639425/Monkey_Brains/atlas/civm_rhesus_v1_labels.nii.gz'
subj_folders = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/'))
subj_ids = [x[48:54] for x in subj_folders] # Change this to 'catch' the subject IDs. Check by printing below.
print(subj_ids)
# print(subj_folders)


# In[4]:


# Extract B0's from the pre-processed ExploreDTI-ready dwi data
def extract_b0(subj_folders,subj_ids,file_extension):
    for path,subj in zip(subj_folders,subj_ids):
        print(path,subj)
        cmd = 'fslroi ' + path + subj + file_extension + ' ' + path + subj + '_dwi_bet_shuffled_FP_b0.nii.gz 0 1'
        print(cmd)
        os.system(cmd)
    

file_extension = '_dwi_bet_shuffled_FP.nii' # this is the default file extension after you have got the data ready for tractography via Explore DTI
extract_b0(subj_folders,subj_ids,file_extension)


# ## Register the B0 of the atlas to the ExploreDTI-ready monkey b0 you just extracted. b0_monkey_images is an ordered list of all the b0 monkey brains you just extracted.

# In[25]:


b0_atlas_image = '/cubric/data/c1639425/Monkey_Brains/atlas/civm_rhesus_v1_b0.nii.gz'
print(b0_atlas_image)
b0_monkey_images = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_dwi_bet_shuffled_FP_b0.nii.gz'))
print(b0_monkey_images)


# In[38]:


def flirt_b0_atlas_b0_monkey(subj_folders,subj_ids,b0_monkey_images,b0_atlas_image):
    for subj_folder,subj,b0_monkey in zip(subj_folders,subj_ids,b0_monkey_images):
        print(subj)
        cmd = 'flirt -in ' + b0_atlas_image + ' -ref ' + b0_monkey + ' -out ' + subj_folder + subj + '_b0_atlas_flirt ' + '-omat ' + subj_folder + subj + '_b0_atlas.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp nearestneighbour'
        print(cmd)
        os.system(cmd)
        
flirt_b0_atlas_b0_monkey(subj_folders,subj_ids,b0_monkey_images,b0_atlas_image)


# # Apply the transformation matrix to atlas labels
# 
# The transformation of the atlas b0 image to the monkey specific b0 image will have produced a transformation matrix. Use this matrix to take the atlas labels image (the one where all the regions are labelled) to the monkey specific (native) space. 

# In[39]:


# Collect atlas b0 transformations
transformation_matrices = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_b0_atlas.mat*'))

print(transformation_matrices)


# In[42]:


def apply_transform_to_atlas(b0_monkey_images,atlas_labels,transformation_matrices,subj_ids,subj_folders):
    for b0_monkey_image, transformation, subj, subj_folder in zip(b0_monkey_images, transformation_matrices, subj_ids, subj_folders):
        print(subj)
        cmd = 'flirt -in ' + atlas_labels + ' -ref ' + b0_monkey_image + ' -out ' + subj_folder + subj + '_registered_labels -applyxfm -init ' + transformation +         ' -interp nearestneighbour'
        print(cmd)
        os.system(cmd)
        
apply_transform_to_atlas(b0_monkey_images,atlas_labels,transformation_matrices,subj_ids,subj_folders)


# ## Final prep stages
# 
# You need to inspect each of the images to make sure the transformation of the atlas to the brain has worked well. Following this, you can then extract masks of the regions of interest for further analysis. This will be done using the command-line script 'extract_ROI.py'.

# In[ ]:




