# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:32:47 2019

@author: wolfft
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:11:14 2019

@author: Quality Control Validation 
"""
import pandas 
import plotly
import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
plotly.tools.set_credentials_file(username='wolffto', api_key='B5bPKK7NCAF6oWtG3zQZ')
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

colnames_fs = ["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig", "SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","lh_defects","rh_defects","Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"]
data_fs = pandas.read_csv("/home/wolfft/qatools/adni-results/quality_checker_v2.csv", names = colnames_fs)

colnames_full = ["", "Subject.ID", "Phase", "Sex", "Research.Group","Visit","Archive.Date", "Study.Date", "Age","MMSE.Total.Score", "GDSCALE.Total.Score", "Global.CDR", "Description","Type", "Imaging.Protocol",  "Image_ID",  "Site.ID",  "RID"]
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

#Get the holes data: 
holes_lh = data_fs.lh_defects.tolist()
holes_lh.pop(0)
holes_lh = [int(i) for i in holes_lh]

holes_rh = data_fs.rh_defects.tolist()
holes_rh.pop(0)
holes_rh = [int(i) for i in holes_rh]

holes = np.array([holes_lh, holes_rh])
holes = np.average(holes, axis=0)

idx_match_full = []
#Get the indices of the subjects which are in both 
for index, subject in enumerate(sbj_full):
    if subject not in sbj_fs:
        subject = -1
    else: 
        idx_match_full.append(index)
############### 80 and older ################
idx_80 = []
# Get the subject older than 80: 
for index, age in enumerate(age_full): 
    if age > 80:
        idx_80.append(index)

idx_80_fs =[]
ID_80_match = [] 
#Get the subjects older than 80 processed by freesurfer: 
for item in idx_match_full: 
    if item in idx_80:
        idx_80_fs.append(item)
        ID_80_match.append(sbj_full[item])

nb_holes_80 =[]
for subject in ID_80_match: 
    nb_holes_80.append(holes[sbj_fs.index(subject)])
    
    
    
#####70 and older ########################
idx_70 = []
# Get the subject older than 70: 
for index, age in enumerate(age_full): 
    if age < 80 and age > 70:
        idx_70.append(index)

idx_70_fs =[]
ID_70_match = [] 
#Get the subjects older than 70 processed by freesurfer: 
for item in idx_match_full: 
    if item in idx_70:
        idx_70_fs.append(item)
        ID_70_match.append(sbj_full[item])

nb_holes_70 =[]
for subject in ID_70_match: 
    nb_holes_70.append(holes[sbj_fs.index(subject)])


######60 and older#################

idx_60 = []
# Get the subject older than 60: 
for index, age in enumerate(age_full): 
    if age < 70 and age > 60:
        idx_60.append(index)

idx_60_fs =[]
ID_60_match = [] 
#Get the subjects older than 80 processed by freesurfer: 
for item in idx_match_full: 
    if item in idx_60:
        idx_60_fs.append(item)
        ID_60_match.append(sbj_full[item])

nb_holes_60 =[]
for subject in ID_60_match: 
    nb_holes_60.append(holes[sbj_fs.index(subject)])


########50 and older ################

idx_50 = []
# Get the subject older than 60: 
for index, age in enumerate(age_full): 
    if age < 60 and age > 50:
        idx_50.append(index)

idx_50_fs =[]
ID_50_match = [] 

#Get the subjects older than 80 processed by freesurfer: 
for item in idx_match_full: 
    if item in idx_50:
        idx_50_fs.append(item)
        ID_50_match.append(sbj_full[item])

nb_holes_50 =[]
for subject in ID_50_match: 
    nb_holes_50.append(holes[sbj_fs.index(subject)])



x_data = ['50 - 60', '60 - 70',
          '70 - 80', '80+',]

y0 = nb_holes_50
y1 = nb_holes_60
y2 = nb_holes_70
y3 = nb_holes_80

y_data = [y0,y1,y2,y3]

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)']

text_ID = [ID_50_match, ID_60_match, ID_70_match, ID_80_match]

traces = []

for xd, yd, textd, cls in zip(x_data, y_data, text_ID, colors):
        traces.append(go.Box(
            y=yd,
            name=xd,
            text = textd, 
            boxpoints='all',
            jitter=0.8,
            pointpos = 0,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker=dict(
                size=3,
            ),
            line=dict(width=1),
        ))

layout = go.Layout(
    title='Number of defects in relation to the age',
    xaxis= dict(
        title= 'Age',
    ),
    yaxis=dict(
        title= 'Number of defects',
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    showlegend=True
)

fig = go.Figure(data=traces, layout=layout)
plotly.offline.plot(fig, filename = 'age-defects-boxplot.html')
        