# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:36:55 2019

@author: Tobias Wolff

"""

def write_shape_to_file(subjects_dir, subjects, path_shape_file):

    import csv

    cere_wm = []
    acc_area = []
    put = []
    pial_2d = []
    cau = []
    pall = []
    lat_ven = []
    amy = []
    hipp = []
    cer_cor = []
    stria = [] 
    thalamus_proper = []
    wh_2d = []
    ven_DC = []
    
    for subject in subjects:
        path_data_file = str(subjects_dir) + str(subject) + "/brainprint/" + str(subject) + ".brainprint_50_distances.csv"
        with open(path_data_file, 'r') as csv_input:
            reader = csv.reader(csv_input)
            reader = list(reader)
            for index, row in enumerate(reader[1:]): 
                cere_wm.append(row[0])
                acc_area.append(row[1])
                put.append(row[2])
                pial_2d.append(row[3])
                cau.append(row[4])
                pall.append(row[5])
                lat_ven.append(row[6])
                amy.append(row[7])
                hipp.append(row[8])
                cer_cor.append(row[9])
                stria.append(row[10])
                thalamus_proper.append(row[11])
                wh_2d.append(row[12])
                ven_DC.append(row[13])
                
                
                
    with open(path_shape_file,'w') as file: 
        writer = csv.writer(file)
        writer.writerow(["Subject", "Cerebellum white matter", "Accumbens area", "Putamen", "Pial 2d", "Caudate", "Pallidum", "Lateral Ventricle", "Amygdala", "Hippocampus", "Cerebellum Cortex", "Striatum", "Thalamus Proper", "White 2d", "Ventral DC"])
        for index, subject in enumerate(subjects): 
            writer.writerow([subject, cere_wm[index], acc_area[index], put[index], pial_2d[index], cau[index], pall[index], lat_ven[index], amy[index], hipp[index], cer_cor[index], stria[index], thalamus_proper[index], wh_2d[index], ven_DC[index]])
