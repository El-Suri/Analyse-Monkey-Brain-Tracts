#!/usr/bin/env python
# coding: utf-8

# # Extract ROI from atlas

# In[ ]:


import argparse
import glob
import os

def cmd_line_args():
    parser = argparse.ArgumentParser(description='Extract the ROI from your monkey brains using the appropriate ROI reference number')
    # Add a mutually exclusive group, either path to a file, a list of files, or a glob search string can be provided.
    input_file_specifier = parser.add_mutually_exclusive_group(required=True)
    input_file_specifier.add_argument('-f','--file', type=str,help='Provide the path to an atlas label image that has been warped to native space')
    input_file_specifier.add_argument('-l','--list', type=str, help='Provide the path to a file that contains a list of each warped atlas label image for every monkey you wish to extact from, with each line containing a path for each subject. e.g /my/path/sub-1/dwi/my_file *newline* /my/path/sub-2/dwi/my_file')
    input_file_specifier.add_argument('-g','--glob',type = str, help='Provide a search string that will find all warped atlas label images you wish to extract from. * wildcards are allowed, google \'glob python\' for information on how to format your search strings. A typical example would be: \"/my/path/sub-*/dwi/*registered_labels.nii.gz\". Note - search string MUST be placed between \"\"')
    parser.add_argument("-r","--roi", type=int, required = True, help="Provide an integer that specifies the ROI you wish to extract. A list of ROIs and their respective integers can be found in the document \'atlas_labels.txt'")
    parser.add_argument("-o","--output",type=str, required = True, help="Required, specify mask output name.")

    
    args = parser.parse_args()
    
    print(' ')
    
    if args.file is not None:
        list_of_files = args.file
    elif args.list is not None:
        import csv
        list_of_files = []
        with open(args.list, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                list_of_files.append(row)
    else:
        list_of_files = sorted(glob.glob(args.glob))
    
    
    print('Selected files are: ' + str(list_of_files))
    print(' ')
    
    return(args,list_of_files,args.roi,args.output)



def extract_roi(args,list_of_files,roi,output):
    print('Performing ROI extraction...')
    print(' ')
    roi = str(roi)
    if args.file:
        cmd = 'fslmaths ' + list_of_files + ' -thr ' + roi + ' -uthr ' + roi + ' -bin ' + list_of_files[0:-8] + output
        print(cmd)
        os.system(cmd)
        unzip = 'gunzip ' + list_of_files[0:-8] + output + '.nii.gz'
        os.system(unzip)
    elif args.list:
        for counter, ignore in enumerate(list_of_files):
            file = str(list_of_files[counter][0])
            cmd = 'fslmaths ' + file + ' -thr ' + roi + ' -uthr ' + roi + ' -bin ' + file[0:-7] + output 
            print(cmd)
            os.system(cmd)
            unzip = 'gunzip ' + file[0:-7] + output + '.nii.gz'
            os.system(unzip)
    else:
        for file in list_of_files:
            cmd = 'fslmaths ' + file + ' -thr ' + roi + ' -uthr ' + roi + ' -bin ' + file[0:-7] + output 
            print(cmd)
            os.system(cmd)
            unzip = 'gunzip ' + file[0:-7] + output + '.nii.gz'
            os.system(unzip)
    print(' ')
    print('Completed')

    
if __name__ == "__main__":
    args,list_of_files,roi,output = cmd_line_args()
    extract_roi(args,list_of_files,roi,output)

