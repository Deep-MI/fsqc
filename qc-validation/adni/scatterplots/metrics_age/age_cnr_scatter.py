# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:05:12 2019

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
cnr_lh = data_fs.Contrast_WM_GM_LH_rawavg_mgz.tolist()
cnr_lh.pop(0)
cnr_lh = [float(i) for i in cnr_lh]

cnr_rh = data_fs.Contrast_WM_GM_RH_rawavg_mgz.tolist()
cnr_rh.pop(0)
cnr_rh = [float(i) for i in cnr_rh]

cnr = np.array([cnr_lh, cnr_rh])
cnr = np.average(cnr, axis=0)

sbj_match_full = []

#Get the indices of the subjects which are in both 
for index, subject in enumerate(sbj_full):
    if subject not in sbj_fs:
        subject = -1
    else: 
        sbj_match_full.append(subject)

cnr_graph = [] 
age_graph = []
for subject in sbj_match_full: 
    index_fs = sbj_fs.index(subject)
    cnr_graph.append(cnr[index_fs])
    
    index_full = sbj_full.index(subject)
    age_graph.append(age_full[index_full])

slope, intercept, r_value, p_value, std_err = stats.linregress(age_graph,cnr_graph)
line = slope*np.asarray(age_graph)+intercept


# Create traces
trace0 = go.Scatter(
    x = age_graph,
    y = cnr_graph,
    text = sbj_match_full, 
    mode = 'markers',
    name = 'CNR'
)

trace1 = go.Scatter(
                  x=age_graph,
                  y=line,
                  mode='lines',
                  marker=go.Marker(color='rgb(2, 2, 2)'),
                  name='Linear fit'
                  )


layout= go.Layout(
    title= 'Contrast to Noise ratio over age',
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
        dtick=0.1,
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= True
)
data = [trace0, trace1]
fig= go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'age-cnr-scatter.html')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        