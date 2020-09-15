# Analyse Monkey Brain Tracts

Notebooks and scripts for the tractography analysis of monkey MRI data.

This repository should serve as a record and guide for how to use non-human primate MRI images to analyse structural connections between regions using the (insert name of atlas) atlas. Created by Sam Berry and Dr. Mark Postans at Cardiff University. 

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
8. Use the 'Convert raw data to DTI *.mat' tool to convert the nifti image and corresponding bmatrix to a dti .mat file. There are a number of parameters to set here. The image labeled DTI-to-mat.img contains some appropriate default parameters. Double check these images by clicking Data/load_dti.mat in ExploreDTI.

Your images are now ready for the next step, which is to register the Atlas to each individual monkeys brain.

### Second step - register Atlas to Monkey space

The code to run these steps, as well as more precise infomation and parameters are located in the script/ notebook called 'Register Atlas to Monkey Native Space'

1. Extract the b0's from your ExploreDTI-ready DWI images.
2. Flirt the Atlas b0's to your individual monkeys b0's that you just extracted. Use the -omat flat to save the transformation matrix.
3. Flirt the transformation matrix from the last stage to move the Atlas labels image to each individual monkeys space. 
4. Manually check your images to make sure that the atlas labels are where they should be. 

### Third step - extract your ROIs

The code for extracting ROIs for one, or all, of your subjects is in the script 'extract_ROIs.py'. A short guide on how to run it can be accessed directly from the command line by typing <python3 extract_ROIs.py -h>

*Briefly, what does the script do?*

Give the script the path to the files of the subject-space Atlases, a digit that correspondes to the ROI you want to extract (e.g 3), and an output name to idnetify your extracted region (e.g Hippocampus), and it will extract the ROI and place a binary .nii mask back into the respective subj folder. You can provide a path to a single file, a .txt list of files with each path on a new line, or a glob search string to find all relevent files. Check the flags and appropriate input format using the -h or -help flag. 

The digits that correspond to the appropriate ROI's are listed in the file 'atlas/atlas_labels.txt'.


### Fourth step - run the tractography.

Once you have extracted the appropriate ROI's, you can open matlab and run the script 'tractography_through_masks'. A GUI will pop-up and you will be asked to select the .mat DWI file, two masks to track through, and an optional NOT mask. You will then be asked to provide some parameters, some decent starting default options are provided in the image 'tractography_params.png'. Once completed, you can load these tracts in ExploreDTI by clicking Data/ Load fiber tracts, then opening Palette/ Draw and then clicking 'Analyse Tracts' and finally 'Draw Tracts'. More information on ExploreDTI can be found in the manual, located [here](http://www.exploredti.com/manual/Manual_ExploreDTI.pdf). 
