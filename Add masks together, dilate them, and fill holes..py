#!/usr/bin/env python
# coding: utf-8

# ## Add masks together, dilate them, and fill holes.

# In[1]:


import os
import glob


# Add all subiculum masks together 

# In[19]:


subic_masks = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labels_subiculum.nii'))
para_subic = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labelsparasubic.nii'))
pre_subic = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labelspresubic.nii'))
pro_subic = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labelsprosubic.nii'))


# In[24]:


print(subic_masks[0][0:-4])


# In[31]:


for i in range(len(subic_masks)):
    cmd = 'fslmaths ' + subic_masks[i] + ' -add ' + para_subic[i] + ' -add ' + pre_subic[i] + ' -add ' + pro_subic[i] + ' ' + subic_masks[i][0:-4] + '_all'
    print(cmd)
    os.system(cmd)
    unzip = 'gunzip ' + subic_masks[i][0:-4] + '_all.nii.gz'
    os.system(unzip)


# In[ ]:


# Add nucleus accumbens masks together


# In[5]:


accumb_core = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labels_accumbcore.nii'))
accum_shell = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labels_accumbshell.nii'))
accum_nuc = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/*_registered_labels_accumb_nuc.nii'))

print(accumb_core)
print(accum_shell)
print(accum_nuc)


# In[6]:


for i in range(len(accumb_core)):
    cmd = 'fslmaths ' + accumb_core[i] + ' -add ' + accum_shell[i] + ' -add ' + accum_nuc[i] + ' ' + accumb_core[i][0:-4] + '_all_accum_nuc'
    print(cmd)
    os.system(cmd)
    unzip = 'gunzip ' + accumb_core[i][0:-4] + '_all_accum_nuc.nii.gz'
    os.system(unzip)


# ## Add anterior thalamus masks together

# In[2]:


anteromedial = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/ROIS/*_registered_labels_anteromedial_thalamic.nii'))
anteroventral = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/sub*/dwi/ROIS/*_registered_labels_anteroventral_thalamic.nii'))

print(anteromedial)
print(anteroventral)


# In[3]:


for i in range(len(anteromedial)):
    cmd = 'fslmaths ' + anteromedial[i] + ' -add ' + anteroventral[i] + ' ' + anteromedial[i][0:-4] + '_all_anterior_thalamic'
    print(cmd)
    os.system(cmd)
    unzip = 'gunzip ' + anteromedial[i][0:-4] + '_all_anterior_thalamic.nii.gz'
    os.system(unzip)


# Fill any holes in masks (didn't work how I wanted it to)

# In[ ]:


for mask in subic_masks:
    cmd = 'fslmaths ' + mask + ' -kernel 3D -dilM ' + mask[0:-4] + '_dilated'
    print(cmd)
    os.system(cmd)
    rm = 'rm ' + mask[0:-4] + '_dilated.nii'
    unzip = 'gunzip ' + mask[0:-4] + '_dilated.nii.gz'
    #os.system(rm)
    print(unzip)
    os.system(unzip)


# Expand (dilate) masks (made masks too big and caused huge amount of implausible streamlines)

# In[13]:


for mask in subic_masks:
    cmd = 'fslmaths ' + mask + ' -kernel 3D -dilM ' + mask[0:-4] + '_dilated'
    print(cmd)
    os.system(cmd)
    rm = 'rm ' + mask[0:-4] + '_dilated.nii'
    unzip = 'gunzip ' + mask[0:-4] + '_dilated.nii.gz'
    #os.system(rm)
    print(unzip)
    os.system(unzip)


# In[ ]:




