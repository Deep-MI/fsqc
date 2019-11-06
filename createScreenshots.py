def createScreenshots(SUBJECT, SUBJECTS_DIR, OUTFILE, INTERACTIVE=True, VIEWS=[('x',-10),('x',10),('y',0),('z',0)], LAYOUT=None):

    """
    function createScreenshots()
    
    Requires FREESURFER_HOME environment variable 

    """

    # -----------------------------------------------------------------------------
    # TODO

    # - possibly add option to determine which surface(s) should be plotted in 
    #   which color
    # - talairch?
    # - remove white background
    # - add linewidth parameter

    # -----------------------------------------------------------------------------
    # auxiliary functions

    def computeLayout(n):
        
        import numpy as np
        
        y = np.ceil(np.sqrt(n))
        
        x = y - np.divmod(y**2 - n, y)[0]
        
        return int(x), int(y)

    # -----------------------------------------------------------------------------
    # imports

    import os

    import pandas as pd

    import numpy as np
    import nibabel as nb

    import matplotlib

    if not INTERACTIVE:
        matplotlib.use('Agg')

    from matplotlib import pyplot as plt

    from levelsetsTria import levelsetsTria

    # -----------------------------------------------------------------------------
    # settings

    CutsRRAS = VIEWS

    FIGSIZE = 32

    FIGDPI = 100

    ALPHA = 0.5

    # -----------------------------------------------------------------------------
    # import image data

    norm = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, 'mri', 'norm.mgz'))

    aseg = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, 'mri', 'aseg.mgz'))

    # -----------------------------------------------------------------------------
    # import surface data

    lhWhite = nb.freesurfer.io.read_geometry(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.white'), read_metadata=True)
    rhWhite = nb.freesurfer.io.read_geometry(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.white'), read_metadata=True)

    lhPial = nb.freesurfer.io.read_geometry(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.pial'), read_metadata=True)
    rhPial = nb.freesurfer.io.read_geometry(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.pial'), read_metadata=True)

    # -----------------------------------------------------------------------------
    # import colortable, compute auxiliary variables, and transform to matplotlib
    # colortable

    lut = pd.read_csv(os.path.join(os.environ['FREESURFER_HOME'],'FreeSurferColorLUT.txt'),
                      sep=' ',
                      comment='#',
                      header=None,
                      skipinitialspace=True,
                      skip_blank_lines=True,
                      error_bad_lines=False,
                      warn_bad_lines=True
                      )

    lut = np.array(lut)

    lutEnum = dict(zip(lut[:, 0], range(len(lut[:, 0]))))

    lutTab = np.array(lut[:, (2, 3, 4, 5)] / 255, dtype="float32")
    lutTab[:, 3] = 1

    lutMap = matplotlib.colors.ListedColormap(lutTab)

    # -----------------------------------------------------------------------------
    # compute levelsets

    lhWhiteLVL=list()
    rhWhiteLVL=list()
    lhPialLVL=list()
    rhPialLVL=list()

    for i in range(len(CutsRRAS)):
        
        # determine dimension
        if CutsRRAS[i][0] is 'x':
            iDim = 0
        elif CutsRRAS[i][0] is 'y':
            iDim = 1
        elif CutsRRAS[i][0] is 'z':
            iDim = 2

        # compute levelsets: e.g., lhWhiteLVL[VIEWS][vLVL|tLVL|iLVL][0][elementDim1][elementDim2]
        lhWhiteLVL.append(levelsetsTria(lhWhite[0], lhWhite[1], lhWhite[0][:, iDim], CutsRRAS[i][1]))
        rhWhiteLVL.append(levelsetsTria(rhWhite[0], rhWhite[1], rhWhite[0][:, iDim], CutsRRAS[i][1]))
        lhPialLVL.append(levelsetsTria(lhPial[0],  lhPial[1],  lhPial[0][:, iDim],  CutsRRAS[i][1]))
        rhPialLVL.append(levelsetsTria(rhPial[0],  rhPial[1],  rhPial[0][:, iDim],  CutsRRAS[i][1]))

    # -----------------------------------------------------------------------------
    # get data for norm

    normData = norm.get_data()

    normVals = normData

    # -----------------------------------------------------------------------------
    # get data for aseg and change to enumerated aseg so that it can be used as
    # index to lutMap

    asegData = aseg.get_data()

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

    m = aseg.header.get_vox2ras_tkr()
    n = aseg.header.get_data_shape()

    xyzIdx = np.array(np.meshgrid(np.linspace(0, n[0] - 1, n[0]), np.linspace(0, n[1] - 1, n[1]), np.linspace(0, n[2] - 1, n[2])))
    xyzIdxFlat3 = np.reshape(xyzIdx, (3, np.prod(n))).transpose()
    xyzIdxFlat4 = np.hstack((xyzIdxFlat3, np.ones((np.prod(n), 1))))
    rasIdxFlat3 = np.matmul(m, xyzIdxFlat4.transpose()).transpose()[:, 0:3]

    normValsRAS = list()
    asegValsRAS = list()

    for i in range(len(CutsRRAS)):
        
        # determine dimension
        if CutsRRAS[i][0] is 'x':
            iDim = 0
        elif CutsRRAS[i][0] is 'y':
            iDim = 1
        elif CutsRRAS[i][0] is 'z':
            iDim = 2

        #
        sel = np.array(xyzIdxFlat3[rasIdxFlat3[:, iDim] == CutsRRAS[i][1], :], dtype="int")
        normValsRAS.append(np.squeeze(normVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1]))
        asegValsRAS.append(np.squeeze(asegVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1]))

    # -----------------------------------------------------------------------------
    # plotting: create a new figure, plot into it, then close it so it never gets
    # displayed

    # turn interactive plotting off unless interactive
    if not INTERACTIVE:
        plt.ioff()

    # compute layout
    if LAYOUT is None:
        myLayout = computeLayout(len(CutsRRAS))
    else:
        myLayout = LAYOUT

    myLayoutList = list()
    for axsx in range(myLayout[0]):
        for axsy in range(myLayout[1]):
            myLayoutList.append((axsx,axsy))

    # create subplots
    fig, axs = plt.subplots(myLayout[0],myLayout[1])
    axs = np.reshape(axs,myLayout)

    # adjust layout
    fig.set_size_inches([FIGSIZE*myLayout[1],FIGSIZE*myLayout[0]])
    fig.set_dpi(FIGDPI)
    fig.set_facecolor('black')
    fig.set_tight_layout({'pad': 0})
    fig.subplots_adjust(wspace=0)

    # -----------------------------------------------------------------------------
    # plot each panel

    for p in range(len(CutsRRAS)):

        axsx = myLayoutList[p][0]
        axsy = myLayoutList[p][1]

        # determine dimensions
        if CutsRRAS[p][0] is 'x':
            # x axis of the image should be towards anterior, y axis should be towards superior in RAS image
            dims = (1, 2)
            # determine extent
            extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            cor = np.where(m[dims[0], 0:3])[0]
            axi = np.where(m[dims[1], 0:3])[0]
            #
            if axi < cor:
                axs[axsx,axsy].imshow(normValsRAS[p], cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p] + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)
            else:
                axs[axsx,axsy].imshow(normValsRAS[p].transpose(), cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p].transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)
        elif CutsRRAS[p][0] is 'y':
            #
            dims = (0, 2)
            # determine extent
            extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            sag = np.where(m[dims[0], 0:3])[0]
            axi = np.where(m[dims[1], 0:3])[0]
            #
            if axi < sag:
                axs[axsx,axsy].imshow(normValsRAS[p].transpose(), cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p].transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)
            else:
                axs[axsx,axsy].imshow(normValsRAS[p].transpose(), cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p].transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)
        elif CutsRRAS[p][0] is 'z':
            #
            dims = (0, 1)
            # determine extent
            extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])
            # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
            sag = np.where(m[dims[0], 0:3])[0]
            cor = np.where(m[dims[1], 0:3])[0]
            if axi < sag:
                axs[axsx,axsy].imshow(normValsRAS[p].transpose(), cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p].transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)
            else:
                axs[axsx,axsy].imshow(normValsRAS[p].transpose(), cmap='gray', origin='lower', extent=extent)
                axs[axsx,axsy].imshow(asegValsRAS[p].transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=ALPHA)

        # prepare plot
        if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
            axs[axsx,axsy].invert_xaxis()
        if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
            axs[axsx,axsy].invert_yaxis()

        axs[axsx,axsy].set_axis_off()
        axs[axsx,axsy].set_aspect('equal')

        # now plot
        for i in range(len(lhWhiteLVL[p][1][0])):
            axs[axsx,axsy].plot(
                (lhWhiteLVL[p][0][0][lhWhiteLVL[p][1][0][i][0] - 1][dims[0]], lhWhiteLVL[p][0][0][lhWhiteLVL[p][1][0][i][1] - 1][dims[0]]),
                (lhWhiteLVL[p][0][0][lhWhiteLVL[p][1][0][i][0] - 1][dims[1]], lhWhiteLVL[p][0][0][lhWhiteLVL[p][1][0][i][1] - 1][dims[1]]),
                color='yellow')

        for i in range(len(rhWhiteLVL[p][1][0])):
            axs[axsx,axsy].plot(
                (rhWhiteLVL[p][0][0][rhWhiteLVL[p][1][0][i][0] - 1][dims[0]], rhWhiteLVL[p][0][0][rhWhiteLVL[p][1][0][i][1] - 1][dims[0]]),
                (rhWhiteLVL[p][0][0][rhWhiteLVL[p][1][0][i][0] - 1][dims[1]], rhWhiteLVL[p][0][0][rhWhiteLVL[p][1][0][i][1] - 1][dims[1]]),
                color='yellow')

        for i in range(len(lhPialLVL[p][1][0])):
            axs[axsx,axsy].plot(
                (lhPialLVL[p][0][0][lhPialLVL[p][1][0][i][0] - 1][dims[0]], lhPialLVL[p][0][0][lhPialLVL[p][1][0][i][1] - 1][dims[0]]),
                (lhPialLVL[p][0][0][lhPialLVL[p][1][0][i][0] - 1][dims[1]], lhPialLVL[p][0][0][lhPialLVL[p][1][0][i][1] - 1][dims[1]]),
                color='red')

        for i in range(len(rhPialLVL[p][1][0])):
            axs[axsx,axsy].plot(
                (rhPialLVL[p][0][0][rhPialLVL[p][1][0][i][0] - 1][dims[0]], rhPialLVL[p][0][0][rhPialLVL[p][1][0][i][1] - 1][dims[0]]),
                (rhPialLVL[p][0][0][rhPialLVL[p][1][0][i][0] - 1][dims[1]], rhPialLVL[p][0][0][rhPialLVL[p][1][0][i][1] - 1][dims[1]]),
                color='red')

    # -----------------------------------------------------------------------------
    # output

    if not INTERACTIVE:
        plt.savefig(OUTFILE, facecolor=fig.get_facecolor())
        plt.close(fig)
