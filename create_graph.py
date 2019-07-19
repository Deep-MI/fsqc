# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 17:07:32 2019

@author: wolfft
"""



def create_graph(subjects, username_plotly, plotly_key, metrics):
    import plotly
    import numpy as np
    import plotly.graph_objs as go
    from plotly import tools
    plotly.tools.set_credentials_file(username=username_plotly,  api_key=plotly_key)
    plotly.tools.set_config_file(world_readable=True,
                             sharing='public')
    all_lh_holes = [float(i) for i in metrics.all_lh_holes]
    all_rh_holes = [float(i) for i in metrics.all_rh_holes]
    all_lh_holes = np.array(all_lh_holes)
    all_rh_holes = np.array(all_rh_holes)
    all_holes = np.array([all_lh_holes, all_rh_holes])
    all_holes = np.average(all_holes, axis=0)
    
    all_lh_defects = [float(i) for i in metrics.all_lh_defects]
    all_rh_defects = [float(i) for i in metrics.all_rh_defects]
    all_lh_defects = np.array(all_lh_defects)
    all_rh_defects = np.array(all_rh_defects)
    all_defects = np.array([all_lh_defects, all_rh_defects])
    all_defects= np.average(all_defects, axis=0)
        
    all_topo_lh = [float(i) for i in metrics.all_topo_lh]
    all_topo_rh = [float(i) for i in metrics.all_topo_rh]
    all_topo_lh = np.array(all_topo_lh)
    all_topo_rh = np.array(all_topo_rh )
    all_topo = np.array([all_topo_lh, all_topo_rh ])
    all_topo = np.average(all_topo, axis=0)
    
    all_con_lh_snr = [float(i) for i in metrics.all_con_lh_snr]
    all_con_rh_snr = [float(i) for i in metrics.all_con_rh_snr]
    all_con_lh_snr = np.array(all_con_lh_snr)
    all_con_rh_snr = np.array(all_con_rh_snr )
    all_con_snr = np.array([all_con_lh_snr, all_con_rh_snr ])
    all_con_snr = np.average(all_con_snr, axis=0)
    
    wm_norm = [float(i) for i in metrics.all_wm_snr_norm]
    gm_norm = [float(i) for i in metrics.all_gm_snr_norm]
    
    wm_orig = [float(i) for i in metrics.all_wm_snr_orig]
    gm_orig = [float(i) for i in metrics.all_gm_snr_norm]
    
    cc_items = [float(i) for i in metrics.cc_items]
         
            
    trace0 = go.Box(
        y = all_holes,
        name = 'Mean number holes',
        text =subjects,
        boxpoints='all',
    )
    trace1 = go.Box(
        y = all_defects,
        name = 'Mean number defects',
        text =subjects,
        boxpoints='all',
    )    
    
    trace2 = go.Box(
        y = all_topo,
        name = 'Mean topological fixing time',
        text = subjects,
        boxpoints='all',
    )

    trace3 = go.Box(
        y = wm_norm,
        name = 'White matter SNR [norm.mgz]',
        text = subjects,
        boxpoints='all',
    )    
    trace4 = go.Box(
        y = gm_norm,
        name = 'Gray matter SNR [norm.mgz]',
        text = subjects,
        boxpoints='all',
    ) 
    trace5 = go.Box(
        y = wm_orig,
        name = 'White matter SNR [orig.mgz]',
        text = subjects,
        boxpoints='all',
    )     
    trace6 = go.Box(
        y = gm_orig,
        name = 'Gray matter SNR [orig.mgz]',
        text = subjects,
        boxpoints='all',
    ) 
    trace7 = go.Box(
        y = cc_items,
        name = 'Corpus Callosum size',
        text = subjects,
        boxpoints='all',
    )
    trace8 = go.Box(
        y = all_con_snr,
        name = 'Mean of the contrast to noise ratio',
        text = subjects,
        boxpoints='all',
    )
    
    fig = tools.make_subplots(rows = 1, cols = 9)
    
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2) 
    fig.append_trace(trace2, 1, 3)
    fig.append_trace(trace3, 1, 4) 
    fig.append_trace(trace4, 1, 5)
    fig.append_trace(trace5, 1, 6)
    fig.append_trace(trace6, 1, 7)
    fig.append_trace(trace7, 1, 8)
    fig.append_trace(trace8, 1, 9)
    
    fig['layout'].update(height=1000, width=3500, title='Different parameters')
    plotly.offline.plot(fig, filename ="summary-plot.html")
    