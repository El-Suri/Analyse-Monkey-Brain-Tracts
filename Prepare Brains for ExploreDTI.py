#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
import pandas as pd
import glob
import numpy as np


# ## Gather subjects files and IDs

# In[18]:


paths = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/'))
subject_ids = [x[48:54] for x in paths] 
print(subject_ids)
print(paths)


# ## Extract the b0
# 
# This can be done in a loop for all monkeys

# In[24]:


for path,subj in zip(paths,subject_ids):
    #print(path,subj)
    cmd = 'fslroi ' + path + subj + '_space-subject_desc-eddy_dwi.nii.gz ' +  path + subj + '_dwi_nodif.nii.gz 0 1'
    print(cmd)
    os.system(cmd)
    
    


# ## Skull Strip
# 
# It's important to visually inspect these results, especially as you only have 9 monkeys. If there are problems find the center cords and alter the F value. As such this is probably best done at the command line, but here is a loop example with 'standard' settings anyway. You can perform this and then adjust as appropriate.  

# In[27]:


#cmd_bet = 'bet /cubric/data/c1639425/Monkey_Brains/derivatives/sub-03/dwi/dwi_nodif.nii.gz /cubric/data/c1639425/Monkey_Brains/derivatives/sub-03/dwi/dwi_nodif_bet.nii.gz -c 62 62 20 -f 0.37 -m'

for path,subj in zip(paths,subject_ids):
    cmd = 'bet ' + path + subj + '_dwi_nodif.nii.gz ' +  path + subj + '_dwi_nodif_bet.nii.gz -m'
    print(cmd)
    os.system(cmd)


# Final parameters used for BET for each participant:
#     
#     sub 1 = bet sub-01_dwi_nodif.nii.gz sub-01_dwi_nodif_bet.nii.gz -c 63 61 23 -f 0.37 -m
#     sub 2 = bet sub-02_dwi_nodif.nii.gz sub-02_dwi_nodif_bet.nii.gz -c 65 59 24 -f 0.37 -m # maybe part of frontal lobe should be included
#     sub 3 = bet sub-03_dwi_nodif.nii.gz sub-03_dwi_nodif_bet.nii.gz -c 62 62 20 -f 0.37 -m 
#     sub 4 = bet sub-04_dwi_nodif.nii.gz sub-04_dwi_nodif_bet.nii.gz -c 52 52 19 -f 0.32 -m
#     sub 5 = bet sub-05_dwi_nodif.nii.gz sub-05_dwi_nodif_bet.nii.gz -c 54 52 23 -f 0.35 -m # Missing part of front right
#     sub 6 = bet sub-06_dwi_nodif.nii.gz sub-06_dwi_nodif_bet.nii.gz -c 51 50 22 -f 0.37 -m
#     sub 7 = bet sub-07_dwi_nodif.nii.gz sub-07_dwi_nodif_bet.nii.gz -c 52 53 20 -f 0.37 -m * check with Marc - same part of the brain (bottom, middle left)
#     sub 8 =  bet sub-08_dwi_nodif.nii.gz sub-08_dwi_nodif_bet.nii.gz -c 54 46 19 -f 0.37 -m * check with Marc
#     sub 9 = bet sub-09_dwi_nodif.nii.gz sub-09_dwi_nodif_bet.nii.gz -c 52 49 20 -f 0.39 -m
# 
#     

# ### Multiply the binary mask with the dataset to obtain your skullstripped dwi data
# 
# <fslmaths dwi_nodif_bet_mask.nii.gz -mul dwi.nii.gz dwi _bet.nii.gz>

# In[2]:


for path,subj in zip(paths,subject_ids):
    cmd_strip = 'fslmaths ' + path + subj + '_dwi_nodif_bet_mask.nii.gz -mul ' + path + subj + '_space-subject_desc-eddy_dwi.nii.gz ' + path + subj + '_dwi_bet.nii.gz' 
    print(cmd_strip)
    os.system(cmd_strip)


# ## Reorder bvec and bval files
# 
# For further analysis the b0 images need to be at the beginning. You can change the order of the images using Explore DTI, but you must also change the bval and bvec files. Below, the code loads in the bval files, finds where the 0 values are, and then moves the b0 data from both bval and bvec files to the beginning. 

# ## Define the function that moves items in a list around.
# 
# If you want to make this better you can let it takes multiple original and final indexes. Don't really need it here as there are only two values to change for each subject. if you have more though it means a seperate call to 'move' each tim you want to move something, which can get messy. 
# 

