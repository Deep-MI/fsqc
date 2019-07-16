# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:42:34 2019

@author: wolfft
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:24:23 2019

@author: wolfft
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:55:06 2019

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
from scipy import stats
plotly.tools.set_credentials_file(username='wolffto', api_key='B5bPKK7NCAF6oWtG3zQZ')
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

colnames_fs = ["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig", "SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"]
data_fs = pandas.read_csv("/home/wolfft/qatools/adni-results/quality-checker.csv", names = colnames_fs)

colnames_full = ["", "Subject_ID", "Phase", "Sex", "Research_Group","Visit","Archive.Date", "Study.Date", "Age","MMSE.Total.Score", "GDSCALE.Total.Score", "Global.CDR", "Description","Type", "Imaging.Protocol",  "Image_ID",  "Site.ID",  "RID"]
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
holes_lh = data_fs.Holes_LH.tolist()
holes_lh.pop(0)
holes_lh = [float(i) for i in holes_lh]

holes_rh = data_fs.Holes_RH.tolist()
holes_rh.pop(0)
holes_rh = [float(i) for i in holes_rh]

holes = np.array([holes_lh, holes_rh])
holes = np.average(holes, axis=0)

#Get the person ID
sbj_ID = data_full.Subject_ID.tolist()
sbj_ID.pop(0)
        
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
        elif health_state[index] == "MCI" or health_state[index] =="EMCI" or health_state[index] =="LMCI" or health_state[index] == "SMC": 
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
    
'''
holes_hgt_graph = []
age_hgt_graph = []
# Find on specific subject in order to see the distribution of his points 
for index, subject in enumerate(sbj_ID):
    if subject == "003_S_5165":
        Image_ID = sbj_full[index]
        if Image_ID in sbj_AD:
            print("The subject was processed")
            index_fs = sbj_fs.index(Image_ID)
            holes_hgt_graph.append(holes[index_fs])
            
            index_full = sbj_full.index(Image_ID)
            age_hgt_graph.append(age_full[index_full])
'''

#Generate Linear fit for alzheimer disease patients
slope_AD, intercept_AD, r_value_AD, p_value_AD, std_err_AD = stats.linregress(age_AD_graph,holes_AD_graph)
line_AD = slope_AD*np.asarray(age_AD_graph)+intercept_AD

#Generate linear fit for control patients
slope_CN, intercept_CN, r_value_CN, p_value_CN, std_err_CN = stats.linregress(age_CN_graph,holes_CN_graph)
line_CN = slope_CN*np.asarray(age_CN_graph)+intercept_CN

#Generate linear fit for control patients
slope_MCI, intercept_MCI, r_value_MCI, p_value_MCI, std_err_MCI = stats.linregress(age_MCI_graph,holes_MCI_graph)
line_MCI = slope_MCI*np.asarray(age_MCI_graph)+intercept_MCI

# Create traces
trace0 = go.Scatter(
    x = age_AD_graph,
    y = holes_AD_graph,
    text = sbj_AD, 
    mode = 'markers',
    marker = dict(
        size = 5,
        color = 'rgb(204, 0, 0)',
        ),
    name = 'Number of defects for Alzheimer disease patients',

)
trace1 = go.Scatter(
    x=age_AD_graph,
    y=line_AD,
    line = dict(
        color = ('rgb(204, 0, 0)'),
        width = 3),
    name='Linear fit of the Alzheimer disease patients'
)

trace2 = go.Scatter(
    x = age_CN_graph,
    y = holes_CN_graph,
    text = sbj_CN, 
    mode = 'markers',
    marker = dict(
    size = 5,
    color = 'rgb(102, 204, 0)',
    ),
    name = 'Number of defects for control subjects'
)

trace3 = go.Scatter(
    x=age_CN_graph,
    y=line_CN,
    line = dict(
        color = ('rgb(102, 204, 0)'),
        width = 3),
    name='Linear fit of the control subjects'
)
trace4 = go.Scatter(
    x = age_MCI_graph,
    y = holes_MCI_graph,
    text = sbj_MCI, 
    mode = 'markers',
    marker = dict(
        size = 5,
        color = 'rgb(255, 153, 0)',
        ),
    name='Number of defects for the mild cognitive disease subjects',

)
trace5 = go.Scatter(
    x=age_MCI_graph,
    y=line_MCI,
    line = dict(
        color = ('rgb(255, 153, 0)'),
        width = 3),
    name='Linear fit of the mild cognitive diseaser disease subjects'
)
'''
trace6 = go.Scatter(
    x = age_hgt_graph,
    y = holes_hgt_graph,
    mode = 'markers',
    marker = dict(
        size = 5,
        color = 'rgb(0, 0, 255)',
        ),
    name='The same subject',

)
'''

layout= go.Layout(
    title= 'Number of defects in Freesurfer recon all over age and illness',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Age',
        dtick=2,
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'Number holes',
        dtick=5,
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= True
)
#Linear fit difficult, beacause not every y value has a unique x value
fig= go.Figure(data=[trace0, trace1, trace2, trace3, trace4, trace5], layout=layout)
plotly.offline.plot(fig, filename = 'age-illness-holes-scatter-extended.html')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        