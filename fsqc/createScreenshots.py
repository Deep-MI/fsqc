"""
This module provides a function to create screenshots

"""

# -----------------------------------------------------------------------------


def createScreenshots(
    SUBJECT,
    SUBJECTS_DIR,
    OUTFILE,
    INTERACTIVE=True,
    LAYOUT="default",
    BASE="default",
    OVERLAY="default",
    LABELS=None,
    SURF="default",
    SURFCOLOR="default",
    VIEWS="default",
    XLIM=None,
    YLIM=None,
    BINARIZE=False,
    ORIENTATION="radiological",
):
    """
    Function to create screenshots.

    Parameters
    ----------
    SUBJECT : str
        The subject.
    SUBJECTS_DIR : str
        The subjects directory.
    OUTFILE : str
        The output file path.
    INTERACTIVE : bool, optional
        Flag for interactive mode, default is True.
    LAYOUT : list, optional
        The layout, default is "default".
    BASE : str, optional
        The base, default is "default".
        Load norm.mgz as default.
    OVERLAY : str, optional
        The overlay, default is "default".
        Load aseg.mgz as default.
        Can be None.
    LABELS : None or str, optional
        The labels, default is None.
    SURF : list, optional
        The surface, default is "default".
        Can be None.
    SURFCOLOR : list, optional
        The surface color, default is "default".
        Can be None.
    VIEWS : list, optional
        The views, default is "default".
    XLIM : None or list, optional
        The x limits, default is None.
    YLIM : None or list, optional
        The y limits, default is None.
    BINARIZE : bool, optional
        Flag for binarization, default is False.
    ORIENTATION : str, optional
        The orientation, default is "radiological".

    Notes
    -----
    LAYOUT, VIEWS can be lists or "default".

    SURF, SURFCOLOR can be lists, None, or "default".

    XLIM, YLIM can be lists of list two-element numeric lists or None; if given,
    length must match length of VIEWS. x and y refer to final image dimensions,
    not MR volume dimensions.
    """
    # -----------------------------------------------------------------------------
    # auxiliary functions

    def computeLayout(n):
        import numpy as np

        y = np.ceil(np.sqrt(n))

        x = y - np.divmod(y**2 - n, y)[0]

        return int(x), int(y)

    # -----------------------------------------------------------------------------
    # imports

    import logging
    import os
    import warnings

    import matplotlib
    import nibabel as nb
    import numpy as np

    if not INTERACTIVE:
        matplotlib.use("Agg")

    from matplotlib import pyplot as plt

    from fsqc.fsqcUtils import levelsetsTria, returnFreeSurferColorLUT

    # -----------------------------------------------------------------------------
    # settings

    logging.captureWarnings(True)

    FIGSIZE = 8

    FIGDPI = 100

    ALPHA = 0.5

    tol = 1e-16

    # -----------------------------------------------------------------------------
    # import image data

    if BASE == "default":
        norm = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz"))
    else:
        norm = nb.load(BASE)

    if OVERLAY is None:
        aseg = None
    elif OVERLAY == "default":
        aseg = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "aseg.mgz"))
    else:
        aseg = nb.load(OVERLAY)

    # -----------------------------------------------------------------------------
    # import surface data

    if SURF == "default":
        surflist = [
            os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "lh.white"),
            os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "rh.white"),
            os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "lh.pial"),
            os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "rh.pial"),
        ]
    else:
        surflist = SURF

    if SURF is None:
        surfcolor = None
    elif SURFCOLOR == "default" and SURF == "default":
        surfcolor = ["yellow", "yellow", "red", "red"]
    elif SURFCOLOR == "default" and SURF != "default":
        surfcolor = ["yellow"] * len(surflist)
    else:
        surfcolor = SURFCOLOR

    surf = list()

    if surflist is not None and surfcolor is not None:
        for i in range(len(surflist)):
            surf.append(nb.freesurfer.io.read_geometry(surflist[i], read_metadata=True))

    # -----------------------------------------------------------------------------
    # import colortable, compute auxiliary variables, and transform to matplotlib
    # colortable

    lut = returnFreeSurferColorLUT()

    # some fs7 labels are not present in fs6 LUT, check and add if necessary

    if not (
        np.isin(
            list(range(231, 247)) + [801, 802, 803, 804, 805, 806, 807, 808, 809, 810],
            lut[:, 0],
        ).all()
    ):
        lutAdd = np.array(
            (
                [801, "L_hypothalamus_anterior_inferior", 250, 255, 50, 0],
                [802, "L_hypothalamus_anterior_superior", 80, 200, 255, 0],
                [803, "L_hypothalamus_posterior", 255, 160, 0, 0],
                [804, "L_hypothalamus_tubular_inferior", 255, 160, 200, 0],
                [805, "L_hypothalamus_tubular_superior", 20, 180, 130, 0],
                [806, "R_hypothalamus_anterior_inferior", 250, 255, 50, 0],
                [807, "R_hypothalamus_anterior_superior", 80, 200, 255, 0],
                [808, "R_hypothalamus_posterior", 255, 160, 0, 0],
                [809, "R_hypothalamus_tubular_inferior", 255, 160, 200, 0],
                [810, "R_hypothalamus_tubular_superior", 20, 180, 130, 0],
                [231, "HP_body", 0, 255, 0, 0],
                [232, "HP_head", 255, 0, 0, 0],
                [233, "presubiculum-head", 32, 0, 32, 0],
                [234, "presubiculum-body", 64, 0, 64, 0],
                [235, "subiculum-head", 0, 0, 175, 0],
                [236, "subiculum-body", 0, 0, 255, 0],
                [237, "CA1-head", 175, 75, 75, 0],
                [238, "CA1-body", 255, 0, 0, 0],
                [239, "CA3-head", 0, 80, 0, 0],
                [240, "CA3-body", 0, 128, 0, 0],
                [241, "CA4-head", 120, 90, 50, 0],
                [242, "CA4-body", 196, 160, 128, 0],
                [243, "GC-ML-DG-head", 75, 125, 175, 0],
                [244, "GC-ML-DG-body", 32, 200, 255, 0],
                [245, "molecular_layer_HP-head", 100, 25, 25, 0],
                [246, "molecular_layer_HP-body", 128, 0, 0, 0],
            ),
            dtype=object,
        )

        lut = np.concatenate((lut, lutAdd), axis=0)

    lutEnum = dict(zip(lut[:, 0], range(len(lut[:, 0]))))

    lutTab = np.array(lut[:, (2, 3, 4, 5)] / 255, dtype="float32")
    lutTab[:, 3] = 1

    lutMap = matplotlib.colors.ListedColormap(lutTab)

    # -----------------------------------------------------------------------------
    # determine VIEWS

    if VIEWS == "default":
        CutsRRAS = [("x", -10), ("x", 10), ("y", 0), ("z", 0)]
    else:
        CutsRRAS = VIEWS

    # -----------------------------------------------------------------------------
    # check if the chosen VIEWS are feasible. If not feasible changing to the nearest feasible values

    m = norm.header.get_vox2ras_tkr()
    n = norm.header.get_data_shape()

    xyzIdx = np.array(
        np.meshgrid(
            np.linspace(0, n[0] - 1, n[0]),
            np.linspace(0, n[1] - 1, n[1]),
            np.linspace(0, n[2] - 1, n[2]),
        )
    )
    xyzIdxFlat3 = np.reshape(xyzIdx, (3, np.prod(n))).transpose()
    xyzIdxFlat4 = np.hstack((xyzIdxFlat3, np.ones((np.prod(n), 1))))
    rasIdxFlat3 = np.matmul(m, xyzIdxFlat4.transpose()).transpose()[:, 0:3]

    for i, icr in enumerate(CutsRRAS):
        if icr[0] == "x":
            iDim = 0
        elif icr[0] == "y":
            iDim = 1
        elif icr[0] == "z":
            iDim = 2

        if not np.any(rasIdxFlat3[:, iDim] == icr[1]):
            closestCutValue = rasIdxFlat3[
                np.abs(rasIdxFlat3[:, iDim] - icr[1]).argmin(), iDim
            ]
            logging.info(
                f"INFO: the VIEW {icr} will be changed to ('{icr[0]}', {closestCutValue:.2f}) so it is not"
                " necessary to interpolate volumetric data"
            )
            CutsRRAS[i] = (icr[0], closestCutValue)

    # -----------------------------------------------------------------------------
    # compute levelsets

    LVL = list()

    # will not run if surf is empty (intended)
    for s in range(len(surf)):
        sLVL = list()

        for i in range(len(CutsRRAS)):
            # determine dimension
            if CutsRRAS[i][0] == "x":
                iDim = 0
            elif CutsRRAS[i][0] == "y":
                iDim = 1
            elif CutsRRAS[i][0] == "z":
                iDim = 2

            # compute levelsets: e.g., LVL[SURF][VIEWS][vLVL|tLVL|iLVL][0][elementDim1][elementDim2]
            sLVL.append(
                levelsetsTria(
                    surf[s][0], surf[s][1], surf[s][0][:, iDim], CutsRRAS[i][1]
                )
            )

        LVL.append(sLVL)

    # -----------------------------------------------------------------------------
    # get data for norm

    normData = norm.get_fdata()

    normVals = normData

    # -----------------------------------------------------------------------------
    # get data for aseg and change to enumerated aseg so that it can be used as
    # index to lutMap

    if aseg is not None:
        asegData = aseg.get_fdata()

        if LABELS is not None:
            asegData = asegData * np.isin(asegData, LABELS)

        if BINARIZE is True:
            asegData = (asegData > 0).astype(int)

        asegUnique, asegIdx = np.unique(asegData, return_inverse=True)

        asegEnum = np.array([lutEnum[x] for x in asegUnique])

        asegVals = np.reshape(asegEnum[asegIdx], (aseg.shape))

    # -----------------------------------------------------------------------------
    # compile image data for plotting

    # note that we are using the TkReg RAS system, not RAS per se
    # this is because the surfaces are in TkReg RAS also

    # one considerable advantage of the (TkReg) RAS system is that it is solely
    # based on switching dimensions, not rotating at odd angles etc, so no need
    # for interpolating.

    # x_R y_R z_R c_R
    # x_A y_A z_A c_A
    # x_S y_S z_S c_S
    #   0   0   0   1

    # m = norm.header.get_vox2ras_tkr()
    # n = norm.header.get_data_shape()

    # xyzIdx = np.array(np.meshgrid(np.linspace(0, n[0] - 1, n[0]), np.linspace(0, n[1] - 1, n[1]), np.linspace(0, n[2] - 1, n[2])))
    # xyzIdxFlat3 = np.reshape(xyzIdx, (3, np.prod(n))).transpose()
    # xyzIdxFlat4 = np.hstack((xyzIdxFlat3, np.ones((np.prod(n), 1))))
    # rasIdxFlat3 = np.matmul(m, xyzIdxFlat4.transpose()).transpose()[:, 0:3]

    normValsRAS = list()
    if aseg is not None:
        asegValsRAS = list()

    for i in range(len(CutsRRAS)):
        # determine dimension
        if CutsRRAS[i][0] == "x":
            iDim = 0
        elif CutsRRAS[i][0] == "y":
            iDim = 1
        elif CutsRRAS[i][0] == "z":
            iDim = 2

        sel = np.array(
            xyzIdxFlat3[rasIdxFlat3[:, iDim] == CutsRRAS[i][1], :], dtype="int"
        )
        normValsRAS.append(
            np.squeeze(
                normVals[
                    np.min(sel[:, 0]) : np.max(sel[:, 0]) + 1,
                    np.min(sel[:, 1]) : np.max(sel[:, 1]) + 1,
                    np.min(sel[:, 2]) : np.max(sel[:, 2]) + 1,
                ]
            )
        )
        if aseg is not None:
            asegValsRAS.append(
                np.squeeze(
                    asegVals[
                        np.min(sel[:, 0]) : np.max(sel[:, 0]) + 1,
                        np.min(sel[:, 1]) : np.max(sel[:, 1]) + 1,
                        np.min(sel[:, 2]) : np.max(sel[:, 2]) + 1,
                    ]
                )
            )

    # -----------------------------------------------------------------------------
    # plotting: create a new figure, plot into it, then close it so it never gets
    # displayed

    # turn interactive plotting off unless interactive
    if not INTERACTIVE:
        plt.ioff()

    # compute layout
    if LAYOUT == "default":
        myLayout = computeLayout(len(CutsRRAS))
    else:
        myLayout = LAYOUT

    # create list of de-facto layouts
    myLayoutList = list()
    for axsx in range(myLayout[0]):
        for axsy in range(myLayout[1]):
            myLayoutList.append((axsx, axsy))

    # create subplots
    fig, axs = plt.subplots(myLayout[0], myLayout[1])
    axs = np.reshape(axs, myLayout)

    # adjust layout
    fig.set_size_inches([FIGSIZE * myLayout[1], FIGSIZE * myLayout[0]])
    fig.set_dpi(FIGDPI)
    fig.set_facecolor("black")
    fig.set_tight_layout({"pad": 0})
    fig.subplots_adjust(wspace=0)

    # -----------------------------------------------------------------------------
    # plot each panel

    for p in range(len(CutsRRAS)):
        logging.info("Panel " + str(p))

        axsx = myLayoutList[p][0]
        axsy = myLayoutList[p][1]

        # determine dimensions
        if CutsRRAS[p][0] == "x":
            # x axis of the image should be towards anterior, y axis should be towards superior in RAS image
            dims = (1, 2)
            # determine extent
            extent = (
                rasIdxFlat3[0, dims[0]],
                rasIdxFlat3[-1, dims[0]],
                rasIdxFlat3[0, dims[1]],
                rasIdxFlat3[-1, dims[1]],
            )
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            cor = np.where(m[dims[0], 0:3])[0]
            axi = np.where(m[dims[1], 0:3])[0]
            #
            if axi < cor:
                axs[axsx, axsy].imshow(
                    normValsRAS[p], cmap="gray", origin="lower", extent=extent
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p] + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )
            else:
                axs[axsx, axsy].imshow(
                    normValsRAS[p].transpose(),
                    cmap="gray",
                    origin="lower",
                    extent=extent,
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p].transpose() + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )
        elif CutsRRAS[p][0] == "y":
            # x axis of the image should be towards right, y axis should be towards superior in RAS image
            dims = (0, 2)
            # determine extent
            extent = (
                rasIdxFlat3[0, dims[0]],
                rasIdxFlat3[-1, dims[0]],
                rasIdxFlat3[0, dims[1]],
                rasIdxFlat3[-1, dims[1]],
            )
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            sag = np.where(m[dims[0], 0:3])[0]
            axi = np.where(m[dims[1], 0:3])[0]
            #
            if axi < sag:
                axs[axsx, axsy].imshow(
                    normValsRAS[p], cmap="gray", origin="lower", extent=extent
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p] + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )
            else:
                axs[axsx, axsy].imshow(
                    normValsRAS[p].transpose(),
                    cmap="gray",
                    origin="lower",
                    extent=extent,
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p].transpose() + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )
        elif CutsRRAS[p][0] == "z":
            # x axis of the image should be towards right, y axis should be towards anterior in RAS image
            dims = (0, 1)
            # determine extent
            extent = (
                rasIdxFlat3[0, dims[0]],
                rasIdxFlat3[-1, dims[0]],
                rasIdxFlat3[0, dims[1]],
                rasIdxFlat3[-1, dims[1]],
            )
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            sag = np.where(m[dims[0], 0:3])[0]
            cor = np.where(m[dims[1], 0:3])[0]
            if cor < sag:
                axs[axsx, axsy].imshow(
                    normValsRAS[p], cmap="gray", origin="lower", extent=extent
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p] + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )
            else:
                axs[axsx, axsy].imshow(
                    normValsRAS[p].transpose(),
                    cmap="gray",
                    origin="lower",
                    extent=extent,
                )
                if aseg is not None:
                    axs[axsx, axsy].imshow(
                        asegValsRAS[p].transpose() + 0.5,
                        cmap=lutMap,
                        origin="lower",
                        extent=extent,
                        vmin=0,
                        vmax=len(lutTab),
                        alpha=ALPHA,
                    )

        # prepare plot
        if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
            axs[axsx, axsy].invert_xaxis()
        if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
            axs[axsx, axsy].invert_yaxis()

        axs[axsx, axsy].set_axis_off()
        axs[axsx, axsy].set_aspect("equal")

        if XLIM is not None:
            axs[axsx, axsy].set_xlim(XLIM[p])

        if YLIM is not None:
            axs[axsx, axsy].set_ylim(YLIM[p])

        # determine left-right orientation for coronal and axial views
        if ORIENTATION == "radiological":
            if CutsRRAS[p][0] == "y" or CutsRRAS[p][0] == "z":
                axs[axsx, axsy].invert_xaxis()

        # now plot
        for s in range(len(surf)):
            if len(LVL[s][p][0][0]) > 0:
                logging.info("Surface " + str(s))

                # create array of line segments
                tmpx = list()
                tmpy = list()

                for i in range(len(LVL[s][p][1][0])):
                    tmpx.append(
                        (
                            LVL[s][p][0][0][LVL[s][p][1][0][i][0] - 1][dims[0]],
                            LVL[s][p][0][0][LVL[s][p][1][0][i][1] - 1][dims[0]],
                        )
                    )
                    tmpy.append(
                        (
                            LVL[s][p][0][0][LVL[s][p][1][0][i][0] - 1][dims[1]],
                            LVL[s][p][0][0][LVL[s][p][1][0][i][1] - 1][dims[1]],
                        )
                    )

                tmpx = np.array(tmpx)
                tmpy = np.array(tmpy)

                # remove duplicate points
                tmpxy = np.unique(np.concatenate((tmpx, tmpy), axis=1), axis=0)
                tmpx = tmpxy[:, 0:2]
                tmpy = tmpxy[:, 2:4]

                # remove segments which are de-facto points
                tmpIdx = np.logical_or(
                    np.abs(tmpx[:, 0] - tmpx[:, 1]) > tol,
                    np.abs(tmpy[:, 0] - tmpy[:, 1]) > tol,
                )
                tmpx = tmpx[tmpIdx, :]
                tmpy = tmpy[tmpIdx, :]

                # need to order array of line segments; whenever we encounter a
                # closed loop, we will already plot; otherwise, plot in the end
                sortIdx = np.array(range(0, len(tmpx)))

                tmpxSort = np.array(tmpx[sortIdx[0],], ndmin=2)
                tmpySort = np.array(tmpy[sortIdx[0],], ndmin=2)

                sortIdx = np.delete(sortIdx, sortIdx[0])

                while len(sortIdx) > 1:
                    findIdx = np.array(
                        np.where(
                            np.logical_and(
                                np.abs(
                                    tmpx[sortIdx,] - tmpxSort[tmpxSort.shape[0] - 1, 1]
                                )
                                < tol,
                                np.abs(
                                    tmpy[sortIdx,] - tmpySort[tmpySort.shape[0] - 1, 1]
                                )
                                < tol,
                            )
                        ),
                        ndmin=2,
                    ).T

                    # delete existing finds
                    findIdxKeep = list()
                    for k in range(findIdx.shape[0]):
                        if not np.any(
                            np.all(
                                np.logical_or(
                                    tmpx[sortIdx[findIdx[k, 0]], 0] == tmpxSort,
                                    tmpx[sortIdx[findIdx[k, 0]], 1] == tmpxSort,
                                ),
                                axis=1,
                            )
                        ):
                            findIdxKeep.append(k)
                    findIdx = findIdx[findIdxKeep,]

                    if findIdx.shape[0] == 0:
                        # close loop and plot already
                        axs[axsx, axsy].plot(
                            tmpxSort,
                            tmpySort,
                            color=surfcolor[s],
                            linewidth=np.round(FIGSIZE / 8),
                        )
                        # reset (start new loop)
                        tmpxSort = np.array(tmpx[sortIdx[0],], ndmin=2)
                        tmpySort = np.array(tmpy[sortIdx[0],], ndmin=2)
                        sortIdx = np.delete(sortIdx, 0)
                    elif findIdx.shape[0] == 1:
                        # add to current set
                        if findIdx[0, 1] == 0:
                            tmpxSort = np.append(
                                tmpxSort,
                                np.array(tmpx[sortIdx[findIdx[0, 0]], ::1], ndmin=2),
                                axis=0,
                            )
                            tmpySort = np.append(
                                tmpySort,
                                np.array(tmpy[sortIdx[findIdx[0, 0]], ::1], ndmin=2),
                                axis=0,
                            )
                        elif findIdx[0, 1] == 1:
                            tmpxSort = np.append(
                                tmpxSort,
                                np.array(tmpx[sortIdx[findIdx[0, 0]], ::-1], ndmin=2),
                                axis=0,
                            )
                            tmpySort = np.append(
                                tmpySort,
                                np.array(tmpy[sortIdx[findIdx[0, 0]], ::-1], ndmin=2),
                                axis=0,
                            )
                        sortIdx = np.delete(sortIdx, findIdx[0, 0])
                    elif findIdx.shape[0] > 1:
                        warnings.warn(
                            "WARNING: a problem occurred with the surface overlays",
                            stacklevel = 2
                        )
                # now final plot
                axs[axsx, axsy].plot(
                    tmpxSort,
                    tmpySort,
                    color=surfcolor[s],
                    linewidth=np.round(FIGSIZE / 8),
                )

    # -----------------------------------------------------------------------------
    # output

    if not INTERACTIVE:
        plt.savefig(OUTFILE, facecolor=fig.get_facecolor())
        plt.close(fig)

    # -----------------------------------------------------------------------------
    #
