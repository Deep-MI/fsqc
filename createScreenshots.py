def createScreenshots(SUBJECT, SUBJECTS_DIR, OUTFILE, INTERACTIVE=True):

    """
    function createScreenshots()
    
    Requires FREESURFER_HOME environment variable 

    """

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

    CutsRRAS = np.array((-10, 10, 0, 0))

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
    # compute levelsets

    lhWhiteLVL1a = levelsetsTria(lhWhite[0], lhWhite[1], lhWhite[0][:, 0, ], CutsRRAS[0])
    lhWhiteLVL1b = levelsetsTria(lhWhite[0], lhWhite[1], lhWhite[0][:, 0, ], CutsRRAS[1])
    lhWhiteLVL2 = levelsetsTria(lhWhite[0], lhWhite[1], lhWhite[0][:, 1, ], CutsRRAS[2])
    lhWhiteLVL3 = levelsetsTria(lhWhite[0], lhWhite[1], lhWhite[0][:, 2, ], CutsRRAS[3])

    rhWhiteLVL1a = levelsetsTria(rhWhite[0], rhWhite[1], rhWhite[0][:, 0, ], CutsRRAS[0])
    rhWhiteLVL1b = levelsetsTria(rhWhite[0], rhWhite[1], rhWhite[0][:, 0, ], CutsRRAS[1])
    rhWhiteLVL2 = levelsetsTria(rhWhite[0], rhWhite[1], rhWhite[0][:, 1, ], CutsRRAS[2])
    rhWhiteLVL3 = levelsetsTria(rhWhite[0], rhWhite[1], rhWhite[0][:, 2, ], CutsRRAS[3])

    lhPialLVL1a = levelsetsTria(lhPial[0], lhPial[1], lhPial[0][:, 0, ], CutsRRAS[0])
    lhPialLVL1b = levelsetsTria(lhPial[0], lhPial[1], lhPial[0][:, 0, ], CutsRRAS[1])
    lhPialLVL2 = levelsetsTria(lhPial[0], lhPial[1], lhPial[0][:, 1, ], CutsRRAS[2])
    lhPialLVL3 = levelsetsTria(lhPial[0], lhPial[1], lhPial[0][:, 2, ], CutsRRAS[3])

    rhPialLVL1a = levelsetsTria(rhPial[0], rhPial[1], rhPial[0][:, 0, ], CutsRRAS[0])
    rhPialLVL1b = levelsetsTria(rhPial[0], rhPial[1], rhPial[0][:, 0, ], CutsRRAS[1])
    rhPialLVL2 = levelsetsTria(rhPial[0], rhPial[1], rhPial[0][:, 1, ], CutsRRAS[2])
    rhPialLVL3 = levelsetsTria(rhPial[0], rhPial[1], rhPial[0][:, 2, ], CutsRRAS[3])

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

    sel = np.array(xyzIdxFlat3[rasIdxFlat3[:, 0] == CutsRRAS[0], :], dtype="int")
    normValsRAS1a = np.squeeze(normVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])
    asegValsRAS1a = np.squeeze(asegVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])

    sel = np.array(xyzIdxFlat3[rasIdxFlat3[:, 0] == CutsRRAS[1], :], dtype="int")
    normValsRAS1b = np.squeeze(normVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])
    asegValsRAS1b = np.squeeze(asegVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])

    sel = np.array(xyzIdxFlat3[rasIdxFlat3[:, 1] == CutsRRAS[2], :], dtype="int")
    normValsRAS2 = np.squeeze(normVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])
    asegValsRAS2 = np.squeeze(asegVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])

    sel = np.array(xyzIdxFlat3[rasIdxFlat3[:, 2] == CutsRRAS[3], :], dtype="int")
    normValsRAS3 = np.squeeze(normVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])
    asegValsRAS3 = np.squeeze(asegVals[np.min(sel[:, 0]):np.max(sel[:, 0]) + 1, np.min(sel[:, 1]):np.max(sel[:, 1]) + 1, np.min(sel[:, 2]):np.max(sel[:, 2]) + 1])

    # -----------------------------------------------------------------------------
    # plotting: create a new figure, plot into it, then close it so it never gets
    # displayed

    # turn interactive plotting off unless interactive
    if not INTERACTIVE:
        plt.ioff()

    # create subplots
    fig, axs = plt.subplots(1, 4)

    # adjust layout
    fig.set_size_inches([32, 8])
    fig.set_dpi(100)
    fig.set_facecolor('black')
    fig.set_tight_layout({'pad': 0})
    fig.subplots_adjust(wspace=0)

    # -----------------------------------------------------------------------------
    # plot dimension 1a:

    # select panel 0
    axsi = 0

    # x axis of the image should be towards anterior, y axis should be towards superior; we choose dims 1 and 2 of the
    # RAS image
    dims = (1, 2)

    # determine extent
    extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])

    # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
    cor = np.where(m[dims[0], 0:3])[0]
    axi = np.where(m[dims[1], 0:3])[0]

    if axi < cor:
        axs[axsi].imshow(normValsRAS1a, cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS1a + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)
    else:
        axs[axsi].imshow(normValsRAS1a.transpose(), cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS1a.transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)

    if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
        axs[axsi].invert_xaxis()
    if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
        axs[axsi].invert_yaxis()

    axs[axsi].set_axis_off()
    axs[axsi].set_aspect('equal')

    for i in range(len(lhWhiteLVL1a[1][0])):
        axs[axsi].plot(
            (lhWhiteLVL1a[0][0][lhWhiteLVL1a[1][0][i][0] - 1][dims[0]], lhWhiteLVL1a[0][0][lhWhiteLVL1a[1][0][i][1] - 1][dims[0]]),
            (lhWhiteLVL1a[0][0][lhWhiteLVL1a[1][0][i][0] - 1][dims[1]], lhWhiteLVL1a[0][0][lhWhiteLVL1a[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(rhWhiteLVL1a[1][0])):
        axs[axsi].plot(
            (rhWhiteLVL1a[0][0][rhWhiteLVL1a[1][0][i][0] - 1][dims[0]], rhWhiteLVL1a[0][0][rhWhiteLVL1a[1][0][i][1] - 1][dims[0]]),
            (rhWhiteLVL1a[0][0][rhWhiteLVL1a[1][0][i][0] - 1][dims[1]], rhWhiteLVL1a[0][0][rhWhiteLVL1a[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(lhPialLVL1a[1][0])):
        axs[axsi].plot(
            (lhPialLVL1a[0][0][lhPialLVL1a[1][0][i][0] - 1][dims[0]], lhPialLVL1a[0][0][lhPialLVL1a[1][0][i][1] - 1][dims[0]]),
            (lhPialLVL1a[0][0][lhPialLVL1a[1][0][i][0] - 1][dims[1]], lhPialLVL1a[0][0][lhPialLVL1a[1][0][i][1] - 1][dims[1]]),
            color='red')

    for i in range(len(rhPialLVL1a[1][0])):
        axs[axsi].plot(
            (rhPialLVL1a[0][0][rhPialLVL1a[1][0][i][0] - 1][dims[0]], rhPialLVL1a[0][0][rhPialLVL1a[1][0][i][1] - 1][dims[0]]),
            (rhPialLVL1a[0][0][rhPialLVL1a[1][0][i][0] - 1][dims[1]], rhPialLVL1a[0][0][rhPialLVL1a[1][0][i][1] - 1][dims[1]]),
            color='red')

    # -----------------------------------------------------------------------------
    # plot dimension 1b:

    # select panel 1
    axsi = 1

    # x axis of the image should be towards anterior, y axis should be towards superior; we choose dims 1 and 2 of the
    # RAS image
    dims = (1, 2)

    # determine extent
    extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])

    # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
    cor = np.where(m[dims[0], 0:3])[0]
    axi = np.where(m[dims[1], 0:3])[0]
    if axi < cor:
        axs[axsi].imshow(normValsRAS1b, cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS1b + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)
    else:
        axs[axsi].imshow(normValsRAS1b.transpose(), cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS1b.transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)

    if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
        axs[axsi].invert_xaxis()
    if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
        axs[axsi].invert_yaxis()

    axs[axsi].set_axis_off()
    axs[axsi].set_aspect('equal')

    for i in range(len(lhWhiteLVL1b[1][0])):
        axs[axsi].plot(
            (lhWhiteLVL1b[0][0][lhWhiteLVL1b[1][0][i][0] - 1][dims[0]], lhWhiteLVL1b[0][0][lhWhiteLVL1b[1][0][i][1] - 1][dims[0]]),
            (lhWhiteLVL1b[0][0][lhWhiteLVL1b[1][0][i][0] - 1][dims[1]], lhWhiteLVL1b[0][0][lhWhiteLVL1b[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(rhWhiteLVL1b[1][0])):
        axs[axsi].plot(
            (rhWhiteLVL1b[0][0][rhWhiteLVL1b[1][0][i][0] - 1][dims[0]], rhWhiteLVL1b[0][0][rhWhiteLVL1b[1][0][i][1] - 1][dims[0]]),
            (rhWhiteLVL1b[0][0][rhWhiteLVL1b[1][0][i][0] - 1][dims[1]], rhWhiteLVL1b[0][0][rhWhiteLVL1b[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(lhPialLVL1b[1][0])):
        axs[axsi].plot(
            (lhPialLVL1b[0][0][lhPialLVL1b[1][0][i][0] - 1][dims[0]], lhPialLVL1b[0][0][lhPialLVL1b[1][0][i][1] - 1][dims[0]]),
            (lhPialLVL1b[0][0][lhPialLVL1b[1][0][i][0] - 1][dims[1]], lhPialLVL1b[0][0][lhPialLVL1b[1][0][i][1] - 1][dims[1]]),
            color='red')

    for i in range(len(rhPialLVL1b[1][0])):
        axs[axsi].plot(
            (rhPialLVL1b[0][0][rhPialLVL1b[1][0][i][0] - 1][dims[0]], rhPialLVL1b[0][0][rhPialLVL1b[1][0][i][1] - 1][dims[0]]),
            (rhPialLVL1b[0][0][rhPialLVL1b[1][0][i][0] - 1][dims[1]], rhPialLVL1b[0][0][rhPialLVL1b[1][0][i][1] - 1][dims[1]]),
            color='red')

    # -----------------------------------------------------------------------------
    # plot dimension 2:

    # select panel 2
    axsi = 2

    #  x axis of the image should be towards right, y axis should be towards superior; we choose dims 0 and 2 of the
    #  RAS image
    dims = (0, 2)

    # determine extent
    extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])

    # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
    sag = np.where(m[dims[0], 0:3])[0]
    axi = np.where(m[dims[1], 0:3])[0]

    if axi < sag:
        axs[axsi].imshow(normValsRAS2.transpose(), cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS2.transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)
    else:
        axs[axsi].imshow(normValsRAS2.transpose(), cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS2.transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)

    if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
        axs[axsi].invert_xaxis()
    if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
        axs[axsi].invert_yaxis()

    axs[axsi].set_axis_off()
    axs[axsi].set_aspect('equal')

    for i in range(len(lhWhiteLVL2[1][0])):
        axs[axsi].plot(
            (lhWhiteLVL2[0][0][lhWhiteLVL2[1][0][i][0] - 1][dims[0]], lhWhiteLVL2[0][0][lhWhiteLVL2[1][0][i][1] - 1][dims[0]]),
            (lhWhiteLVL2[0][0][lhWhiteLVL2[1][0][i][0] - 1][dims[1]], lhWhiteLVL2[0][0][lhWhiteLVL2[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(rhWhiteLVL2[1][0])):
        axs[axsi].plot(
            (rhWhiteLVL2[0][0][rhWhiteLVL2[1][0][i][0] - 1][dims[0]], rhWhiteLVL2[0][0][rhWhiteLVL2[1][0][i][1] - 1][dims[0]]),
            (rhWhiteLVL2[0][0][rhWhiteLVL2[1][0][i][0] - 1][dims[1]], rhWhiteLVL2[0][0][rhWhiteLVL2[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(lhPialLVL2[1][0])):
        axs[axsi].plot(
            (lhPialLVL2[0][0][lhPialLVL2[1][0][i][0] - 1][dims[0]], lhPialLVL2[0][0][lhPialLVL2[1][0][i][1] - 1][dims[0]]),
            (lhPialLVL2[0][0][lhPialLVL2[1][0][i][0] - 1][dims[1]], lhPialLVL2[0][0][lhPialLVL2[1][0][i][1] - 1][dims[1]]),
            color='red')

    for i in range(len(rhPialLVL2[1][0])):
        axs[axsi].plot(
            (rhPialLVL2[0][0][rhPialLVL2[1][0][i][0] - 1][dims[0]], rhPialLVL2[0][0][rhPialLVL2[1][0][i][1] - 1][dims[0]]),
            (rhPialLVL2[0][0][rhPialLVL2[1][0][i][0] - 1][dims[1]], rhPialLVL2[0][0][rhPialLVL2[1][0][i][1] - 1][dims[1]]),
            color='red')

    # -----------------------------------------------------------------------------
    # plot dimension 3:

    # select panel 3
    axsi = 3

    # x axis of the image should be towards right, y axis should be towards anterior; we choose dims 0 and 1 of the
    # RAS image
    dims = (0, 1)

    # determine extent
    extent = (rasIdxFlat3[0, dims[0]], rasIdxFlat3[-1, dims[0]], rasIdxFlat3[0, dims[1]], rasIdxFlat3[-1, dims[1]])

    # imshow puts the first dimension (rows) of the data on the y axis, and the second (columns) on the x axis
    sag = np.where(m[dims[0], 0:3])[0]
    cor = np.where(m[dims[1], 0:3])[0]

    if cor < sag:
        axs[axsi].imshow(normValsRAS3, cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS3 + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)
    else:
        axs[axsi].imshow(normValsRAS3.transpose(), cmap='gray', origin='lower', extent=extent)
        axs[axsi].imshow(asegValsRAS3.transpose() + 0.5, cmap=lutMap, origin='lower', extent=extent, vmin=0, vmax=len(lutTab), alpha=0.5)

    if rasIdxFlat3[0, dims[0]] > rasIdxFlat3[-1, dims[0]]:
        axs[axsi].invert_xaxis()
    if rasIdxFlat3[0, dims[1]] > rasIdxFlat3[-1, dims[1]]:
        axs[axsi].invert_yaxis()

    axs[axsi].set_axis_off()
    axs[axsi].set_aspect('equal')

    for i in range(len(lhWhiteLVL3[1][0])):
        axs[axsi].plot(
            (lhWhiteLVL3[0][0][lhWhiteLVL3[1][0][i][0] - 1][dims[0]], lhWhiteLVL3[0][0][lhWhiteLVL3[1][0][i][1] - 1][dims[0]]),
            (lhWhiteLVL3[0][0][lhWhiteLVL3[1][0][i][0] - 1][dims[1]], lhWhiteLVL3[0][0][lhWhiteLVL3[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(rhWhiteLVL3[1][0])):
        axs[axsi].plot(
            (rhWhiteLVL3[0][0][rhWhiteLVL3[1][0][i][0] - 1][dims[0]], rhWhiteLVL3[0][0][rhWhiteLVL3[1][0][i][1] - 1][dims[0]]),
            (rhWhiteLVL3[0][0][rhWhiteLVL3[1][0][i][0] - 1][dims[1]], rhWhiteLVL3[0][0][rhWhiteLVL3[1][0][i][1] - 1][dims[1]]),
            color='yellow')

    for i in range(len(lhPialLVL3[1][0])):
        axs[axsi].plot(
            (lhPialLVL3[0][0][lhPialLVL3[1][0][i][0] - 1][dims[0]], lhPialLVL3[0][0][lhPialLVL3[1][0][i][1] - 1][dims[0]]),
            (lhPialLVL3[0][0][lhPialLVL3[1][0][i][0] - 1][dims[1]], lhPialLVL3[0][0][lhPialLVL3[1][0][i][1] - 1][dims[1]]),
            color='red')

    for i in range(len(rhPialLVL3[1][0])):
        axs[axsi].plot(
            (rhPialLVL3[0][0][rhPialLVL3[1][0][i][0] - 1][dims[0]], rhPialLVL3[0][0][rhPialLVL3[1][0][i][1] - 1][dims[0]]),
            (rhPialLVL3[0][0][rhPialLVL3[1][0][i][0] - 1][dims[1]], rhPialLVL3[0][0][rhPialLVL3[1][0][i][1] - 1][dims[1]]),
            color='red')

    # -----------------------------------------------------------------------------
    # output

    if not INTERACTIVE:
        plt.savefig(OUTFILE, facecolor=fig.get_facecolor())
        plt.close(fig)
