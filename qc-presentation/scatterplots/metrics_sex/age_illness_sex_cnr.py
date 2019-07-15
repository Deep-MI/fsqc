# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 12:28:35 2019

@author: wolfft
"""


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
cnr_lh = data_fs.Contrast_WM_GM_LH_rawavg_mgz.tolist()
cnr_lh.pop(0)
cnr_lh = [float(i) for i in cnr_lh]

cnr_rh = data_fs.Contrast_WM_GM_RH_rawavg_mgz.tolist()
cnr_rh.pop(0)
cnr_rh = [float(i) for i in cnr_rh]

cnr = np.array([cnr_lh, cnr_rh])
cnr = np.average(cnr, axis=0)

#Get the sex data
sex = data_full.Sex.tolist()
sex.pop()

#Get the indices of the subjects which are in both sheets
sbj_match_full = []
for index, subject in enumerate(sbj_full):
    if subject not in sbj_fs:
        subject = -1
    else: 
        sbj_match_full.append(subject)


sbj_m = []
sbj_f = []

#Get the IDs of the Alzheimer disease subjects in both files: 
for index, subject in enumerate(sbj_full):
    if subject in sbj_match_full:
        if sex[index] == "M":
            sbj_m.append(subject)
        elif sex[index] == "F":
            sbj_f.append(subject)


#List of cnr male subjects 
cnr_m_graph = [] 
age_m_graph = []
for subject in sbj_m: 
    index_fs = sbj_fs.index(subject)
    cnr_m_graph.append(cnr[index_fs])
    
    index_full = sbj_full.index(subject)
    age_m_graph.append(age_full[index_full])

#List of cnr female subjects
cnr_f_graph = []
age_f_graph = [] 
for subject in sbj_f: 
    index_fs = sbj_fs.index(subject)
    cnr_f_graph.append(cnr[index_fs])
    
    index_full = sbj_full.index(subject)
    age_f_graph.append(age_full[index_full])



#Generate Linear fit for male subjects
slope_m, intercept_m, r_value_m, p_value_m, std_err_m = stats.linregress(age_m_graph,cnr_m_graph)
line_m = slope_m*np.asarray(age_m_graph)+intercept_m

#Generate linear fit for female subjects
slope_f, intercept_f, r_value_f, p_value_f, std_err_f = stats.linregress(age_f_graph,cnr_f_graph)
line_f = slope_f*np.asarray(age_f_graph)+intercept_f


# Create traces
trace0 = go.Scatter(
    x = age_m_graph,
    y = cnr_m_graph,
    text = sbj_m, 
    mode = 'markers',
    marker = dict(
        size = 5,
        color = 'rgb(0, 0, 255)',
        ),
    name = 'CNR male subjects',

)
trace1 = go.Scatter(
    x=age_m_graph,
    y=line_m,
    line = dict(
        color = ('rgb(0, 0, 255)'),
        width = 3),
    name='Linear fit of the male subjects'
)

trace2 = go.Scatter(
    x = age_f_graph,
    y = cnr_f_graph,
    text = sbj_f, 
    mode = 'markers',
    marker = dict(
    size = 5,
    color = 'rgb(255, 0, 0)',
    ),
    name = 'CNR female subjects'
)

trace3 = go.Scatter(
    x=age_f_graph,
    y=line_f,
    line = dict(
        color = ('rgb(255, 0, 0)'),
        width = 3),
    name='Linear fit of the female subjects'
)


layout= go.Layout(
    title= 'Contrast to noise ration over age and sex',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Age',
        dtick=2,
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'Contrast to noise ratio',
        dtick=0.25,
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= True
)
#Linear fit difficult, beacause not every y value has a unique x value
fig= go.Figure(data=[trace0, trace1, trace2, trace3], layout=layout)
plotly.offline.plot(fig, filename = 'age-sex-cnr-scatter.html')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        