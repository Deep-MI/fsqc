# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:43:45 2019

@author: Tobias Wolff
Purpose of this function:
1) This function computes the mean volumes for all segmentations of the indicated subjects. 
2) Then the function checks if every segemntation volume is within the mean value and two times the standard deviation of this specific segmentation. 
3) If this is not the case, there is an output on the screen

4) The default is that the function computes the mean segmentation volumes on its own. Another way to get the mean values is to extract them from a table. 
The path to this table must be given by the user. The file has to be named mean_file and must be at the location of the subjects_directory /subjects_dir/mean_file

Required arguments:
    - subjects_dir: Path to the directory where the subjects are located
    - subjects: The ID of the subjects
    - recon_checker_scripts: Path to the recon chekcer scripts, in order to find the seg2file
    - path_data_file: The path to the csv file, where all the other information is stored. 
    
Optional arguments:  
    - print_Means_to_file: Option explained in step 4 
    - Look_up_means_from_file: Path to the files, where they are located
    
What needs to be done: 
    - Report_only flag: Specifies only the number of outliers
"""
import csv
from datetime import datetime
from g_parc_mean_norm import g_parc_mean_norm
from g_parc_val_norm import g_parc_val_norm
from read_parc_mean_from_table import read_parc_mean_from_table

def recon_all_aseg_outlier_checker(subjects_dir, subjects, recon_checker_scripts, path_data_file, print_means_to_file = 0, look_up_means_from_file = 0):
    path_mean_file = str(subjects_dir) + "mean_file"     
    
    path_segs_file2 = str(recon_checker_scripts) + "/" + "segsfile2" 
    list_of_means = []    
    list_of_parc_val = []
    nb_outliers = 0
    first_call_write_file = 1

    
    # This step is required in order to extract all the possible segementations 
    print("The path to the segsfile is", path_segs_file2)    
    try:
        with open(path_segs_file2) as segs_file:
            segmentations = segs_file.read().splitlines()
    except FileNotFoundError:
            print("The path",path_segs_file2, "does not have an appropriate file")
    
    for segmentation in segmentations:
        #Look out for the mean values for all the segmentations over all subjects, or compute them 
        if look_up_means_from_file:
                list_segmentation = [str(segmentation)]
                look_up_mean_file = str(subjects_dir) + "mean_file"
                list_of_means = read_parc_mean_from_table(list_segmentation, look_up_mean_file )                
        else:
            list_segmentation = [str(segmentation)]
            list_of_means = g_parc_mean_norm(subjects_dir, subjects, list_segmentation)
        # the actual output of the g_parc_mean_norm function is .. +/- .. 
        # where the first value is the mean value and the second one the standard deviation
        
        means = list_of_means[0]
        stds = list_of_means[2]
        
        # If the volume is not found, then just continue with the next iteration 
        if means == "." :
            continue
        
        # If the user want to have a specific file with the means and standard deviations:                                         
        if print_means_to_file:
            if first_call_write_file == 1:
                try: 
                    with open(path_mean_file, 'w') as f:
                        f.write("{0}: {1} {2} {3} {4}".format(segmentation, means, "+/-", stds, "\n"))
                        first_call_write_file+=1
                except: 
                    print("Impossible to write the mean values into a file, located at the subjects directory")
            else:
                try: 
                    with open(path_mean_file, 'a') as f:
                        f.write("{0}: {1} {2} {3} {4}".format(segmentation, means, "+/-", stds, "\n"))
                except: 
                    print("Impossible to write the mean values into a file, located at the subjects directory")
                    
        # Now test every segmentations of every subject against the means and standard deviations
        for subject in subjects: 
            list_segmentation = [str(segmentation)]
            list_subject = [str(subject)]
            
            # Get the actual value of the segmentation volume
            list_of_parc_val = g_parc_val_norm(subjects_dir, list_subject, list_segmentation)
            
            #Upper Limit
            if float(list_of_parc_val [0]) < float(means) - 2*float(stds):
                print("The subject", subject, "at the segmentation", segmentation, "is an outlier")
                #with open(path_log_file, 'a') as logfile:
                       #logfile.write("The subject {0} at the segmentation {1} is an outlier \n".format(subject, segmentation))
                nb_outliers +=1
            
                with open(path_data_file,'r') as csvinput:
                    reader= csv.reader(csvinput)
                    reader = list(reader)
                for index, row in enumerate(reader[1:]):
                    if subject in row:
                        try: 
                            nb_outlier_sub = int(row[15])
                            nb_outlier_sub += 1
                            new_segs = row[16] + " " + str(segmentation)
                            row[15] = nb_outlier_sub
                            row[16] = new_segs
                        except: 
                            nb_outlier_sub = 1
                            new_segs = segmentation
                            row.append(nb_outlier_sub)
                            row.append(new_segs)
                        with open(path_data_file,'w') as csvoutput:
                            writer = csv.writer(csvoutput)
                            writer.writerows(reader) 

            #Lower Limit
            elif float(list_of_parc_val [0]) > float(means) + 2*float(stds):
                print("The subject", subject, "at the segmentation", segmentation, "is an outlier")
                nb_outliers +=1
                with open(path_data_file,'r') as csvinput:
                    reader= csv.reader(csvinput)
                    reader = list(reader)
                for index, row in enumerate(reader[1:]):
                    if subject in row:
                        try: 
                            nb_outlier_sub = int(row[15])
                            nb_outlier_sub += 1
                            new_segs = row[16]
                            new_segs = row[16] + " " + str(segmentation)
                            row[15] = nb_outlier_sub
                            row[16] = new_segs
                        except: 
                            nb_outlier_sub = 1
                            new_segs = segmentation
                            row.append(nb_outlier_sub)
                            row.append(new_segs)
                        with open(path_data_file,'w') as csvoutput:
                            writer = csv.writer(csvoutput)
                            writer.writerows(reader)                      
    
    print(nb_outliers,"outlier(s) have been found")