# In[261]:


def move(a_list, original_index, final_index):
    a_list.insert(final_index, a_list.pop(original_index))
    return a_list
    


# ## Re-arrange bval and bvec files
# 
# This function takes in a list of bvec and bval files, finds where the 0 values are in the bval file, and uses the index position to move bval and associated bvec values to the front. This makes it ready for Explore DTI, which expects b0's at the front. This currently only works if there are two b0 values.

# In[277]:


def reorder_bvals_bvecs(paths, bval_files,bvec_files):
    for path, bval_file, bvec_file in zip(paths,bval_files,bvec_files):
        ## Import bval_file as np array, find 0 values, and save index positions
        print('Processing ' + bval_file)
        print(path)
        bval = np.loadtxt(bval_file)
        #print(bval[0])
        zeros = np.where(bval == 0)
        print('B0\'s are located at :')
        print(zeros)
        bval_list = list(bval)
        #print(bval_list)
        print('Moving bval 0\'s to front of file')
        move(bval_list,zeros[0][0],0)
        move(bval_list,zeros[0][1],1)
        #add another 'move' here if you have more than one b0, so it would look like move(bval_list,zeros[0][2],2)
        #print(bval_list) 
        bval_df = pd.DataFrame(bval_list)
        bval_transposed = bval_df.T
        #bval_df.loc[0] = bval_list
        #print(bval_transposed)
        bval_transposed.to_csv(path + 'space-subject_desc-eddy_dwi_updated.bval', index =False, header = None, sep = ' ')
        print('')
        print('Processing' + bvec_file)
        df = pd.read_csv(bvec_file, header = None, sep = ' ')
        #put each dimension into its own list
        dim1 = df.loc[0].tolist()
        dim2 = df.loc[1].tolist()
        dim3 = df.loc[2].tolist()
        #print(dim1)
        #print(dim2)
        #print(dim3)
        ## Run function that moves the values around.
        print('Moving bvec b0 values to the front for each dimension')
        move(dim1,zeros[0][0],0)
        move(dim2,zeros[0][0],0)
        move(dim3,zeros[0][0],0)
        move(dim1,zeros[0][1],1)
        move(dim2,zeros[0][1],1)
        move(dim3,zeros[0][1],1)
        #print(dim1)
        #print(dim2)
        #print(dim3)
        #print('Saving new bvec file')
        #write_bvec_files(path,dim1,dim2,dim3)
        print('Done')
        print('')
        df.loc[0] = dim1
        df.loc[1] = dim2
        df.loc[2] = dim3
        df.to_csv(path + 'space-subject_desc-eddy_dwi_updated.bvec',header = None,sep = ' ', index = False)
        

bval_files = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_space-subject_desc-eddy_dwi.bval'))
#print(bval_files)
bvec_files = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/*_space-subject_desc-eddy_dwi.bvec'))
#print(bvec_files)
paths = sorted(glob.glob('/cubric/data/c1639425/Monkey_Brains/derivatives/*/dwi/'))
#print(paths)
reorder_bvals_bvecs(paths,bval_files,bvec_files)


# Next, go into ExploreDTI and do the following:
# 
# 6) Now use the ExploreDTI plugin ‘Convert …*.bval/*.bvec to B-matrix *.txt file(s)’, to generate a bmatrix based on the bval and bvec files
# 
# 7) As well as all the above, I would recommend that at some point prior to generating the .mat file in subsequent steps, you also use the ExploreDTI plugin “Flip/permute dimensions in 3D/4D *.nii file(s)”, to make the images ExploreDTI friendly and avoid problems with flipping of axes. 
# 
# 8) Use the 'Convert raw data to DTI *.mat' tool to convert the nifti image and corresponding bmatrix to a dti .mat file. I will need to check that the acquisition protocol was consistent across the monkey species/subjects, but the parameters I used just now which worked fine for subject 1 were:
# 
# 
# 
# Note: I set Background masking to None whereas the default is automatic. You can try automatic if you like, without performing the various bet and fslmaths steps above that are done for masking/skull-stripping. Whichever route you go though, you will need a no_dif image for DWI-to-T1 registration (and more importantly the inverse transform for taking T1-derived region labels from T1 to native diffusion space). Linear is also the least fancy ‘Diffusion tensor estimation’ setting – I’ve used it here just for speed of testing. You can set it to non-linear or summat if you like but I wouldn’t worry about it for an initial test run.
# 

# In[ ]:




