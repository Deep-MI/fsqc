"""
This module provides various import/export functions as well as the
'levelsetsTria' function

"""

# ------------------------------------------------------------------------------


def importMGH(filename):
    """
    A function to read Freesurfer MGH files.

    Required arguments:
        - filename

    Returns:
        - vol

    Requires valid mgh file. If not found, NaNs will be returned.

    """

    import os
    import struct

    import numpy

    if not os.path.exists(filename):
        print("WARNING: could not find " + filename + ", returning NaNs")
        return numpy.nan

    fp = open(filename, "rb")
    intsize = struct.calcsize(">i")
    shortsize = struct.calcsize(">h")
    floatsize = struct.calcsize(">f")
    charsize = struct.calcsize(">b")

    v = struct.unpack(">i", fp.read(intsize))[0]
    ndim1 = struct.unpack(">i", fp.read(intsize))[0]
    ndim2 = struct.unpack(">i", fp.read(intsize))[0]
    ndim3 = struct.unpack(">i", fp.read(intsize))[0]
    nframes = struct.unpack(">i", fp.read(intsize))[0]
    vtype = struct.unpack(">i", fp.read(intsize))[0]
    dof = struct.unpack(">i", fp.read(intsize))[0]

    UNUSED_SPACE_SIZE = 256
    USED_SPACE_SIZE = (3 * 4) + (4 * 3 * 4)  # space for ras transform
    unused_space_size = UNUSED_SPACE_SIZE - 2

    ras_good_flag = struct.unpack(">h", fp.read(shortsize))[0]
    if ras_good_flag:
        # We read these in but don't process them
        # as we just want to move to the volume data
        delta = struct.unpack(">fff", fp.read(floatsize * 3))
        Mdc = struct.unpack(">fffffffff", fp.read(floatsize * 9))
        Pxyz_c = struct.unpack(">fff", fp.read(floatsize * 3))

    unused_space_size = unused_space_size - USED_SPACE_SIZE

    for i in range(unused_space_size):
        struct.unpack(">b", fp.read(charsize))[0]

    nv = ndim1 * ndim2 * ndim3 * nframes
    vol = numpy.fromstring(fp.read(floatsize * nv), dtype=numpy.float32).byteswap()

    nvert = max([ndim1, ndim2, ndim3])
    vol = numpy.reshape(vol, (ndim1, ndim2, ndim3, nframes), order="F")
    vol = numpy.squeeze(vol)
    fp.close()

    return vol


# ------------------------------------------------------------------------------


def binarizeImage(img_file, out_file, match=None):
    import nibabel as nb
    import numpy as np

    # get image
    img = nb.load(img_file)
    img_data = img.get_fdata()

    # binarize
    if match is None:
        img_data_bin = img_data != 0.0
    else:
        img_data_bin = np.isin(img_data, match)

    # write output
    img_bin = nb.nifti1.Nifti1Image(img_data_bin.astype(int), img.affine, dtype="uint8")
    nb.save(img_bin, out_file)


# ------------------------------------------------------------------------------


def applyTransform(img_file, out_file, mat_file, interp):
    import os
    import sys

    import nibabel as nb
    import numpy as np
    from scipy import ndimage

    # get image
    img = nb.load(img_file)
    img_data = img.get_fdata()

    #
    _, mat_file_ext = os.path.splitext(mat_file)

    # get matrix
    if mat_file_ext == ".xfm":
        print("ERROR: xfm matrices not (yet) supported. Please convert to lta format")
        sys.exit(1)
    elif mat_file_ext == ".lta":
        # get lta matrix
        lta = readLTA(mat_file)
        # get vox2vox transform
        if lta["type"] == 1:
            # compute vox2vox from ras2ras as vox2ras2ras2vox transform:
            # vox2ras from input image (source)
            # ras2ras from make_upright.lta
            # ras2vox from upright image (target)
            # m = np.matmul(np.linalg.inv(upr.affine), np.matmul(lta['lta'], img.affine))
            print("ERROR: lta type 1 (ras2ras) not supported yet")
            sys.exit(1)
        elif lta["type"] == 0:
            # vox2vox transform
            m = lta["lta"]
    else:
        print("ERROR: matrices must be either xfm or lta format")
        sys.exit(1)

    # apply transform
    if interp == "nearest":
        img_data_interp = ndimage.affine_transform(img_data, np.linalg.inv(m), order=0)
    elif interp == "cubic":
        img_data_interp = ndimage.affine_transform(img_data, np.linalg.inv(m), order=3)
    else:
        print("ERROR: interpolation must be either nearest or cubic")
        sys.exit(1)

    # write image
    img_interp = nb.nifti1.Nifti1Image(img_data_interp, img.affine)
    nb.save(img_interp, out_file)


# ------------------------------------------------------------------------------


def readLTA(file):
    import re

    import numpy as np

    with open(file, "r") as f:
        lta = f.readlines()
    d = dict()
    i = 0
    while i < len(lta):
        if re.match("type", lta[i]) is not None:
            d["type"] = int(re.sub("=", "", re.sub("[a-z]+", "", re.sub("#.*", "", lta[i]))).strip())
            i += 1
        elif re.match("nxforms", lta[i]) is not None:
            d["nxforms"] = int(re.sub("=", "", re.sub("[a-z]+", "", re.sub("#.*", "", lta[i]))).strip())
            i += 1
        elif re.match("mean", lta[i]) is not None:
            d["mean"] = [
                float(x)
                for x in re.split(" +", re.sub("=", "", re.sub("[a-z]+", "", re.sub("#.*", "", lta[i]))).strip())
            ]
            i += 1
        elif re.match("sigma", lta[i]) is not None:
            d["sigma"] = float(re.sub("=", "", re.sub("[a-z]+", "", re.sub("#.*", "", lta[i]))).strip())
            i += 1
        elif re.match("-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+", lta[i]) is not None:
            d["lta"] = np.array(
                [
                    [
                        float(x)
                        for x in re.split(
                            " +",
                            re.match(
                                "-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+", lta[i]
                            ).string.strip(),
                        )
                    ],
                    [
                        float(x)
                        for x in re.split(
                            " +",
                            re.match(
                                "-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+", lta[i + 1]
                            ).string.strip(),
                        )
                    ],
                    [
                        float(x)
                        for x in re.split(
                            " +",
                            re.match(
                                "-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+", lta[i + 2]
                            ).string.strip(),
                        )
                    ],
                    [
                        float(x)
                        for x in re.split(
                            " +",
                            re.match(
                                "-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+-*[0-9]\.\S+\W+", lta[i + 3]
                            ).string.strip(),
                        )
                    ],
                ]
            )
            i += 4
        elif re.match("src volume info", lta[i]) is not None:
            while i < len(lta) and re.match("dst volume info", lta[i]) is None:
                if re.match("valid", lta[i]) is not None:
                    d["src_valid"] = int(re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                elif re.match("filename", lta[i]) is not None:
                    d["src_filename"] = re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                elif re.match("volume", lta[i]) is not None:
                    d["src_volume"] = [
                        int(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("voxelsize", lta[i]) is not None:
                    d["src_voxelsize"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("xras", lta[i]) is not None:
                    d["src_xras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("yras", lta[i]) is not None:
                    d["src_yras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("zras", lta[i]) is not None:
                    d["src_zras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("cras", lta[i]) is not None:
                    d["src_cras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                i += 1
        elif re.match("dst volume info", lta[i]) is not None:
            while i < len(lta) and re.match("src volume info", lta[i]) is None:
                if re.match("valid", lta[i]) is not None:
                    d["dst_valid"] = int(re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                elif re.match("filename", lta[i]) is not None:
                    d["dst_filename"] = re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                elif re.match("volume", lta[i]) is not None:
                    d["dst_volume"] = [
                        int(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("voxelsize", lta[i]) is not None:
                    d["dst_voxelsize"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("xras", lta[i]) is not None:
                    d["dst_xras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("yras", lta[i]) is not None:
                    d["dst_yras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("zras", lta[i]) is not None:
                    d["dst_zras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                elif re.match("cras", lta[i]) is not None:
                    d["dst_cras"] = [
                        float(x) for x in re.split(" +", re.sub(".*=", "", re.sub("#.*", "", lta[i])).strip())
                    ]
                i += 1
        else:
            i += 1
    # create full transformation matrices
    d["src"] = np.concatenate(
        (
            np.concatenate(
                (np.c_[d["src_xras"]], np.c_[d["src_yras"]], np.c_[d["src_zras"]], np.c_[d["src_cras"]]), axis=1
            ),
            np.array([0.0, 0.0, 0.0, 1.0], ndmin=2),
        ),
        axis=0,
    )
    d["dst"] = np.concatenate(
        (
            np.concatenate(
                (np.c_[d["dst_xras"]], np.c_[d["dst_yras"]], np.c_[d["dst_zras"]], np.c_[d["dst_cras"]]), axis=1
            ),
            np.array([0.0, 0.0, 0.0, 1.0], ndmin=2),
        ),
        axis=0,
    )
    # return
    return d


# ------------------------------------------------------------------------------


def levelsetsTria(v, t, p, levelsets):
    """
    This is the levelsetsTria function

    """

    import numpy as np
    from scipy.sparse import lil_matrix

    vLVL = list()
    lLVL = list()
    iLVL = list()

    levelsets = np.array(levelsets, ndmin=2)

    for lidx in range(len(levelsets)):
        A = lil_matrix((np.shape(v)[0], np.shape(v)[0]))

        lvl = levelsets[lidx]

        nlvl = p[t] > lvl

        n = np.where(np.logical_or(np.sum(nlvl, axis=1) == 1, np.sum(nlvl, axis=1) == 2))[0]

        # interpolate points

        ti = list()
        vi = list()

        for i in range(len(n)):
            # which are the outlying points in the current tria?
            oi = np.where(nlvl[n[i], :])[0]

            #  convert 2 --> 1
            if len(oi) == 2:
                oi = np.setdiff1d((0, 1, 2), oi)

            # find the two non - outyling points
            oix = np.setdiff1d((0, 1, 2), oi)

            # check if we have interpolated for one or both of these points before
            if np.count_nonzero(A[t[n[i], oi.item()], t[n[i], oix[0]]]) == 0:
                # compute difference vectors between outlying point and other points

                d10 = v[t[n[i], oix[0]], :] - v[t[n[i], oi], :]

                # compute differences of all points to lvl to get interpolation factors

                s10 = (lvl - p[t[n[i], oi]]) / (p[t[n[i], oix[0]]] - p[t[n[i], oi]])

                # compute new points

                v10 = s10 * d10 + v[t[n[i], oi], :]

                # update vi and index(order matters)

                vi.append(v10.tolist()[0])

                ti10 = len(vi)

                # store between which two points we are interpolating (to avoid having duplicate points)

                A[t[n[i], oi.item()], t[n[i], oix[0]]] = ti10
                A[t[n[i], oix[0]], t[n[i], oi.item()]] = ti10

            else:
                ti10 = int(A[t[n[i], oi.item()], t[n[i], oix[0]]])

            # essentially the same as above, just for oix[1]

            if np.count_nonzero(A[t[n[i], oi.item()], t[n[i], oix[1]]]) == 0:
                d20 = v[t[n[i], oix[1]], :] - v[t[n[i], oi], :]

                s20 = (lvl - p[t[n[i], oi]]) / (p[t[n[i], oix[1]]] - p[t[n[i], oi]])

                v20 = s20 * d20 + v[t[n[i], oi], :]

                # update vi and index(order matters)

                vi.append(v20.tolist()[0])

                ti20 = len(vi)

                A[t[n[i], oi.item()], t[n[i], oix[1]]] = ti20
                A[t[n[i], oix[1]], t[n[i], oi.item()]] = ti20

            else:
                ti20 = int(A[t[n[i], oi.item()], t[n[i], oix[1]]])

            # store new indices

            ti.append((ti10, ti20))

            # clean up

            # clear oi oix d10 d20 s10 s20 v10 v20 t10 t20

        # store

        vLVL.append(vi)
        lLVL.append(ti)
        iLVL.append(n)

    return vLVL, lLVL, iLVL
