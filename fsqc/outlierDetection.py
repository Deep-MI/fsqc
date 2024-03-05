"""
This module provides a function to evaluate potential outliers in the
aseg.stats, aparc.stats, and hypothalamic and hippocampal values (if present).

"""

# ------------------------------------------------------------------------------
# subfunctions


def readAsegStats(path_aseg_stats):
    """
    Read FreeSurfer aseg.stats files.

    Parameters
    ----------
    path_aseg_stats : str
        Path to the aseg.stats file.

    Returns
    -------
    dict
        A dictionary containing FreeSurfer aseg measures.
    """
    # read file
    with open(path_aseg_stats) as stats_file:
        aseg_stats = stats_file.read().splitlines()

    # initialize
    aseg = dict()

    # read measures
    for line in aseg_stats:
        if "# Measure BrainSeg," in line:
            aseg.update({"aseg.BrainSeg": float(line.split(",")[3])})
        elif "# Measure BrainSegNotVent," in line:
            aseg.update({"aseg.BrainSegNotVent": float(line.split(",")[3])})
        elif "# Measure BrainSegNotVentSurf," in line:
            aseg.update({"aseg.BrainSegNotVentSurf": float(line.split(",")[3])})
        elif "# Measure VentricleChoroidVol," in line:
            aseg.update({"aseg.VentricleChoroidVol": float(line.split(",")[3])})
        elif "# Measure lhCortex," in line:
            aseg.update({"aseg.lhCortex": float(line.split(",")[3])})
        elif "# Measure rhCortex," in line:
            aseg.update({"aseg.rhCortex": float(line.split(",")[3])})
        elif "# Measure Cortex," in line:
            aseg.update({"aseg.Cortex": float(line.split(",")[3])})
        elif "# Measure lhCerebralWhiteMatter," in line:
            aseg.update({"aseg.lhCerebralWhiteMatter": float(line.split(",")[3])})
        elif "# Measure rhCerebralWhiteMatter," in line:
            aseg.update({"aseg.rhCerebralWhiteMatter": float(line.split(",")[3])})
        elif "# Measure CerebralWhiteMatter," in line:
            aseg.update({"aseg.CerebralWhiteMatter": float(line.split(",")[3])})
        elif "# Measure SubCortGray," in line:
            aseg.update({"aseg.SubCortGray": float(line.split(",")[3])})
        elif "# Measure TotalGray," in line:
            aseg.update({"aseg.TotalGray": float(line.split(",")[3])})
        elif "# Measure SupraTentorial," in line:
            aseg.update({"aseg.SupraTentorial": float(line.split(",")[3])})
        elif "# Measure SupraTentorialNotVent," in line:
            aseg.update({"aseg.SupraTentorialNotVent": float(line.split(",")[3])})
        elif "# Measure SupraTentorialNotVentVox," in line:
            aseg.update({"aseg.SupraTentorialNotVentVox": float(line.split(",")[3])})
        elif "# Measure Mask," in line:
            aseg.update({"aseg.Mask": float(line.split(",")[3])})
        elif "# Measure BrainSegVol-to-eTIV," in line:
            aseg.update({"aseg.BrainSegVol_to_eTIV": float(line.split(",")[3])})
        elif "# Measure MaskVol-to-eTIV," in line:
            aseg.update({"aseg.MaskVol_to_eTIV": float(line.split(",")[3])})
        elif "# Measure lhSurfaceHoles," in line:
            aseg.update({"aseg.lhSurfaceHoles": float(line.split(",")[3])})
        elif "# Measure rhSurfaceHoles," in line:
            aseg.update({"aseg.rhSurfaceHoles": float(line.split(",")[3])})
        elif "# Measure SurfaceHoles," in line:
            aseg.update({"aseg.SurfaceHoles": float(line.split(",")[3])})
        elif "# Measure EstimatedTotalIntraCranialVol," in line:
            aseg.update(
                {"aseg.EstimatedTotalIntraCranialVol": float(line.split(",")[3])}
            )
        elif "Left-Lateral-Ventricle" in line:
            aseg.update({"aseg.Left-Lateral-Ventricle": float(line.split()[3])})
        elif "Left-Inf-Lat-Vent" in line:
            aseg.update({"aseg.Left-Inf-Lat-Vent": float(line.split()[3])})
        elif "Left-Cerebellum-White-Matter" in line:
            aseg.update({"aseg.Left-Cerebellum-White-Matter": float(line.split()[3])})
        elif "Left-Cerebellum-Cortex" in line:
            aseg.update({"aseg.Left-Cerebellum-Cortex": float(line.split()[3])})
        elif "Left-Thalamus-Proper" in line:
            aseg.update({"aseg.Left-Thalamus-Proper": float(line.split()[3])})
        elif "Left-Caudate" in line:
            aseg.update({"aseg.Left-Caudate": float(line.split()[3])})
        elif "Left-Putamen" in line:
            aseg.update({"aseg.Left-Putamen": float(line.split()[3])})
        elif "Left-Pallidum" in line:
            aseg.update({"aseg.Left-Pallidum": float(line.split()[3])})
        elif "3rd-Ventricle" in line:
            aseg.update({"aseg.3rd-Ventricle": float(line.split()[3])})
        elif "4th-Ventricle" in line:
            aseg.update({"aseg.4th-Ventricle": float(line.split()[3])})
        elif "Brain-Stem" in line:
            aseg.update({"aseg.Brain-Stem": float(line.split()[3])})
        elif "Left-Hippocampus" in line:
            aseg.update({"aseg.Left-Hippocampus": float(line.split()[3])})
        elif "Left-Amygdala" in line:
            aseg.update({"aseg.Left-Amygdala": float(line.split()[3])})
        elif "CSF" in line:
            aseg.update({"aseg.CSF": float(line.split()[3])})
        elif "Left-Accumbens-area" in line:
            aseg.update({"aseg.Left-Accumbens-area": float(line.split()[3])})
        elif "Left-VentralDC" in line:
            aseg.update({"aseg.Left-VentralDC": float(line.split()[3])})
        elif "Left-vessel" in line:
            aseg.update({"aseg.Left-vessel": float(line.split()[3])})
        elif "Left-choroid-plexus" in line:
            aseg.update({"aseg.Left-choroid-plexus": float(line.split()[3])})
        elif "Right-Lateral-Ventricle" in line:
            aseg.update({"aseg.Right-Lateral-Ventricle": float(line.split()[3])})
        elif "Right-Inf-Lat-Vent" in line:
            aseg.update({"aseg.Right-Inf-Lat-Vent": float(line.split()[3])})
        elif "Right-Cerebellum-White-Matter" in line:
            aseg.update({"aseg.Right-Cerebellum-White-Matter": float(line.split()[3])})
        elif "Right-Cerebellum-Cortex" in line:
            aseg.update({"aseg.Right-Cerebellum-Cortex": float(line.split()[3])})
        elif "Right-Thalamus-Proper" in line:
            aseg.update({"aseg.Right-Thalamus-Proper": float(line.split()[3])})
        elif "Right-Caudate" in line:
            aseg.update({"aseg.Right-Caudate": float(line.split()[3])})
        elif "Right-Putamen" in line:
            aseg.update({"aseg.Right-Putamen": float(line.split()[3])})
        elif "Right-Pallidum" in line:
            aseg.update({"aseg.Right-Pallidum": float(line.split()[3])})
        elif "Right-Hippocampus" in line:
            aseg.update({"aseg.Right-Hippocampus": float(line.split()[3])})
        elif "Right-Amygdala" in line:
            aseg.update({"aseg.Right-Amygdala": float(line.split()[3])})
        elif "Right-Accumbens-area" in line:
            aseg.update({"aseg.Right-Accumbens-area": float(line.split()[3])})
        elif "Right-VentralDC" in line:
            aseg.update({"aseg.Right-VentralDC": float(line.split()[3])})
        elif "Right-vessel" in line:
            aseg.update({"aseg.Right-vessel": float(line.split()[3])})
        elif "Right-choroid-plexus" in line:
            aseg.update({"aseg.Right-choroid-plexus": float(line.split()[3])})
        elif "5th-Ventricle" in line:
            aseg.update({"aseg.5th-Ventricle": float(line.split()[3])})
        elif "WM-hypointensities" in line:
            aseg.update({"aseg.WM-hypointensities": float(line.split()[3])})
        elif "Left-WM-hypointensities" in line:
            aseg.update({"aseg.Left-WM-hypointensities": float(line.split()[3])})
        elif "Right-WM-hypointensities" in line:
            aseg.update({"aseg.Right-WM-hypointensities": float(line.split()[3])})
        elif "non-WM-hypointensities" in line:
            aseg.update({"aseg.non-WM-hypointensities": float(line.split()[3])})
        elif "Left-non-WM-hypointensities" in line:
            aseg.update({"aseg.Left-non-WM-hypointensities": float(line.split()[3])})
        elif "Right-non-WM-hypointensities" in line:
            aseg.update({"aseg.Right-non-WM-hypointensities": float(line.split()[3])})
        elif "Optic-Chiasm" in line:
            aseg.update({"aseg.Optic-Chiasm": float(line.split()[3])})
        elif "CC_Posterior" in line:
            aseg.update({"aseg.CC_Posterior": float(line.split()[3])})
        elif "CC_Mid_Posterior" in line:
            aseg.update({"aseg.CC_Mid_Posterior": float(line.split()[3])})
        elif "CC_Central" in line:
            aseg.update({"aseg.CC_Central": float(line.split()[3])})
        elif "CC_Mid_Anterior" in line:
            aseg.update({"aseg.CC_Mid_Anterior": float(line.split()[3])})
        elif "CC_Anterior" in line:
            aseg.update({"aseg.CC_Anterior": float(line.split()[3])})

    # return
    return aseg


