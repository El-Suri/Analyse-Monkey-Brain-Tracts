# Analyse Monkey Brain Tracts
Notebooks and scripts for the tractography analysis of the BST - Subiculum in monkey MRI data.

This repository should serve as a record for how to use non-human primate MRI images to analyse structural connections between regions using the (insert name of atlas) atlas. 

### Dataset information

9 Non-human primates (insert species here) were downloaded from the (insert repo)

The dataset includes:

* T1w 7T structural images (input acqusition info)
* Diffusion weighted images (insert aqusition info)

The atlas was generated using data from * and was downloaded from **

### First steps - get images ready for the ExploreDTI software

The images come pre-processed (see above for info), however there are a few more steps before they are ready for ExploreDTI - the software we are using to analyse the tracts. The code to complete the steps below is contained in the notebook "Prepare_brains_for_ExploreDTI.ipynb"

1. Extract a b0 (no diffusion) image from the DWI data using fslroi 
2. Run brain extraction on the extracted B0 images using FSL BET, using the -m option to save a binary mask
3. Multiply the binary masks with the DWI images using fslmaths to remove the skull

There are two b0s in the DWI data. For ExploreDTI to work they both need to be at the front, which is not the case. Therefore, the below steps deal with this issue.

4. Change the bvec and bval files so that the data associated with the b0 images is at the front. The b0 images can be found where the bval file has values of 0. This index position is used to move the appropriate data from the 3 dimensions of the bvec files to the front. (This is done in the notebook)
5. Open ExploreDTI and use the ExploreDTI plugin ‘Shuffle/select 3D volume(s) in 4D *.nii file(s)’ to reorder the b0 images to the beginning. All the b0 images are in the same place for every monkey, so you can use the sequence: 1 66 2:65 67:130 for all. 
6. Now use the ExploreDTI plugin ‘Convert …*.bval/*.bvec to B-matrix *.txt file(s)’, to generate a bmatrix based on the bval and bvec files.
7. Use the ExploreDTI plugin “Flip/permute dimensions in 3D/4D *.nii file(s)”, to make the images ExploreDTI friendly and avoid problems with flipping of axes. 
8. Use the 'Convert raw data to DTI *.mat' tool to convert the nifti image and corresponding bmatrix to a dti .mat file. There are a number of parameters to set here. The image labeled DTI-to-mat.img contains some appropriate default parameters.

Your images are now ready for the next step, which is to register the Atlas to each individual monkeys brain.




