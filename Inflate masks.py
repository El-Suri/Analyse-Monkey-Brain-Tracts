#!/usr/bin/env python
# coding: utf-8

# ## Add masks together, dilate them, and fill holes.

# In[2]:


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




