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

### Second step - register Atlas to Monkey space

The code to run these steps, as well as more precise infomation and parameters are located in the script/ notebook called 'Register Atlas to Monkey Native Space'

1. Extract the b0's from your ExploreDTI-ready DWI images.
2. Flirt the Atlas b0's to your individual monkeys b0's that you just extracted. Use the -omat flat to save the transformation matrix.
3. Flirt the transformation matrix from the last stage to move the Atlas labels image to each individual monkeys space. 
4. Manually check your images to make sure that the atlas labels are where they should be. 

### Third step - extract your ROIs

The code for extracting ROIs for one, or all, of your subjects is in the script 'extract_ROIs.py'. This can be run directly from the command line. A guide to using this script will be placed below. Help can also be accessed by using the -h or -help flag. 

*What does the script do?*

* Briefly, you give the script the directories of the subjects you want to extract from, the full paths to native-space registered Atlas labels images  , a digit that correspondes to the ROI you want to extract (e.g 3), 
1. 

