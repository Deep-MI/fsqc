# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:48:12 2019

@author: wolfft
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:29:12 2019

@author: wolfft
"""

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
cc_size = data_fs.Relative_Corpus_Callosum_size.tolist()
cc_size.pop(0)
cc_size = [float(i) for i in cc_size]


sbj_match_full = []

#Get the indices of the subjects which are in both 
for index, subject in enumerate(sbj_full):
    if subject not in sbj_fs:
        subject = -1
    else: 
        sbj_match_full.append(subject)

cc_size_graph = [] 
age_graph = []
for subject in sbj_match_full: 
    index_fs = sbj_fs.index(subject)
    cc_size_graph.append(cc_size[index_fs])
    
    index_full = sbj_full.index(subject)
    age_graph.append(age_full[index_full])

slope, intercept, r_value, p_value, std_err = stats.linregress(age_graph,cc_size_graph)
line = slope*np.asarray(age_graph)+intercept


# Create traces
trace0 = go.Scatter(
    x = age_graph,
    y = cc_size_graph,
    text = sbj_match_full, 
    mode = 'markers',
    name = 'Relative CC size'
)

trace1 = go.Scatter(
      x=age_graph,
      y=line,
      mode='lines',
      marker=go.Marker(color='rgb(2, 2, 2)'),
      name='Linear fit'
)


layout= go.Layout(
    title= 'Relative Corpus Callosum size over age',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Age',
        dtick=2,
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'Relative Corpus Callosum size ',
        dtick=0.0001,
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= True
)
data = [trace0, trace1]
fig= go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'age-cc-size.html')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        