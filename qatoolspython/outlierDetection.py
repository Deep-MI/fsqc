#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides a function to evaluate potential outliers in the aseg.stats
values.

"""

# ------------------------------------------------------------------------------
# subfunctions

def readAsegStats(path_aseg_stats):
    """
    A function to read aseg.stats files.

    """

    # read file
    with open(path_aseg_stats) as stats_file:
        aseg_stats = stats_file.read().splitlines()

    # initialize
    aseg = dict()

    # read measures
    for line in aseg_stats:
        if '# Measure BrainSeg,' in line:
            aseg.update({'BrainSeg' : float(line.split(',')[3])})
        elif '# Measure BrainSegNotVent,' in line:
            aseg.update({'BrainSegNotVent' : float(line.split(',')[3])})
        elif '# Measure BrainSegNotVentSurf,' in line:
            aseg.update({'BrainSegNotVentSurf' : float(line.split(',')[3])})
        elif '# Measure VentricleChoroidVol,' in line:
            aseg.update({'VentricleChoroidVol' : float(line.split(',')[3])})
        elif '# Measure lhCortex,' in line:
            aseg.update({'lhCortex' : float(line.split(',')[3])})
        elif '# Measure rhCortex,' in line:
            aseg.update({'rhCortex' : float(line.split(',')[3])})
        elif '# Measure Cortex,' in line:
            aseg.update({'Cortex' : float(line.split(',')[3])})
        elif '# Measure lhCerebralWhiteMatter,' in line:
            aseg.update({'lhCerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure rhCerebralWhiteMatter,' in line:
            aseg.update({'rhCerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure CerebralWhiteMatter,' in line:
            aseg.update({'CerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure SubCortGray,' in line:
            aseg.update({'SubCortGray' : float(line.split(',')[3])})
        elif '# Measure TotalGray,' in line:
            aseg.update({'TotalGray' : float(line.split(',')[3])})
        elif '# Measure SupraTentorial,' in line:
            aseg.update({'SupraTentorial' : float(line.split(',')[3])})
        elif '# Measure SupraTentorialNotVent,' in line:
            aseg.update({'SupraTentorialNotVent' : float(line.split(',')[3])})
        elif '# Measure SupraTentorialNotVentVox,' in line:
            aseg.update({'SupraTentorialNotVentVox' : float(line.split(',')[3])})
        elif '# Measure Mask,' in line:
            aseg.update({'Mask' : float(line.split(',')[3])})
        elif '# Measure BrainSegVol-to-eTIV,' in line:
            aseg.update({'BrainSegVol_to_eTIV' : float(line.split(',')[3])})
        elif '# Measure MaskVol-to-eTIV,' in line:
            aseg.update({'MaskVol_to_eTIV' : float(line.split(',')[3])})
        elif '# Measure lhSurfaceHoles,' in line:
            aseg.update({'lhSurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure rhSurfaceHoles,' in line:
            aseg.update({'rhSurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure SurfaceHoles,' in line:
            aseg.update({'SurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure EstimatedTotalIntraCranialVol,' in line:
            aseg.update({'EstimatedTotalIntraCranialVol' : float(line.split(',')[3])})
        elif 'Left-Lateral-Ventricle' in line:
            aseg.update({'Left-Lateral-Ventricle' : float(line.split()[3])})
        elif 'Left-Inf-Lat-Vent' in line:
            aseg.update({'Left-Inf-Lat-Vent' : float(line.split()[3])})
        elif 'Left-Cerebellum-White-Matter' in line:
            aseg.update({'Left-Cerebellum-White-Matter' : float(line.split()[3])})
        elif 'Left-Cerebellum-Cortex' in line:
            aseg.update({'Left-Cerebellum-Cortex' : float(line.split()[3])})
        elif 'Left-Thalamus-Proper' in line:
            aseg.update({'Left-Thalamus-Proper' : float(line.split()[3])})
        elif 'Left-Caudate' in line:
            aseg.update({'Left-Caudate' : float(line.split()[3])})
        elif 'Left-Putamen' in line:
            aseg.update({'Left-Putamen' : float(line.split()[3])})
        elif 'Left-Pallidum' in line:
            aseg.update({'Left-Pallidum' : float(line.split()[3])})
        elif '3rd-Ventricle' in line:
            aseg.update({'3rd-Ventricle' : float(line.split()[3])})
        elif '4th-Ventricle' in line:
            aseg.update({'4th-Ventricle' : float(line.split()[3])})
        elif 'Brain-Stem' in line:
            aseg.update({'Brain-Stem' : float(line.split()[3])})
        elif 'Left-Hippocampus' in line:
            aseg.update({'Left-Hippocampus' : float(line.split()[3])})
        elif 'Left-Amygdala' in line:
            aseg.update({'Left-Amygdala' : float(line.split()[3])})
        elif 'CSF' in line:
            aseg.update({'CSF' : float(line.split()[3])})
        elif 'Left-Accumbens-area' in line:
            aseg.update({'Left-Accumbens-area' : float(line.split()[3])})
        elif 'Left-VentralDC' in line:
            aseg.update({'Left-VentralDC' : float(line.split()[3])})
        elif 'Left-vessel' in line:
            aseg.update({'Left-vessel' : float(line.split()[3])})
        elif 'Left-choroid-plexus' in line:
            aseg.update({'Left-choroid-plexus' : float(line.split()[3])})
        elif 'Right-Lateral-Ventricle' in line:
            aseg.update({'Right-Lateral-Ventricle' : float(line.split()[3])})
        elif 'Right-Inf-Lat-Vent' in line:
            aseg.update({'Right-Inf-Lat-Vent' : float(line.split()[3])})
        elif 'Right-Cerebellum-White-Matter' in line:
            aseg.update({'Right-Cerebellum-White-Matter' : float(line.split()[3])})
        elif 'Right-Cerebellum-Cortex' in line:
            aseg.update({'Right-Cerebellum-Cortex' : float(line.split()[3])})
        elif 'Right-Thalamus-Proper' in line:
            aseg.update({'Right-Thalamus-Proper' : float(line.split()[3])})
        elif 'Right-Caudate' in line:
            aseg.update({'Right-Caudate' : float(line.split()[3])})
        elif 'Right-Putamen' in line:
            aseg.update({'Right-Putamen' : float(line.split()[3])})
        elif 'Right-Pallidum' in line:
            aseg.update({'Right-Pallidum' : float(line.split()[3])})
        elif 'Right-Hippocampus' in line:
            aseg.update({'Right-Hippocampus' : float(line.split()[3])})
        elif 'Right-Amygdala' in line:
            aseg.update({'Right-Amygdala' : float(line.split()[3])})
        elif 'Right-Accumbens-area' in line:
            aseg.update({'Right-Accumbens-area' : float(line.split()[3])})
        elif 'Right-VentralDC' in line:
            aseg.update({'Right-VentralDC' : float(line.split()[3])})
        elif 'Right-vessel' in line:
            aseg.update({'Right-vessel' : float(line.split()[3])})
        elif 'Right-choroid-plexus' in line:
            aseg.update({'Right-choroid-plexus' : float(line.split()[3])})
        elif '5th-Ventricle' in line:
            aseg.update({'5th-Ventricle' : float(line.split()[3])})
        elif 'WM-hypointensities' in line:
            aseg.update({'WM-hypointensities' : float(line.split()[3])})
        elif 'Left-WM-hypointensities' in line:
            aseg.update({'Left-WM-hypointensities' : float(line.split()[3])})
        elif 'Right-WM-hypointensities' in line:
            aseg.update({'Right-WM-hypointensities' : float(line.split()[3])})
        elif 'non-WM-hypointensities' in line:
            aseg.update({'non-WM-hypointensities' : float(line.split()[3])})
        elif 'Left-non-WM-hypointensities' in line:
            aseg.update({'Left-non-WM-hypointensities' : float(line.split()[3])})
        elif 'Right-non-WM-hypointensities' in line:
            aseg.update({'Right-non-WM-hypointensities' : float(line.split()[3])})
        elif 'Optic-Chiasm' in line:
            aseg.update({'Optic-Chiasm' : float(line.split()[3])})
        elif 'CC_Posterior' in line:
            aseg.update({'CC_Posterior' : float(line.split()[3])})
        elif 'CC_Mid_Posterior' in line:
            aseg.update({'CC_Mid_Posterior' : float(line.split()[3])})
        elif 'CC_Central' in line:
            aseg.update({'CC_Central' : float(line.split()[3])})
        elif 'CC_Mid_Anterior' in line:
            aseg.update({'CC_Mid_Anterior' : float(line.split()[3])})
        elif 'CC_Anterior' in line:
            aseg.update({'CC_Anterior' : float(line.split()[3])})

    # return
    return aseg

# ------------------------------------------------------------------------------
# outlier table

def outlierTable():
    """
    A function to provide normative values for Freesurfer segmentations and 
    parcellations.

    """

    # define

    outlierDict = dict([
        ('Left-Accumbens-area',     dict([('upper' ,   509.6091023431), ('lower',  255.3576702622)])),
        ('Right-Accumbens-area',    dict([('upper' ,   536.8292541219), ('lower',  223.7429113041)])),
        ('Left-Amygdala',           dict([('upper' ,  1346.7573549195), ('lower',  380.9204342249)])),
        ('Right-Amygdala',          dict([('upper' ,  1365.6951800715), ('lower',  420.9326296839)])),
        ('Brain-Stem',              dict([('upper' , 16997.7430745096), ('lower', 3657.1478690755)])),
        ('Left-Caudate',            dict([('upper' ,  3188.8127849175), ('lower',  853.5816689255)])),
        ('Right-Caudate',           dict([('upper' ,  3017.2388990504), ('lower',  929.0249281701)])),
        ('Left-Hippocampus',        dict([('upper' ,  3639.3977943391), ('lower',  757.5026482920)])),
        ('Right-Hippocampus',       dict([('upper' ,  3625.6761542953), ('lower',  744.6170559887)])),
        ('Left-Pallidum',           dict([('upper' ,  1243.2988760927), ('lower',  460.1844875813)])),
        ('Right-Pallidum',          dict([('upper' ,  1333.4290920726), ('lower',  395.7811514099)])),
        ('Left-Putamen',            dict([('upper' ,  5199.9084328105), ('lower', 1324.1891523885)])),
        ('Right-Putamen',           dict([('upper' ,  4748.0423983620), ('lower', 1195.5103714010)])),
        ('Left-Thalamus-Proper',    dict([('upper' ,  6927.7566928780), ('lower', 1515.2832635261)])),
        ('Right-Thalamus-Proper',   dict([('upper' ,  6204.6848002925), ('lower', 1151.0914168195)])),
        ('Left-VentralDC',          dict([('upper' ,  3202.3856880955), ('lower',  661.9855654822)])),
        ('Right-VentralDC',         dict([('upper' ,  3249.1969199473), ('lower',  637.5855119944)])),
        ('Left-Lateral-Ventricle',  dict([('upper' ,  3070.2562410945), ('lower', 1779.0430005652)])),
        ('Right-Lateral-Ventricle', dict([('upper' ,  2800.1887579545), ('lower', 1629.7315789310)])),
        ('Left-Inf-Lat-Vent',       dict([('upper' ,   126.4224881060), ('lower',   90.6177444805)])),
        ('Right-Inf-Lat-Vent',      dict([('upper' ,   140.7914462122), ('lower',  103.1532053946)])),
        ('3rd-Ventricle',           dict([('upper' ,   514.6258578455), ('lower',  218.1140098856)])),
        ('4th-Ventricle',           dict([('upper' ,  1506.5993007538), ('lower', 1094.4819038702)]))
        ])

    # return
    return outlierDict

# ------------------------------------------------------------------------------
# main function

def outlierDetection(subjects, subjects_dir, output_dir, outlierDict, min_no_subjects=10):
    """
    A function to evaluate potential outliers in the aseg.stats values.

    """

    # imports

    import os
    import csv
    import numpy as np
    import pandas as pd
    from outlierDetection import readAsegStats

    # create a dictionary with all data from all subjects, and create a list of all available keys

    aseg = dict()

    all_aseg_keys = list()

    for subject in subjects:

        path_aseg_stats = os.path.join(subjects_dir, subject, "stats", "aseg.stats")
        aseg_stats = readAsegStats(path_aseg_stats)

        aseg.update({subject : aseg_stats})

        all_aseg_keys.extend(list(aseg_stats.keys()))

    all_aseg_keys = list(sorted(set(all_aseg_keys)))

    # compare individual data against sample statistics (if more than min_no_subjects cases)

    outlierSampleNonpar = dict()
    outlierSampleParam = dict()

    outlierSampleNonparNum = dict()
    outlierSampleParamNum = dict()

    if len(subjects) >= min_no_subjects:

        # compute means, sd, medians, and quantiles based on sample

        df = pd.DataFrame.from_dict(aseg).transpose()

        iqr = np.percentile(df, 75, axis=0) - np.percentile(df, 25, axis=0)

        sample_nonpar_lower = dict(zip(dict(df).keys(), np.percentile(df, 25, axis=0) - 1.5 * iqr))
        sample_nonpar_upper = dict(zip(dict(df).keys(), np.percentile(df, 75, axis=0) + 1.5 * iqr))

        sample_param_lower = dict(np.mean(df, axis=0) - 2 * np.std(df, axis=0))
        sample_param_upper = dict(np.mean(df, axis=0) + 2 * np.std(df, axis=0))

        # compare individual data against sample statistics

        for subject in aseg:

            nonparDict = dict()
            paramDict = dict()

            for key in aseg[subject]:

                if (aseg[subject][key] < sample_nonpar_lower[key]) or (aseg[subject][key] > sample_nonpar_upper[key]):
                    nonparDict.update({key : True })
                else:
                    nonparDict.update({key : False })

                if (aseg[subject][key] < sample_param_lower[key]) or (aseg[subject][key] > sample_param_upper[key]):
                    paramDict.update({key : True })
                else:
                    paramDict.update({key : False })

            outlierSampleNonpar.update({subject : nonparDict})
            outlierSampleParam.update({subject: paramDict})

            outlierSampleNonparNum.update({subject : np.sum(list(nonparDict.values()))})
            outlierSampleParamNum.update({subject : np.sum(list(paramDict.values()))})

    else:

        for subject in aseg:

            nonparDict = dict()
            paramDict = dict()

            for key in aseg[subject]:

                nonparDict.update({key : np.nan })
                paramDict.update({key : np.nan })

            outlierSampleNonpar.update({subject : nonparDict})
            outlierSampleParam.update({subject: paramDict})

            outlierSampleNonparNum.update({subject: np.nan})
            outlierSampleParamNum.update({subject: np.nan})

    # compare individual data against normative values

    outlierNorms = dict()

    outlierNormsNum = dict()

    for subject in aseg:

        normsDict = dict()

        for key in outlierDict:

            if (aseg[subject][key] < outlierDict[key]['lower']) or (aseg[subject][key] > outlierDict[key]['upper']):
                normsDict.update({key: True})
            else:
                normsDict.update({key: False})

        outlierNorms.update({subject : normsDict})

        outlierNormsNum.update({subject: np.sum(list(normsDict.values()))})

    # write to csv files

    asegFieldnames = ['subject']
    asegFieldnames.extend(all_aseg_keys)

    with open(os.path.join(output_dir, 'all.aseg.stats'), 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=asegFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(aseg.keys()):
            tmp = aseg[subject]
            tmp.update({'subject' : subject})
            csvwriter.writerow(tmp)

    with open(os.path.join(output_dir, 'all.outliers.sample.nonpar.stats'), 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=asegFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(outlierSampleNonpar.keys()):
            tmp = outlierSampleNonpar[subject]
            tmp.update({'subject' : subject})
            csvwriter.writerow(tmp)

    with open(os.path.join(output_dir, 'all.outliers.sample.param.stats'), 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=asegFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(outlierSampleParam.keys()):
            tmp = outlierSampleParam[subject]
            tmp.update({'subject' : subject})
            csvwriter.writerow(tmp)

    with open(os.path.join(output_dir, 'all.outliers.norms.stats'), 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=asegFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(outlierNorms.keys()):
            tmp = outlierNorms[subject]
            tmp.update({'subject' : subject})
            csvwriter.writerow(tmp)

    # return

    return outlierSampleNonparNum, outlierSampleParamNum, outlierNormsNum
