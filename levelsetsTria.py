def levelsetsTria(v, t, p, levelsets):

    import numpy as np
    from scipy.sparse import csr_matrix, lil_matrix

    vLVL = list()
    lLVL = list()
    iLVL = list()

    A = lil_matrix((np.shape(v)[0],np.shape(v)[0]))

    levelsets = (np.array(levelsets, ndmin=2))

    for l in range(len(levelsets)):

        lvl = levelsets[l]

        nlvl = p[t] > lvl

        n = np.where(np.logical_or(np.sum(nlvl, axis=1) == 1 , np.sum(nlvl, axis=1) == 2))[0]

        # interpolate points

        ti = list()
        vi = list()

        for i in range(len(n)):

            # which are the outlying points in the current tria?
            oi = np.where(nlvl[n[i],:])[0]

            #  convert 2 --> 1
            if len(oi) == 2:
                oi = np.setdiff1d((0,1,2), oi)

            # find the two non - outyling points
            oix = np.setdiff1d((0, 1, 2), oi)

            # check if we have interpolated for one or both of these points before

            if np.count_nonzero(A[t[n[i], oi], t[n[i], oix[0]]]) ==0 :

                # compute difference vectors between outlying point and other points

                d10 = v[ t[n[i], oix[0]], :] - v[ t[n[i], oi], :]

                # compute differences of all points to lvl to get interpolation factors

                s10 = (lvl - p[t[n[i], oi]]) / (p[t[n[i], oix[0]]] - p[t[n[i], oi]])

                # compute new points

                v10 = s10 * d10 + v[ t[n[i], oi], :]

                # update vi and index(order matters)

                vi.append(v10.tolist()[0])

                ti10 = len(vi)

                # store between which two points we are interpolating (to avoid having duplicate points)

                A[ t[n[i], oi], t[n[i], oix[0]] ] = ti10
                A[ t[n[i], oix[0]], t[n[i], oi] ] = ti10

            else:

                ti10 = int(A[ t[n[i], oi], t[n[i], oix[0]] ].toarray().item())

            # essentially the same as above, just for oix[1]

            if np.count_nonzero(A[t[n[i], oi], t[n[i], oix[1]]]) == 0:

                d20 = v[ t[n[i], oix[1]], :] - v[ t[n[i], oi], :]

                s20 = (lvl - p[t[n[i], oi]]) / (p[t[n[i], oix[1]]] - p[t[n[i], oi]])

                v20 = s20 * d20 + v[ t[n[i], oi], :]

                # update vi and index(order matters)

                vi.append(v20.tolist()[0])

                ti20 = len(vi)

                A[ t[n[i], oi], t[n[i], oix[1]] ] = ti20
                A[ t[n[i], oix[1]], t[n[i], oi] ] = ti20

            else:

                ti20 = int(A[ t[n[i], oi], t[n[i], oix[1]] ].toarray().item())

            # store new indices

            ti.append((ti10,ti20))

            # clean up

            # clear oi oix d10 d20 s10 s20 v10 v20 t10 t20

        # store

        vLVL.append(vi)
        lLVL.append(ti)
        iLVL.append(n)

    return vLVL[0], lLVL[0], iLVL