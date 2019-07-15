# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:53:25 2019

@author: wolfft
"""


import pandas 
import plotly
import numpy as np
import plotly.graph_objs as go
from scipy import stats
plotly.tools.set_credentials_file(username='wolffto', api_key='B5bPKK7NCAF6oWtG3zQZ')
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

colnames_fs = ["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig", "SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","lh_defects", "rh_defects", "Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"]
data_fs = pandas.read_csv("/home/wolfft/qatools/adni-results/quality_checker_v2.csv", names = colnames_fs)

colnames_full = ["", "Subject.ID", "Phase", "Sex", "Research_Group","Visit","Archive.Date", "Study.Date", "Age","MMSE.Total.Score", "GDSCALE.Total.Score", "Global.CDR", "Description","Type", "Imaging.Protocol",  "Image_ID",  "Site.ID",  "RID"]
data_full = pandas.read_csv("/home/wolfft/qatools/adni-results/adni-qc-table1.csv", names = colnames_full)

#Get the freesurfer processed data
sbj_fs = data_fs.Subject.tolist()
sbj_fs.pop(0)
sbj_fs = [int(i) for i in sbj_fs]


#Get the whole data
sbj_full = data_full.Image_ID.tolist()
sbj_full.pop(0)
sbj_full = [int(i) for i in sbj_full]

#Get the age data
age_full = data_full.Age.tolist()
age_full.pop(0)
age_full = [float(i) for i in age_full]

#Get the health data:
health_state= data_full.Research_Group.tolist()
health_state.pop(0)
#health_state = [float(i) for i in health_state]

#Get the holes data: 
holes_lh = data_fs.lh_defects.tolist()
holes_lh.pop(0)
holes_lh = [float(i) for i in holes_lh]

holes_rh = data_fs.rh_defects.tolist()
holes_rh.pop(0)
holes_rh = [float(i) for i in holes_rh]

holes = np.array([holes_lh, holes_rh])
holes = np.average(holes, axis=0)

#Get the indices of the subjects which are in both sheets
sbj_match_full = []
for index, subject in enumerate(sbj_full):
    if subject not in sbj_fs:
        subject = -1
    else: 
        sbj_match_full.append(subject)


sbj_AD = []
sbj_MCI = []
sbj_CN = []

#Get the IDs of the Alzheimer disease subjects in both files: 
for index, subject in enumerate(sbj_full):
    if subject in sbj_match_full:
        if health_state[index] == "AD":
            sbj_AD.append(subject)
        elif health_state[index] == "CN":
            sbj_CN.append(subject)
        elif health_state[index] == "MCI" or health_state[index] == "EMCI" or health_state[index] == "LMCI": 
            sbj_MCI.append(subject)

#List of holes alzheimer patients 
holes_AD_graph = [] 
age_AD_graph = []
for subject in sbj_AD: 
    index_fs = sbj_fs.index(subject)
    holes_AD_graph.append(holes[index_fs])
    
    index_full = sbj_full.index(subject)
    age_AD_graph.append(age_full[index_full])

#List of holes control subjects
holes_CN_graph = []
age_CN_graph = [] 
for subject in sbj_CN: 
    index_fs = sbj_fs.index(subject)
    holes_CN_graph.append(holes[index_fs])
    
    index_full = sbj_full.index(subject)
    age_CN_graph.append(age_full[index_full])

#List of holes beginning Alzheimer
holes_MCI_graph = []
age_MCI_graph = [] 
for subject in sbj_MCI: 
    index_fs = sbj_fs.index(subject)
    holes_MCI_graph.append(holes[index_fs])
    
    index_full = sbj_full.index(subject)
    age_MCI_graph.append(age_full[index_full])