def readAparcStats(path_aparc_stats, hemi):
    """
    Read FreeSurfer aparc.stats files.

    Parameters
    ----------
    path_aparc_stats : str
        Path to the aparc.stats file.
    hemi : str
        Hemisphere designation ('lh' for left, 'rh' for right).

    Returns
    -------
    tuple
        A tuple containing three dictionaries:

        - Header information for the aparc.stats file.
        - Detailed measures for different anatomical regions.
        - Thickness values for each region.
    """
    # read file
    with open(path_aparc_stats) as stats_file:
        aparc_stats = stats_file.read().splitlines()

    # read header
    header = dict()
    for line in aparc_stats:
        if "# Measure Cortex, NumVert, " in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "CortexNumVert": float(line.split(",")[3])
                }
            )
        elif "# Measure Cortex, WhiteSurfArea," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "CortexWhiteSurfArea": float(line.split(",")[3])
                }
            )
        elif "# Measure Cortex, MeanThickness," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "CortexMeanThickness": float(line.split(",")[3])
                }
            )
        elif "# Measure BrainSeg," in line:
            header.update(
                {"aparc" + "." + hemi + "." + "BrainSeg": float(line.split(",")[3])}
            )
        elif "# Measure BrainSegNotVent," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "BrainSegNotVent": float(line.split(",")[3])
                }
            )
        elif "# Measure BrainSegNotVentSurf," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "BrainSegNotVentSurf": float(line.split(",")[3])
                }
            )
        elif "# Measure Cortex, CortexVol Total cortical gray matter volume," in line:
            # missing comma in fs60 and fs71, hence [2]
            header.update(
                {"aparc" + "." + hemi + "." + "Cortex": float(line.split(",")[2])}
            )
        elif "# Measure SupraTentorial," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "SupraTentorial": float(line.split(",")[3])
                }
            )
        elif "# Measure SupraTentorialNotVent," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "SupraTentorialNotVent": float(line.split(",")[3])
                }
            )
        elif "# Measure EstimatedTotalIntraCranialVol," in line:
            header.update(
                {
                    "aparc"
                    + "."
                    + hemi
                    + "."
                    + "EstimatedTotalIntraCranialVol": float(line.split(",")[3])
                }
            )

    # get column headers
    col_headers = None
    for line in aparc_stats:
        if "# ColHeaders " in line:
            col_headers = line.replace("# ColHeaders", "").split()

    # read aparc
    aparc = dict()
    if col_headers is not None:
        for line in aparc_stats:
            if "bankssts" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "bankssts": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "caudalanteriorcingulate" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "caudalanteriorcingulate": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "caudalmiddlefrontal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "caudalmiddlefrontal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "cuneus" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "cuneus": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "entorhinal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "entorhinal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "fusiform" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "fusiform": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "inferiorparietal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "inferiorparietal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "inferiortemporal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "inferiortemporal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "isthmuscingulate" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "isthmuscingulate": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "lateraloccipital" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "lateraloccipital": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "lateralorbitofrontal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "lateralorbitofrontal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "lingual" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "lingual": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "medialorbitofrontal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "medialorbitofrontal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "middletemporal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "middletemporal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "parahippocampal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "parahippocampal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "paracentral" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "paracentral": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "parsopercularis" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "parsopercularis": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "parsorbitalis" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "parsorbitalis": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "parstriangularis" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "parstriangularis": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "pericalcarine" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "pericalcarine": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "postcentral" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "postcentral": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "posteriorcingulate" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "posteriorcingulate": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "precentral" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "precentral": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "precuneus" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "precuneus": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "rostralanteriorcingulate" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "rostralanteriorcingulate": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "rostralmiddlefrontal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "rostralmiddlefrontal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "superiorfrontal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "superiorfrontal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "superiorparietal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "superiorparietal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "superiortemporal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "superiortemporal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "supramarginal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "supramarginal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "frontalpole" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "frontalpole": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "temporalpole" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "temporalpole": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "transversetemporal" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "transversetemporal": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )
            elif "insula" in line:
                aparc.update(
                    {
                        "aparc"
                        + "."
                        + hemi
                        + "."
                        + "insula": dict(
                            zip(col_headers[1:], [float(x) for x in line.split()[1:]])
                        )
                    }
                )

    # extract thickness values
    if col_headers is not None:
        thickness = dict()
        for x in aparc.keys():
            thickness[x] = aparc[x]["ThickAvg"]

    # return
    return header, aparc, thickness


