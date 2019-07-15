# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 17:07:32 2019

@author: wolfft
"""


import pandas 
import plotly
import numpy as np
import plotly.graph_objs as go
from plotly import tools
plotly.tools.set_credentials_file(username='wolffto', api_key='B5bPKK7NCAF6oWtG3zQZ')
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

def create_graph(subjects, all_lh_holes, all_rh_holes, all_topo_lh, all_topo_rh, all_con_lh_snr, all_con_rh_snr, wm_norm, gm_norm, wm_orig, gm_orig, cc_items):
    
    all_lh_holes = [float(i) for i in all_lh_holes]
    all_rh_holes = [float(i) for i in all_rh_holes]
    all_lh_holes = np.array(all_lh_holes)
    all_rh_holes = np.array(all_rh_holes)
    all_holes = np.array([all_lh_holes, all_rh_holes])
    all_holes = np.average(all_holes, axis=0)
        
    all_topo_lh = [float(i) for i in all_topo_lh]
    all_topo_rh = [float(i) for i in all_topo_rh]
    all_topo_lh = np.array(all_topo_lh)
    all_topo_rh = np.array(all_topo_rh )
    all_topo = np.array([all_topo_lh, all_topo_rh ])
    all_topo = np.average(all_topo, axis=0)
    
    all_con_lh_snr = [float(i) for i in all_con_lh_snr]
    all_con_rh_snr = [float(i) for i in all_con_rh_snr]
    all_con_lh_snr = np.array(all_con_lh_snr)
    all_con_rh_snr = np.array(all_con_rh_snr )
    all_con_snr = np.array([all_con_lh_snr, all_con_rh_snr ])
    all_con_snr = np.average(all_con_snr, axis=0)
    
    wm_norm = [float(i) for i in wm_norm]
    gm_norm = [float(i) for i in gm_norm]
    
    wm_orig = [float(i) for i in wm_orig]
    gm_orig = [float(i) for i in gm_orig]
    
    cc_items = [float(i) for i in cc_items]
    mean_cc =np.mean(cc_items)
    print ("The mwean size of the CC is:", mean_cc)
    std_cc = np.std(cc_items)
    print("The stdv  of the CC is", std_cc)
    
    crit_cc_index1 = np.array(np.where(cc_items < (mean_cc - 2*std_cc)))
    crit_cc_index2 = np.array(np.where( cc_items> (mean_cc + 2*std_cc)))
    crit_cc_index = np.append(crit_cc_index1, crit_cc_index2)
    crit_cc_index = crit_cc_index.tolist()
    print(crit_cc_index)
    #Bad quality manual QC only motion and general image quality: 
    #bad_quality = ["OAS2_0080_MR1", "OAS2_0162_MR1", "OAS2_0157_MR2", "OAS2_0127_MR1", "OAS2_0106_MR2", "OAS2_0112_MR2", "OAS2_0114_MR2", "OAS2_0114_MR1"]
    #motion = ["OAS2_0017_MR3", "OAS2_0017_MR5","OAS2_0047_MR1","OAS2_0080_MR1", "OAS2_0094_MR1", "OAS2_0094_MR2","OAS2_0112_MR2","OAS2_0114_MR2"] 
    #index_bad =[] 
    
    #for subject in motion: 
        #index_bad.append(subjects.index(subject))      
            
    trace0 = go.Box(
        y = all_holes,
        name = 'Mean number holes',
        text =subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    )
    trace1 = go.Box(
        y = all_topo,
        name = 'Mean topological fixing time',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    )

    trace2 = go.Box(
        y = wm_norm,
        name = 'White matter SNR [norm.mgz]',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    )    
    trace3 = go.Box(
        y = gm_norm,
        name = 'Gray matter SNR [norm.mgz]',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    ) 
    trace4 = go.Box(
        y = wm_orig,
        name = 'White matter SNR [orig.mgz]',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    )     
    trace5 = go.Box(
        y = gm_orig,
        name = 'Gray matter SNR [orig.mgz]',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    ) 
    trace6 = go.Box(
        y = cc_items,
        name = 'Corpus Callosum size',
        text = subjects,
        boxpoints='all',
        selectedpoints = crit_cc_index,
    )
    trace7 = go.Box(
        y = all_con_snr,
        name = 'Mean of the contrast to noise ratio',
        text = subjects,
        boxpoints='all',
        #selectedpoints = index_bad,
    )
    
    fig = tools.make_subplots(rows = 1, cols = 8)
    
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2) 
    fig.append_trace(trace2, 1, 3)
    fig.append_trace(trace3, 1, 4) 
    fig.append_trace(trace4, 1, 5)
    fig.append_trace(trace5, 1, 6)
    fig.append_trace(trace6, 1, 7)
    fig.append_trace(trace7, 1, 8)
    
    fig['layout'].update(height=1500, width=3500, title='Different parameters')
    plotly.offline.plot(fig)
    

colnames = ["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig", "SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"]
data = pandas.read_csv("/home/wolfft/qatools/adni-results/quality-checker.csv", names = colnames)

subjects =data.Subject.tolist()
subjects.pop(0)

cc_items = data.Relative_Corpus_Callosum_size.tolist()
cc_items.pop(0)

wm_orig = data.SNR_white_matter_orig.tolist()
wm_orig.pop(0)

gm_orig = data.SNR_gray_matter_orig.tolist()
gm_orig.pop(0)

wm_norm = data.SNR_white_matter_norm.tolist()
wm_norm.pop(0)

gm_norm = data.SNR_gray_matter_norm.tolist()
gm_norm.pop(0)

all_holes_lh = data.Holes_LH.tolist()
all_holes_lh.pop(0)

all_holes_rh = data.Holes_RH.tolist()
all_holes_rh.pop(0)

all_topo_lh = data.Topo_fixing_time_LH.tolist()
all_topo_lh.pop(0)

all_topo_rh = data.Topo_fixing_time_RH.tolist()
all_topo_rh.pop(0)

all_con_lh_snr = data.Contrast_WM_GM_LH_rawavg_mgz.tolist()
all_con_lh_snr.pop(0)

all_con_rh_snr = data.Contrast_WM_GM_RH_rawavg_mgz.tolist()
all_con_rh_snr.pop(0)
















create_graph(subjects, all_holes_lh, all_holes_rh, all_topo_lh, all_topo_rh, all_con_lh_snr, all_con_rh_snr, wm_norm, gm_norm, wm_orig, gm_orig, cc_items)
