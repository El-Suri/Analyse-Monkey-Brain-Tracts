#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import glob


# In[8]:


# Collect all saved tracts using glob search
# deterministic path = '/cubric/data/c1639425/Monkey_Brains/derivatives/sub-0*/dwi/ncc_results/*ncc_Tract_mask.nii'
#probabilistic path = '/cubric/data/c1639425/Monkey_Brains/derivatives/sub-0*/dwi/probabilistic.bedpostX/prob_tract_single_mask_subic/fdt_paths.nii.gz'
saved_tracts = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-0*/dwi/ncc_results/*ncc_Tract_mask.nii'))
print(saved_tracts)
print(len(saved_tracts))


# In[9]:


# Binarise tracts
for subject in saved_tracts:
    cmd = 'fslmaths ' + subject + ' -bin ' + subject[0:-4] + '_bin'
    print(cmd)
    os.system(cmd)

    
    
# Collect results (double check, esp if you have just changed inputs)
bin_tracts = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub-0*/dwi/ncc_results/*_Tract_mask_bin.nii.gz'))
#print(bin_tracts)
print(len(bin_tracts))


# In[12]:


# Warp tracts to atlas space using inverse of atlas b0 to native b0 transformation

# Collect atlas b0 transformations
transformation_matrices = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_b0_atlas.mat'))
#print(transformation_matrices)

ref_atlas_image = '/cubric/data/c1639425/Monkey_Brains/atlas/civm_rhesus_v1_b0.nii.gz'

#Invert transformation matrices
for transform in transformation_matrices:
    cmd = 'convert_xfm -omat ' + transform[0:-4] + '_inverse.mat' + ' -inverse ' + transform
    print(cmd)
    os.system(cmd)


# Collect inverted transforms 
inverse_transformation_matrices = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_b0_atlas_inverse.mat'))
print(len(inverse_transformation_matrices))

# Perform the native to atlas transformations
for tract, transform in zip(bin_tracts,inverse_transformation_matrices):
    cmd = 'flirt -in ' + tract + ' -ref ' + ref_atlas_image + ' -out ' + tract[0:-7] + '_atlas_space' + ' -applyxfm -init ' + transform
    print(cmd)
    os.system(cmd)


# In[13]:


# Add masks together (8 masks)

atlas_space_tracts = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/ncc_results/*_Tract_mask_bin_atlas_space.nii.gz'))

cmd = 'fslmaths ' + atlas_space_tracts[0] + ' -add ' + atlas_space_tracts[1] + ' -add ' + atlas_space_tracts[2] + ' -add ' + atlas_space_tracts[3] + ' -add ' + atlas_space_tracts[4] + ' -add ' + atlas_space_tracts[5] + ' -add ' + atlas_space_tracts[6] + ' -add ' + atlas_space_tracts[7] + ' /cubric/data/c1639425/Monkey_Brains/probability_mask_subic_ncc'

print(cmd)
os.system(cmd)


# In[24]:


# Add masks together (9 masks)

atlas_space_tracts = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_Tract_mask_bin_atlas_space.nii.gz'))

cmd = 'fslmaths ' + atlas_space_tracts[0] + ' -add ' + atlas_space_tracts[1] + ' -add ' + atlas_space_tracts[2] + ' -add ' + atlas_space_tracts[3] + ' -add ' + atlas_space_tracts[4] + ' -add ' + atlas_space_tracts[5] + ' -add ' + atlas_space_tracts[6] + ' -add ' + atlas_space_tracts[7] + ' -add ' + atlas_space_tracts[8] + ' /cubric/data/c1639425/Monkey_Brains/probability_mask'

print(cmd)
os.system(cmd)


# In[ ]:




