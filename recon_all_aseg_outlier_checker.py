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
    - path_data_file: The path to the csv file, where all the other information is stored.
    - path_mean_file: The path to the csv file, where all the means are stored.  
    
Optional arguments:  
    - Look_up_mean_file: Path to the files, where they are located; default: None
    
What needs to be done: 
    - Report_only flag: Specifies only the number of outliers
"""

# ------------------------------------------------------------------------------
# subfunctions

def g_parc_mean_norm(subjects_dir, subjects, segmentations):

    """
    Created on Wed May 15 17:00:06 2019

    @author:Tobias Wolff
    This function takes some subjets and segmentations as input and computes the mean and the standart deviation of all the segementations.
    Required arguments:
        - Subjects directory
        - Subjects
        - Segmentations

    """

    import os 

    from statistics import mean, stdev

    region_vol = []
    Vol_elements= []
    aseg_stat= []
    Mean_volume = 0
    Std_volume = 0
    inter_cranial_volume = 0

    for subject in subjects:
        
        #Get the individual path to the aseg.stat file and open it 
        path_stats_file = os.path.join(subjects_dir,subject,"stats","aseg.stats")
        with open(path_stats_file) as stats_file:
            aseg_stat = stats_file.read().splitlines()
        
        for segmentation in segmentations:            
            for aseg_stat_line in aseg_stat:
                # If the name of the segmentation is present in the aseg.stat file, then grep its volume value.
                # In the next step, norm the value with the total intercranial volume. 
                if segmentation in aseg_stat_line:
                    region_vol.append([segmentation, (float(aseg_stat_line.split()[3])/float(inter_cranial_volume))*100])
                if 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                     inter_cranial_volume= aseg_stat_line.split(',')[3]
    
    # Get only the values of the normed volumes and do not care about their names                
    for i in range(len(region_vol)):
      Vol_elements.append(region_vol[i][1])
    
    # Calculate the mean and the standart deviation and return the value
    if len(Vol_elements)== 0:
        Mean_volume = "."
        Std_volume = "."
    elif len(Vol_elements) == 1:        
        Mean_volume = Vol_elements
        Std_volume = "."

    elif len(Vol_elements) > 1:
        Std_volume = stdev(Vol_elements)
        Mean_volume = mean(Vol_elements)
    else:
        Std_volume=0
        Mean_volume =0

    return  [Mean_volume , Std_volume]


def g_parc_val_norm(subjects_dir, subjects, segmentations):

    """
    Created on Thu May 16 12:30:12 2019

    @author: Tobias Wolff
    This function returns the relativ value of the volume of one subject of one segmentation. 
    The function could return more values, but it is called within a loop, that treats all subjects and all segmentations. 

    Required arguments:
        - Subjects directory
        - The subject
        - Segmentation
    """

    import os

    segmentation_vol = []
    Vol_norm = []
    inter_cranial_volume = 0
    
    for subject in subjects:

        #Open the specific aseg.stats file of one subject.
        path_stats_file = os.path.join(subjects_dir,subject,"stats","aseg.stats")

        with open(path_stats_file) as stats_file:
            aseg_stat = stats_file.read().splitlines()
        
        # Then, get the volume values of the required segmentations and norm them. 
        # Highly important that the aseg.stat file first gives the information about the inter_cranial volume and then the information about the 
        for segmentation in segmentations:
            for aseg_stat_line in aseg_stat:
                if segmentation in aseg_stat_line:
                    segmentation_vol.append([segmentation, (float(aseg_stat_line.split()[3])/float(inter_cranial_volume))*100])
                if 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                     inter_cranial_volume = aseg_stat_line.split(',')[3]

    # Get only the volumes, and do not care anymore of their name. 
    for each_vol in range(len(segmentation_vol)):
         Vol_norm.append([segmentation_vol[each_vol][0], segmentation_vol[each_vol][1]])

    return [i[1] for i in Vol_norm]


def read_parc_mean_from_table(segmentations, look_up_mean_file):

    """
    Created on Wed May 15 15:06:56 2019
    @author:Tobias Wolff

    This function looks out for the mean values of the segmentations in a passed file. 
    This file must be located in the subjects directory. 
    Required Arguments:
        - At least one segmentation
        - The path to the mean_file
    Return Value:
        - The mean values extracted extracted either from the defaultAsegMeans.txt file,
        or from the user specified file in a list
    """

    #segmentation: List with the segmentation
    means_from_file = []
    try:
        with open(look_up_mean_file) as f:
            lines_aseg_means_file = f.read().splitlines()
    except IOError:
        print('Impossible to open the Look up means file, please verify path or existence')
        exit()
        
    #Loop through all the segmentations, that were passed in the arguments
    for segmentation in segmentations:
        #Loop through the whole aseg.means file to see whether the requested segmentation is present or not     
        for line_aseg_means_file in lines_aseg_means_file:
            if segmentation in line_aseg_means_file:
                #Get the value of the Look_up_means file of the form: -- +/- ..
                means_from_file.append(line_aseg_means_file.split()[1:4])

    #When no match is found, then just return a ".". This is treated in the recon_all_aseg_outlier_checker as a case, that is not found. 
    if(len(means_from_file) == 0): 
        return ['.', '.']           
        
    return [means_from_file[0][0], means_from_file[0][1]] 


# ------------------------------------------------------------------------------
# main function

def recon_all_aseg_outlier_checker(subjects_dir, subjects, path_data_file, path_mean_file, look_up_mean_file=None):

    import sys
    import csv

    from datetime import datetime

    from recon_all_aseg_outlier_checker import g_parc_mean_norm
    from recon_all_aseg_outlier_checker import g_parc_val_norm
    from recon_all_aseg_outlier_checker import read_parc_mean_from_table
    
    from available_segmentations import available_segmentations
    
    list_of_means = []    
    list_of_parc_val = []
    nb_outliers = 0

    # get segmentations
    segmentations = available_segmentations()    
    
    for segmentation in segmentations:
        #Look out for the mean values for all the segmentations over all subjects, or compute them 
        if look_up_mean_file is not None:
            list_segmentation = [str(segmentation)]
            list_of_means = read_parc_mean_from_table(list_segmentation, look_up_mean_file)
        else:
            list_segmentation = [str(segmentation)]
            list_of_means = g_parc_mean_norm(subjects_dir, subjects, list_segmentation)
        # in the actual output of the g_parc_mean_norm function the first value is the mean value and the second one the standard deviation
        
        means = list_of_means[0]
        stds = list_of_means[1]
        
        # If the volume is not found, then just continue with the next iteration 
        if means == "." :
            continue

        # compute and return zscore <todo>

        # reconsider from here; for the moment, stop
        sys.exit(0)
        
        # create file with means and standard deviations
        # <todo> consider if it really should be 'a' - that is not so nice with repeated runs
        try: 
            with open(path_mean_file, 'a') as f:
                f.write("{0},{1},{2},{3}".format(segmentation, means, stds, "\n"))
        except: 
            print("Impossible to write the mean values into a file, located at the subjects directory")
                    
        # Now test every segmentations of every subject against the means and standard deviations
        for subject in subjects: 
            list_segmentation = [str(segmentation)]
            list_subject = [str(subject)]
            
            # Get the actual value of the segmentation volume
            list_of_parc_val = g_parc_val_norm(subjects_dir, list_subject, list_segmentation)
            
            #Upper Limit
            if False and (float(list_of_parc_val [0]) < float(means) - 2*float(stds)): # <todo> re-consider the writing routine, and remove the 'False' condition (which is currently used as an off-switch)
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
            elif False and (float(list_of_parc_val [0]) > float(means) + 2*float(stds)): # <todo> re-consider the writing routine, and remove the 'False' condition (which is currently used as an off-switch)
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