def readHypothalamusStats(path_hypothalamus_stats):
    """
    Read hypothalamic volume files.

    Parameters
    ----------
    path_hypothalamus_stats : str
        Path to the hypothalamic volume file.

    Returns
    -------
    dict
        A dictionary containing hypothalamic volume information.
    """
    # imports
    import pandas as pd

    # read file
    hypothalamus_stats = pd.read_csv(path_hypothalamus_stats)

    #
    hypothalamus_stats.columns = "hypothalamus" + "." + hypothalamus_stats.columns

    #
    hypo = hypothalamus_stats.to_dict(orient="index")[0]

    #
    hypo.pop("hypothalamus.subject", None)

    # return
    return hypo


def readHippocampusStats(path_hippocampus_stats, hemi, prefix):
    """
    Read hippocampal or amygdala volume files.

    Parameters
    ----------
    path_hippocampus_stats : str
        Path to the volume file.
    hemi : str
        Hemisphere identifier (e.g., 'lh' or 'rh').
    prefix : str
        Prefix for column names.

    Returns
    -------
    dict
        Dictionary containing volume values with column names.
    """
    # imports
    import pandas as pd

    # read file
    hippocampus_stats = pd.read_csv(
        path_hippocampus_stats, sep=" ", header=None, names=["volume"], index_col=0
    )

    #
    hippo = hippocampus_stats.transpose()

    hippo.columns = prefix + "." + hemi + "." + hippo.columns

    hippo = hippo.to_dict(orient="index")["volume"]

    # return
    return hippo


# ------------------------------------------------------------------------------
# outlier table


def outlierTable():
    """
    Provide upper and lower bounds for volumes of several brain structures.

    Returns
    -------
    dict
        A dictionary containing upper and lower bounds for several brain structures.
    """
    # define

    outlierDict = dict(
        [
            (
                "Left-Accumbens-area",
                dict([("lower", 210.87844594754), ("upper", 718.01022026916)]),
            ),
            (
                "Right-Accumbens-area",
                dict([("lower", 304.86134907845), ("upper", 751.63838456345)]),
            ),
            (
                "Left-Amygdala",
                dict([("lower", 1179.73655974083), ("upper", 1935.09415214717)]),
            ),
            (
                "Right-Amygdala",
                dict([("lower", 1161.54746836742), ("upper", 2002.14187676668)]),
            ),
            (
                "Brain-Stem",
                dict([("lower", 18048.54263155760), ("upper", 25300.51090318110)]),
            ),
            (
                "Left-Caudate",
                dict([("lower", 2702.73311142764), ("upper", 4380.54479618196)]),
            ),
            (
                "Right-Caudate",
                dict([("lower", 2569.61140834210), ("upper", 4412.61035536070)]),
            ),
            (
                "Left-Hippocampus",
                dict([("lower", 3432.26483953083), ("upper", 4934.43236139507)]),
            ),
            (
                "Right-Hippocampus",
                dict([("lower", 3580.74371035841), ("upper", 5067.49668145829)]),
            ),
            (
                "Left-Pallidum",
                dict([("lower", 935.47686324176), ("upper", 1849.42861796994)]),
            ),
            (
                "Right-Pallidum",
                dict([("lower", 1078.14975428593), ("upper", 1864.08951102817)]),
            ),
            (
                "Left-Putamen",
                dict([("lower", 3956.23134409153), ("upper", 6561.97642872937)]),
            ),
            (
                "Right-Putamen",
                dict([("lower", 3768.88684356957), ("upper", 6142.52870810603)]),
            ),
            (
                "Left-Thalamus-Proper",
                dict([("lower", 6483.36121320953), ("upper", 9489.46749012527)]),
            ),
            (
                "Right-Thalamus-Proper",
                dict([("lower", 6065.70220487045), ("upper", 8346.88382091555)]),
            ),
            (
                "Left-VentralDC",
                dict([("lower", 3182.42264293449), ("upper", 4495.77412707751)]),
            ),
            (
                "Right-VentralDC",
                dict([("lower", 3143.88280953869), ("upper", 4407.63641978371)]),
            ),
        ]
    )

    # return
    return outlierDict


# ------------------------------------------------------------------------------
# main function


def outlierDetection(
    subjects,
    subjects_dir,
    output_dir,
    outlierDict,
    min_no_subjects=10,
    hypothalamus=False,
    hippocampus=False,
    hippocampus_label=None,
    fastsurfer=False,
):
    """
    Evaluate outliers in aseg.stats, [lr]h.aparc, and optional hypothalamic/hippocampal values.

    Parameters
    ----------
    subjects : list
        List of subject IDs.
    subjects_dir : str
        Path to the FreeSurfer subjects directory.
    output_dir : str
        Path to the output directory for saving results.
    outlierDict : dict
        Dictionary containing outlier thresholds for different measures.
    min_no_subjects : int, optional
        Minimum number of subjects required for analysis.
    hypothalamus : bool, optional
        Flag to include hypothalamic values in the analysis.
    hippocampus : bool, optional
        Flag to include hippocampal values in the analysis.
    hippocampus_label : str or None, optional
        Label to identify the hippocampus (e.g., "Hippocampus").
    fastsurfer : bool, optional
        Flag to use FastSurfer instead of FreeSurfer output files.

    Returns
    -------
    tuple
        A tuple containing three dictionaries:

        - outlierSampleNonparNum
        - outlierSampleParamNum
        - outlierNormsNum
    """
    # imports

    import csv
    import os

    import numpy as np
    import pandas as pd

    # create a dictionary with all data from all subjects, and create a list of all available keys

    regions = dict()

    all_regions_keys = list()

    for subject in subjects:
        # aseg
        path_aseg_stats = os.path.join(subjects_dir, subject, "stats", "aseg.stats")
        aseg_stats = readAsegStats(path_aseg_stats)
        regions[subject] = aseg_stats.copy()
        all_regions_keys.extend(list(aseg_stats.keys()))

        # aparc
        if fastsurfer is True:
            path_aparc_stats = os.path.join(
                subjects_dir, subject, "stats", "lh.aparc.DKTatlas.mapped.stats"
            )
        else:
            path_aparc_stats = os.path.join(
                subjects_dir, subject, "stats", "lh.aparc.stats"
            )
        aparc_header, aparc_stats, aparc_thickness = readAparcStats(
            path_aparc_stats, hemi="lh"
        )
        regions[subject].update(aparc_thickness)
        all_regions_keys.extend(list(aparc_thickness.keys()))

        if fastsurfer is True:
            path_aparc_stats = os.path.join(
                subjects_dir, subject, "stats", "rh.aparc.DKTatlas.mapped.stats"
            )
        else:
            path_aparc_stats = os.path.join(
                subjects_dir, subject, "stats", "rh.aparc.stats"
            )
        aparc_header, aparc_stats, aparc_thickness = readAparcStats(
            path_aparc_stats, hemi="rh"
        )
        regions[subject].update(aparc_thickness)
        all_regions_keys.extend(list(aparc_thickness.keys()))

        # hypothalamus

        if hypothalamus is True:
            path_hypothalamus_stats = os.path.join(
                subjects_dir, subject, "mri", "hypothalamic_subunits_volumes.v1.csv"
            )
            if os.path.exists(path_hypothalamus_stats):
                hypothalamus_stats = readHypothalamusStats(path_hypothalamus_stats)
                regions[subject].update(hypothalamus_stats)
                all_regions_keys.extend(list(hypothalamus_stats.keys()))

        # hippocampus + amygdala

        if hippocampus is True and hippocampus_label is not None:
            path_hippocampus_stats = os.path.join(
                subjects_dir,
                subject,
                "mri",
                "lh.hippoSfVolumes-" + hippocampus_label + ".txt",
            )
            if os.path.exists(path_hippocampus_stats):
                hippocampus_stats = readHippocampusStats(
                    path_hippocampus_stats, hemi="lh", prefix="hippocampus"
                )
                regions[subject].update(hippocampus_stats)
                all_regions_keys.extend(list(hippocampus_stats.keys()))

            path_hippocampus_stats = os.path.join(
                subjects_dir,
                subject,
                "mri",
                "rh.hippoSfVolumes-" + hippocampus_label + ".txt",
            )
            if os.path.exists(path_hippocampus_stats):
                hippocampus_stats = readHippocampusStats(
                    path_hippocampus_stats, hemi="rh", prefix="hippocampus"
                )
                regions[subject].update(hippocampus_stats)
                all_regions_keys.extend(list(hippocampus_stats.keys()))

            path_hippocampus_stats = os.path.join(
                subjects_dir,
                subject,
                "mri",
                "lh.amygNucVolumes-" + hippocampus_label + ".txt",
            )
            if os.path.exists(path_hippocampus_stats):
                hippocampus_stats = readHippocampusStats(
                    path_hippocampus_stats, hemi="lh", prefix="amygdala"
                )
                regions[subject].update(hippocampus_stats)
                all_regions_keys.extend(list(hippocampus_stats.keys()))

            path_hippocampus_stats = os.path.join(
                subjects_dir,
                subject,
                "mri",
                "rh.amygNucVolumes-" + hippocampus_label + ".txt",
            )
            if os.path.exists(path_hippocampus_stats):
                hippocampus_stats = readHippocampusStats(
                    path_hippocampus_stats, hemi="rh", prefix="amygdala"
                )
                regions[subject].update(hippocampus_stats)
                all_regions_keys.extend(list(hippocampus_stats.keys()))

    # sort keys

    all_regions_keys = set(all_regions_keys)

    all_regions_keys = (
        sorted(list(filter(lambda x: "aseg." in x, list(all_regions_keys))))
        + sorted(list(filter(lambda x: "aparc." in x, list(all_regions_keys))))
        + sorted(list(filter(lambda x: "hippocampus." in x, list(all_regions_keys))))
        + sorted(list(filter(lambda x: "amygdala." in x, list(all_regions_keys))))
        + sorted(list(filter(lambda x: "hypothalamus." in x, list(all_regions_keys))))
    )

    # compare individual data against sample statistics (if more than min_no_subjects cases)

    outlierSampleNonpar = dict()
    outlierSampleParam = dict()

    outlierSampleNonparNum = dict()
    outlierSampleParamNum = dict()

    if len(subjects) >= min_no_subjects:
        # compute means, sd, medians, and quantiles based on sample

        df = pd.DataFrame.from_dict(regions).transpose()

        iqr = np.percentile(df, 75, axis=0) - np.percentile(df, 25, axis=0)

        sample_nonpar_lower = dict(
            zip(df.columns, np.percentile(df, 25, axis=0) - 1.5 * iqr)
        )
        sample_nonpar_upper = dict(
            zip(df.columns, np.percentile(df, 75, axis=0) + 1.5 * iqr)
        )

        sample_param_lower = dict(np.mean(df, axis=0) - 2 * np.std(df, axis=0))
        sample_param_upper = dict(np.mean(df, axis=0) + 2 * np.std(df, axis=0))

        # compare individual data against sample statistics

        for subject in regions:
            nonparDict = dict()
            paramDict = dict()

            for key in regions[subject]:
                if (regions[subject][key] < sample_nonpar_lower[key]) or (
                    regions[subject][key] > sample_nonpar_upper[key]
                ):
                    nonparDict.update({key: True})
                else:
                    nonparDict.update({key: False})

                if (regions[subject][key] < sample_param_lower[key]) or (
                    regions[subject][key] > sample_param_upper[key]
                ):
                    paramDict.update({key: True})
                else:
                    paramDict.update({key: False})

            outlierSampleNonpar.update({subject: nonparDict})
            outlierSampleParam.update({subject: paramDict})

            outlierSampleNonparNum.update({subject: np.sum(list(nonparDict.values()))})
            outlierSampleParamNum.update({subject: np.sum(list(paramDict.values()))})

    else:
        for subject in regions:
            nonparDict = dict()
            paramDict = dict()

            for key in regions[subject]:
                nonparDict.update({key: np.nan})
                paramDict.update({key: np.nan})

            outlierSampleNonpar.update({subject: nonparDict})
            outlierSampleParam.update({subject: paramDict})

            outlierSampleNonparNum.update({subject: np.nan})
            outlierSampleParamNum.update({subject: np.nan})

    # compare individual data against normative values

    outlierNorms = dict()

    outlierNormsNum = dict()

    for subject in regions:
        normsDict = dict()

        for key in regions[subject]:
            # no prefixes in outlier table
            if key.startswith("aseg."):
                outlierKey = key.replace("aseg.", "")
            elif key.startswith("aparc."):
                outlierKey = key.replace("aparc.", "")
            elif key.startswith("hippocampus."):
                outlierKey = key.replace("hippocampus.", "")
            elif key.startswith("amygdala."):
                outlierKey = key.replace("amygdala.", "")
            elif key.startswith("hypothalamus."):
                outlierKey = key.replace("aseg.", "")

            if outlierKey in outlierDict:
                if (regions[subject][key] < outlierDict[outlierKey]["lower"]) or (
                    regions[subject][key] > outlierDict[outlierKey]["upper"]
                ):
                    normsDict.update({key: True})
                else:
                    normsDict.update({key: False})

            else:
                normsDict.update({key: np.nan})

        outlierNorms.update({subject: normsDict})

        outlierNormsNum.update({subject: np.nansum(list(normsDict.values()))})

    # write to csv files

    regionsFieldnames = ["subject"]
    regionsFieldnames.extend(all_regions_keys)

    with open(os.path.join(output_dir, "all.regions.stats"), "w") as datafile:
        csvwriter = csv.DictWriter(
            datafile,
            fieldnames=regionsFieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        csvwriter.writeheader()
        for subject in sorted(list(regions.keys())):
            tmp = regions[subject]
            tmp.update({"subject": subject})
            csvwriter.writerow(tmp)

    with open(
        os.path.join(output_dir, "all.outliers.sample.nonpar.stats"), "w"
    ) as datafile:
        csvwriter = csv.DictWriter(
            datafile,
            fieldnames=regionsFieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        csvwriter.writeheader()
        for subject in sorted(list(outlierSampleNonpar.keys())):
            tmp = outlierSampleNonpar[subject]
            tmp.update({"subject": subject})
            csvwriter.writerow(tmp)

    with open(
        os.path.join(output_dir, "all.outliers.sample.param.stats"), "w"
    ) as datafile:
        csvwriter = csv.DictWriter(
            datafile,
            fieldnames=regionsFieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        csvwriter.writeheader()
        for subject in sorted(list(outlierSampleParam.keys())):
            tmp = outlierSampleParam[subject]
            tmp.update({"subject": subject})
            csvwriter.writerow(tmp)

    with open(os.path.join(output_dir, "all.outliers.norms.stats"), "w") as datafile:
        csvwriter = csv.DictWriter(
            datafile,
            fieldnames=regionsFieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        csvwriter.writeheader()
        for subject in sorted(list(outlierNorms.keys())):
            tmp = outlierNorms[subject]
            tmp.update({"subject": subject})
            csvwriter.writerow(tmp)

    # return

    return outlierSampleNonparNum, outlierSampleParamNum, outlierNormsNum
