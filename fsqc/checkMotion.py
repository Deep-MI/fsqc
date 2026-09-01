# STATEMENT OF CHANGES: This file is derived from sources licensed under the
# Apache-2.0 terms, and this file has been changed.
# The original file this work derives from is found at:
# https://github.com/nipreps/mriqc/blob/master/mriqc/qc/anatomical.py
#
# ORIGINAL WORK'S ATTRIBUTION NOTICE:
#
#     Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
This module provides MRIQC-style image quality metrics related to motion/noise.

Metrics (EFC, FBER, SNR, background summary stats) are computed via
``mriqc.qc.anatomical``, on a single unified image grid shared with the
subject's FreeSurfer/FastSurfer ``aseg``/``aparc`` segmentation. Two
reference volumes are used, mirroring mriqc's own ``in_ras``/``in_noinu``
split:

- the merely-conformed ``ref_image`` (``orig.mgz`` by default) feeds QI2 and
  the rotation mask
- the bias-field-corrected ``nu_image`` (``nu.mgz`` by default;
  ``orig_nu.mgz`` for FastSurfer output) feeds the internally computed head
  mask and is harmonized (rescaled so the white-matter mask's median
  intensity is 1000, mirroring mriqc's own ``Harmonize`` step) before
  EFC/FBER/SNR/background stats are computed from it

QI2 is computed by a local, pure-computation port of mriqc's ``art_qi2`` 
(see :func:`_computeQi2`), to avoid its unconditional SVG report output.

Unlike mriqc, which bias-corrects via its own two-pass ANTs
``N4BiasFieldCorrection`` (SynthStrip-mask-guided, after percentile
intensity clipping) before harmonizing, this module reuses whichever bias
correction FreeSurfer/FastSurfer already applied to produce ``nu_image`` --
a different algorithm/parameterization than mriqc's own, so absolute values
computed here won't numerically match mriqc's, even though the same
two-image-role split and harmonization target are reproduced.

Implemented measures:

- EFC              : Entropy Focus Criterion
- QI2              : Mortamet's quality index 2
- FBER             : Foreground-Background Energy Ratio
- SNR_HEAD         : Signal-to-Noise Ratio over the head mask (externally
                      supplied, or computed internally via Otsu
                      thresholding of the bias-corrected reference image,
                      reinforced by the aparc+aseg segmentation)
- SNR_TISSUE_*     : Signal-to-Noise Ratio in the GM/WM/CSF tissue masks
                      derived from a FreeSurfer/FastSurfer segmentation
                      (``_gm``, ``_wm``, ``_csf``), and their mean
                      (``_total``); GM includes subcortical structures, not
                      just cortex, and WM includes (uneroded) cerebellar
                      white matter alongside the eroded cerebral component
- BG               : Background summary statistics
"""

import os

# -----------------------------------------------------------------------------
# private helper functions and variables
# -----------------------------------------------------------------------------

# FreeSurferColorLUT label IDs used to build tissue masks for SNR estimation
# and harmonization. Unlike fsqc.checkSNR.checkSNR, GM here also includes
# subcortical structures (FreeSurfer's own aseg.stats "SubCortGrayVol" set),
# and WM's cerebellar component is split out into its own (unedoded)
# constant -- see _WM_LABELS_CEREBELLUM below.

# Left/Right-Cerebral-White-Matter, corpus callosum (CC_*), WM-hypointensities;
# eroded by nb_erode_wm.
_WM_LABELS = [2, 41, 251, 252, 253, 254, 255, 77, 78, 79]

# Left/Right-Cerebellum-White-Matter; kept unedoded (never eroded), since it's
# too thin to survive nb_erode_wm -- see checkSNR.py's own docstring for the
# same reasoning applied to (unedoded) GM.
_WM_LABELS_CEREBELLUM = [7, 46]

# Cortex plus FreeSurfer's standard subcortical gray-matter structures
# (matching aseg.stats' "SubCortGrayVol"); never eroded (nb_erode=0), for the
# same thin-structure reason as _WM_LABELS_CEREBELLUM.
_GM_LABELS = [
    3, 42,    # Left/Right-Cerebral-Cortex
    10, 49,   # Left/Right-Thalamus
    11, 50,   # Left/Right-Caudate
    12, 51,   # Left/Right-Putamen
    13, 52,   # Left/Right-Pallidum
    17, 53,   # Left/Right-Hippocampus
    18, 54,   # Left/Right-Amygdala
    26, 58,   # Left/Right-Accumbens-area
    28, 60,   # Left/Right-VentralDC
]

_CSF_LABELS = [24, 4, 43, 5, 44, 14, 15]


def _tissue_mask_from_labels(seg_data, labels, nb_erode=0):
    """Build a binary mask for the given segmentation label IDs, optionally eroded."""
    import numpy as np
    from skimage.morphology import binary_erosion

    mask = np.isin(seg_data, labels).astype(np.uint8)
    if nb_erode > 0:
        mask = binary_erosion(mask, np.ones((nb_erode, nb_erode, nb_erode))).astype(np.uint8)

    return mask


def _save_nii(img, affine, out_path, dtype="uint8"):
    """Save an array as a NIfTI (.nii/.nii.gz) image, cast to ``dtype``."""
    import nibabel as nib

    nib.save(nib.nifti1.Nifti1Image(img.astype(dtype), affine), out_path)


def _load_external_mask(mask_file, mask_label, ref_img_shape, binarize=True, conform=False):
    """
    Load and validate an externally supplied volume against ``ref_img_shape``.

    Returns the loaded array (binarized, unless ``binarize=False``) on
    success. Raises ``FileNotFoundError`` or ``ValueError`` on failure
    (missing file, load error, shape mismatch); the caller is expected to
    warn and fail closed (return NaNs) on exception, since an explicitly
    supplied mask/segmentation should never be silently ignored.

    If ``conform=True``, the volume is passed through
    :func:`_conformImageToRAS` (squeeze + RAS reorientation, no
    interpolation) before use -- for volumes such as FreeSurfer/FastSurfer's
    ``aseg``/``aparc`` segmentations, which live in the same native
    (unconformed) grid as the pre-conform reference image and would
    otherwise be spatially misaligned with it once it's RAS-conformed,
    despite matching shapes (both are 256^3 cubes). Externally supplied
    masks (rotmask/headmask/airmask) are documented as already being in the
    conformed grid, so they use ``conform=False``.
    """
    import nibabel as nib

    if not os.path.exists(mask_file):
        raise FileNotFoundError("could not find external " + mask_label + " " + mask_file)
    mask_img = nib.load(mask_file)
    if conform:
        mask_img = _conformImageToRAS(mask_img)
    candidate = mask_img.get_fdata()
    if candidate.shape[:3] != ref_img_shape:
        raise ValueError(
            "external " + mask_label + " " + mask_file + " has shape "
            + str(candidate.shape[:3]) + ", expected " + str(ref_img_shape)
        )
    return (candidate > 0).astype("uint8") if binarize else candidate


def _conformImageToRAS(in_img):
    """
    Conform an anatomical image the way mriqc's anatomical workflow does.

    Mirrors mriqc's ``mriqc.interfaces.common.ConformImage`` as it is
    actually invoked in mriqc's anatomical workflow
    (``ConformImage(check_dtype=False)``): squeeze a redundant 4th
    dimension, then reorient to RAS canonical orientation
    (``nib.as_closest_canonical``). No dtype casting and no resampling to a
    fixed voxel size/shape is performed (unlike FreeSurfer's own
    ``mri_convert --conform``).

    Parameters
    ----------
    in_img : nibabel.spatialimages.SpatialImage or str or os.PathLike
        Input image, or a path to load one from.

    Returns
    -------
    nibabel.spatialimages.SpatialImage
        Conformed (squeezed + RAS-reoriented) image.
    """
    import nibabel as nib

    if isinstance(in_img, (str, os.PathLike)):
        in_img = nib.load(in_img)

    return nib.as_closest_canonical(nib.squeeze_image(in_img))



def _harmonizeImage(img, wm_mask):
    """
    Rescale ``img`` so that its median intensity within ``wm_mask`` is 1000.

    Mirrors mriqc's ``mriqc.interfaces.anatomical.Harmonize._run_interface``
    (not importable as a plain function -- only available as a nipype
    Interface). ``wm_mask`` is expected to already be eroded (fsqc reuses
    the same eroded white-matter mask built for tissue-based SNR, rather
    than eroding a second time as mriqc's ``Harmonize`` does internally).

    Parameters
    ----------
    img : numpy.ndarray
        3D image array (typically the conformed reference image).
    wm_mask : numpy.ndarray
        Binary white-matter mask, same shape as ``img``.

    Returns
    -------
    numpy.ndarray or None
        The rescaled image, or ``None`` if ``wm_mask`` is empty or its
        median intensity is non-positive/non-finite (harmonization not
        possible).
    """
    import numpy as np

    if not np.any(wm_mask):
        return None

    wm_median = float(np.median(img[wm_mask > 0]))
    if not np.isfinite(wm_median) or wm_median <= 0:
        return None

    return img * (1000.0 / wm_median)


def _computeRotmaskMortamet(img, min_size=500):
    """
    Compute a rotation-artifact mask using the method of [Mortamet2009]_.

    Ported from mriqc's ``mriqc.interfaces.anatomical.RotationMask`` (not
    importable as a plain function -- only available as a nipype
    Interface). Flags hard-zero (``<= 0``) voxels left by an obliquely
    prescribed acquisition being reconstructed into a rectangular voxel grid
    (not resampling padding from a conform step). Thin/noisy zero specks are
    removed via binary opening, then only the largest couple of connected
    components (the real cut-corner region(s), which merge with the padded
    border) are kept; the whole mask is discarded if it is too small to be a
    genuine artifact.

    Parameters
    ----------
    img : numpy.ndarray
        3D image array.
    min_size : int, optional
        Minimum number of voxels for the detected mask to be kept; smaller
        masks are treated as noise and zeroed out (default: 500, matching
        mriqc's hardcoded threshold).

    Returns
    -------
    numpy.ndarray
        Binary rotation mask (uint8, 1 = detected hard-zero artifact region).
    """
    import numpy as np
    from scipy import ndimage as ndimg

    mask = img <= 0

    # Pad one voxel so real cut-corner regions (which touch the volume
    # border) merge into a single component with the padding, separating
    # them from small interior zero specks during the labeling step below.
    mask = np.pad(mask, pad_width=(1,), mode="constant", constant_values=1)

    struct = ndimg.generate_binary_structure(3, 2)
    mask = ndimg.binary_opening(mask, structure=struct).astype(np.uint8)

    label_im, nb_labels = ndimg.label(mask)
    if nb_labels > 2:
        sizes = ndimg.sum(mask, label_im, list(range(nb_labels + 1)))
        ordered = sorted(zip(sizes, list(range(nb_labels + 1)), strict=True), reverse=True)
        for _, label in ordered[2:]:
            mask[label_im == label] = 0

    mask = mask[1:-1, 1:-1, 1:-1]

    if mask.sum() < min_size:
        mask = np.zeros_like(mask, dtype=np.uint8)

    return mask.astype(np.uint8)


def _computeHeadmaskOtsu(img, seg_data, rotmask=None, nb_dilate=10):
    """
    Compute a head mask via Otsu thresholding, reinforced by segmentation.

    An Otsu threshold (``skimage.filters.threshold_otsu``) is estimated
    from the finite, positive-intensity voxels of ``img`` (excluding
    hard-zero/negative conform padding, which would otherwise inject a
    spike at 0 and skew the bimodal histogram split); voxels above it are
    flagged as head. This alone can miss dim tissue near the boundary, so
    the result is unioned with ``seg_data > 0`` -- any voxel already
    assigned a FreeSurfer/FastSurfer segmentation label is unambiguously
    part of the head, regardless of intensity. The combined mask can
    optionally be dilated (see ``nb_dilate``) to close small gaps/
    protrusions along the boundary; binary hole-filling
    (``scipy.ndimage.binary_fill_holes``) then seals interior gaps (e.g.
    ventricles/CSF, or other dark-but-inside-the-head voxels) -- holes can
    be quite large, but are expected to already be fully enclosed by
    mask==1 voxels once the segmentation union (and optional dilation) is
    applied.

    Parameters
    ----------
    img : numpy.ndarray
        3D image array (typically the conformed reference image).
    seg_data : numpy.ndarray
        3D FreeSurfer/FastSurfer segmentation array (e.g. ``aparc+aseg``),
        same shape as ``img``; any nonzero label is treated as head tissue.
    rotmask : numpy.ndarray or None, optional
        Optional rotation-artifact mask, same shape as ``img``; non-zero
        voxels are excluded from the head mask, since they are artifacts
        rather than genuine head tissue.
    nb_dilate : int or None, optional
        Structuring-element size (in voxels) for an optional binary
        dilation applied to the Otsu/segmentation mask, after the union
        but before hole-filling. ``0`` or ``None`` disables dilation
        (default: ``10``).

    Returns
    -------
    numpy.ndarray
        Binary head mask (uint8, 1 = head).
    """
    import numpy as np
    from scipy import ndimage as ndimg
    from skimage.filters import threshold_otsu
    from skimage.morphology import binary_dilation

    finite_positive = img[np.isfinite(img) & (img > 0)]
    threshold = threshold_otsu(finite_positive) if finite_positive.size else 0

    headmask = (img > threshold) | (seg_data > 0)

    if nb_dilate:
        headmask = binary_dilation(headmask, np.ones((nb_dilate, nb_dilate, nb_dilate)))

    headmask = ndimg.binary_fill_holes(headmask).astype(np.uint8)

    if rotmask is not None:
        headmask[rotmask > 0] = 0

    return headmask


def _computeAirmask(headmask, rotmask=None):
    """
    Compute an air/background mask as the complement of ``headmask``.

    Currently a simple inversion, kept as its own function (rather than
    inlining ``headmask == 0`` at the call site) so a more elaborate
    computation can be substituted later without changing
    :func:`checkMotion`'s control flow.

    Parameters
    ----------
    headmask : numpy.ndarray
        Binary head mask, e.g. as returned by :func:`_computeHeadmaskOtsu`.
    rotmask : numpy.ndarray or None, optional
        Optional rotation-artifact mask, same shape as ``headmask``;
        non-zero voxels are excluded from the air mask, since they are
        artifacts rather than genuine background.

    Returns
    -------
    numpy.ndarray
        Binary air mask (uint8, 1 = background/air).
    """
    import numpy as np

    airmask = (headmask == 0).astype(np.uint8)

    if rotmask is not None:
        airmask[rotmask > 0] = 0

    return airmask


def _computeQi2(img, airmask, min_voxels=int(1e3), max_voxels=int(3e5), coil_elements=32):
    """
    Compute Mortamet's QI2: goodness-of-fit of the background noise
    intensity distribution (within ``airmask``) onto a centered chi-square
    distribution.

    Ported from mriqc's ``mriqc.qc.anatomical.art_qi2``, keeping only the
    numeric computation. Unlike mriqc's version, this never writes an
    ``error.svg`` placeholder or fit plot to disk -- those are purely a
    reporting side effect, unconditional even when unwanted, that fsqc has
    no use for.

    Parameters
    ----------
    img : numpy.ndarray
        3D image array.
    airmask : numpy.ndarray
        Binary air/background mask, same shape as ``img``.
    min_voxels : int, optional
        Minimum number of positive-intensity background voxels required to
        attempt the fit; below this, QI2 is defined as 0.0 (default: 1000,
        matching mriqc).
    max_voxels : int, optional
        Background voxels are subsampled to at most this many for the KDE /
        chi-square fit (default: 300000, matching mriqc).
    coil_elements : int, optional
        Number of coil elements, used as the initial degrees-of-freedom
        guess for the chi-square fit (default: 32, matching mriqc).

    Returns
    -------
    float
        QI2: mean absolute difference between the KDE-estimated background
        intensity distribution and the fitted chi-square distribution, over
        the upper tail (above the KDE's half-maximum cutoff).
    """
    import numpy as np
    from scipy.stats import chi2
    from sklearn.neighbors import KernelDensity

    # S. Ogawa was born
    _rng = np.random.RandomState(1191935)

    data = np.nan_to_num(img[airmask > 0], posinf=0.0)
    data[data < 0] = 0

    if (data > 0).sum() < min_voxels:
        return 0.0

    data *= 100 / np.percentile(data, 99)
    modelx = data if len(data) < max_voxels else _rng.choice(data, size=max_voxels)

    x_grid = np.linspace(0.0, 110, 1000)

    # Estimate data pdf with KDE on a random subsample
    kde_skl = KernelDensity(kernel="gaussian", bandwidth=4.0).fit(modelx[:, np.newaxis])
    kde = np.exp(kde_skl.score_samples(x_grid[:, np.newaxis]))

    # Find cutoff
    kdethi = np.argmax(kde[::-1] > kde.max() * 0.5)

    # Fit X^2
    param = chi2.fit(modelx, coil_elements)
    chi_pdf = chi2.pdf(x_grid, *param[:-2], loc=param[-2], scale=param[-1])

    # Compute goodness-of-fit (gof)
    return float(np.abs(kde[-kdethi:] - chi_pdf[-kdethi:]).mean())


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

def checkMotion(
    subjects_dir,
    subject,
    ref_image="orig.mgz",
    nu_image="nu.mgz",
    output_dir=None,
    write_masks=False,
    rotmask_file=None,
    headmask_file=None,
    airmask_file=None,
    aseg_image="aseg.mgz",
    aparc_image="aparc+aseg.mgz",
    nb_erode_wm=3,
    nb_erode_csf=1,
    nb_dilate_headmask=10,
):
    """
    Compute MRIQC-style EFC, QI2, FBER, SNR and BG measures for a subject.

    All measures are computed on a single reference image grid, shared with
    the subject's FreeSurfer/FastSurfer ``aseg``/``aparc`` segmentation.
    Two resolved images are used, mirroring mriqc's own ``in_ras``/
    ``in_noinu`` split: ``ref_image`` (default ``orig.mgz``, FreeSurfer's
    own conformed-but-uncorrected volume) is conformed the way mriqc's
    anatomical workflow does (see :func:`_conformImageToRAS`) and used,
    unmodified, for QI2 and the rotation mask; ``nu_image`` (default
    ``nu.mgz``, FreeSurfer's own bias-field-corrected volume) is likewise
    conformed and used for the internally computed head mask, then
    harmonized (see :func:`_harmonizeImage`) by rescaling it so the eroded
    white-matter mask's median intensity is 1000, mirroring mriqc's own
    ``Harmonize`` step -- EFC, FBER, SNR and background stats are computed
    on this harmonized image. QI2 is computed on ``ref_image`` alone
    (conformed-but-unharmonized *and* not bias-corrected), matching mriqc's
    actual wiring (its QI2 node is fed ``in_ras``, not ``in_noinu``), via a
    local port of mriqc's QI2 computation (see :func:`_computeQi2`).

    Parameters
    ----------
    subjects_dir : str
        The directory containing subject data.
    subject : str
        The name of the subject.
    ref_image : str, optional
        Reference MRI volume under ``mri/`` (default: ``orig.mgz``). Must be
        on the same grid as ``aseg_image``/``aparc_image`` -- overriding it
        with an image on a different grid will fail closed (NaN metrics)
        once the tissue-segmentation shape check fails.
    nu_image : str, optional
        Bias-field-corrected (but not yet intensity-harmonized) MRI volume
        under ``mri/``, on the same grid as ``ref_image`` (default:
        ``nu.mgz``; pass ``orig_nu.mgz`` for FastSurfer output). Feeds the
        internally computed head mask and :func:`_harmonizeImage`,
        mirroring the role mriqc's own N4-bias-corrected ``inu_corrected``
        plays before its ``Harmonize`` step -- unlike mriqc, the bias
        correction itself is not reimplemented here; whatever correction
        FreeSurfer/FastSurfer applied to produce this file is reused as-is.
        Required to be present and on the same grid as ``ref_image``; if
        missing or mismatched, the motion metrics are returned as NaN.
    output_dir : str or None, optional
        Subject-specific metrics output folder to write debug mask images
        to (e.g. the caller's ``metrics_outdir``). Required for
        ``write_masks`` to have any effect.
    write_masks : bool, optional
        Debugging switch: if true and ``output_dir`` is given, save the
        intermediate images and masks used internally as NIfTI files under
        ``output_dir`` -- the conformed reference image (``conformed``),
        the conformed bias-corrected image (``nu_conformed``), the
        ``rotmask``, ``headmask``, ``airmask`` (whichever computed or
        externally supplied), a connected-components labeling of
        ``headmask`` (``headmask_components``, one label per connected
        component -- a fragmented, non-single-component head mask will show
        more than one label), the GM/WM/CSF tissue masks used for SNR
        (``gmmask``/``wmmask``/``csfmask``; ``wmmask`` is also the one used
        for harmonization), and the harmonized image (``harmonized``,
        derived from ``nu_conformed``) (default: ``False``).
    rotmask_file : str or None, optional
        Full path to an externally supplied rotation mask (NIfTI or
        FreeSurfer MGH/MGZ), in the same (conformed) grid as the resolved
        ``ref_image``. If omitted, the rotmask is computed internally via
        :func:`_computeRotmaskMortamet` (mriqc's Mortamet2009 hard-zero
        detection) directly on the conformed reference image.
    headmask_file : str or None, optional
        Full path to an externally supplied head mask (NIfTI or FreeSurfer
        MGH/MGZ), in the same (conformed) grid as the resolved
        ``ref_image``/``nu_image``. If omitted, the head mask is computed
        internally via :func:`_computeHeadmaskOtsu` (Otsu thresholding of
        the bias-corrected ``nu_image``, unioned with the ``aparc+aseg``
        segmentation, optionally dilated by ``nb_dilate_headmask``, holes
        filled, and rotmask voxels excluded). If explicitly given but
        unusable, the motion metrics are returned as NaN.
    airmask_file : str or None, optional
        Full path to an externally supplied air mask (NIfTI or FreeSurfer
        MGH/MGZ), in the same (conformed) grid as the resolved
        ``ref_image``, used for QI2, FBER,
        and the background statistics. If omitted, the air mask is computed
        internally via :func:`_computeAirmask` -- currently the complement
        of ``headmask`` (see ``headmask_file``) with rotmask voxels also
        excluded, though this may become a more elaborate computation in
        the future. If explicitly given but unusable, the motion metrics
        are returned as NaN.
    aseg_image : str, optional
        FreeSurfer/FastSurfer ``aseg`` segmentation under ``mri/``, used for
        the gray matter and CSF SNR masks (default: ``aseg.mgz``). Required
        to be present and on the same grid as ``ref_image``.
    aparc_image : str, optional
        FreeSurfer/FastSurfer ``aparc+aseg``-style segmentation under
        ``mri/``, used for the white matter SNR mask, for harmonization,
        and (when ``headmask_file`` is not given) to reinforce the
        internally computed head mask (default: ``aparc+aseg.mgz``; pass
        e.g. ``aparc.DKTatlas+aseg.deep.mgz`` for FastSurfer output).
        Required to be present and on the same grid as ``ref_image``.
    nb_erode_wm : int, optional
        Erosion (in voxels) applied to the cerebral white matter mask (plus
        corpus callosum and WM-hypointensities) used both for SNR and for
        harmonization (default: 3). Does *not* apply to cerebellar white
        matter, which is unioned in unedoded (too thin to survive this
        erosion) -- see :data:`_WM_LABELS_CEREBELLUM`.
    nb_erode_csf : int, optional
        Erosion (in voxels) applied to the CSF SNR mask (default: 1).
    nb_dilate_headmask : int or None, optional
        Structuring-element size (in voxels) for an optional binary
        dilation applied to the internally computed head mask (see
        :func:`_computeHeadmaskOtsu`), before hole-filling. ``0`` or
        ``None`` disables dilation (default: ``10``). Has no effect when
        ``headmask_file`` is given.

    Returns
    -------
    dict
        Dictionary with keys ``efc``, ``qi2``, ``fber``, ``snr_head``
        (SNR over the head mask), ``snr_tissue_gm``,
        ``snr_tissue_wm``, ``snr_tissue_csf``, ``snr_tissue_total`` (mean
        over GM/WM/CSF), and BG summary statistics: ``bg_mean``,
        ``bg_median``, ``bg_std``, ``bg_mad``, ``bg_kurtosis``, ``bg_p05``,
        ``bg_p95``, ``bg_n``.
    """
    import logging
    import warnings

    import numpy as np
    from scipy import ndimage as ndimg

    from fsqc.fsqcUtils import ensureDir

    # mriqc pulls in nipype/niworkflows, which are known to attach their own
    # handler(s) to the root logger as a side effect of import -- undoing
    # fsqc's own _start_logging() setup and causing every subsequent
    # logging.info/error() call in the process to print twice. Snapshot the
    # root logger's handlers before the import and strip anything it added,
    # so fsqc's own logging configuration is left untouched. Cheap to redo on
    # every call: after the first import, Python's module cache makes this a
    # no-op re-import, so no handlers get added and the loop below is empty.
    _root_logger = logging.getLogger()
    _handlers_before_mriqc = list(_root_logger.handlers)
    from mriqc.qc.anatomical import efc, fber, snr, summary_stats
    for _extra_handler in list(_root_logger.handlers):
        if _extra_handler not in _handlers_before_mriqc:
            _root_logger.removeHandler(_extra_handler)

    def _nan_metrics_dict():
        return {
            "efc": np.nan,
            "qi2": np.nan,
            "fber": np.nan,
            "snr_head": np.nan,
            "snr_tissue_gm": np.nan,
            "snr_tissue_wm": np.nan,
            "snr_tissue_csf": np.nan,
            "snr_tissue_total": np.nan,
            "bg_mean": np.nan,
            "bg_median": np.nan,
            "bg_std": np.nan,
            "bg_mad": np.nan,
            "bg_kurtosis": np.nan,
            "bg_p05": np.nan,
            "bg_p95": np.nan,
            "bg_n": 0,
        }

    logging.captureWarnings(True)
    logging.info("Computing MRIQC-style motion/noise metrics ...")

    if write_masks and output_dir is not None:
        ensureDir(output_dir)

    # resolve + conform the reference volume (single grid, shared with
    # aseg/aparc below); bail out with NaNs if it doesn't exist
    ref_path = os.path.join(subjects_dir, subject, "mri", ref_image)
    if not os.path.exists(ref_path):
        warnings.warn(
            "WARNING: could not find reference image " + ref_path
            + " for " + subject + ", returning NaNs.",
            stacklevel=2,
        )
        return _nan_metrics_dict()

    ref_img = _conformImageToRAS(ref_path)
    img_ras = ref_img.get_fdata()

    if write_masks and output_dir is not None:
        _save_nii(img_ras, ref_img.affine, os.path.join(output_dir, "conformed.nii.gz"), dtype="float32")

    # bias-field-corrected (but not yet intensity-harmonized) volume, on the
    # same grid as ref_image -- stands in for mriqc's inu_corrected, feeding
    # the internal headmask computation and _harmonizeImage below; qi2 and
    # the rotmask stay on the uncorrected img_ras, matching mriqc's in_ras
    # role. Bail out with NaNs if it doesn't exist or doesn't match img_ras's
    # grid, same fail-closed policy as the aseg/aparc segmentation below.
    nu_path = os.path.join(subjects_dir, subject, "mri", nu_image)
    if not os.path.exists(nu_path):
        warnings.warn(
            "WARNING: could not find bias-corrected image " + nu_path
            + " for " + subject + ", returning NaNs.",
            stacklevel=2,
        )
        return _nan_metrics_dict()

    nu_img = _conformImageToRAS(nu_path)
    img_nu = nu_img.get_fdata()
    if img_nu.shape[:3] != img_ras.shape[:3]:
        warnings.warn(
            "WARNING: bias-corrected image " + nu_path + " has shape "
            + str(img_nu.shape[:3]) + ", expected " + str(img_ras.shape[:3])
            + " for " + subject + ", returning NaNs.",
            stacklevel=2,
        )
        return _nan_metrics_dict()

    if write_masks and output_dir is not None:
        _save_nii(img_nu, nu_img.affine, os.path.join(output_dir, "nu_conformed.nii.gz"), dtype="float32")

    # aseg/aparc segmentation, on the same grid as ref_image, required for
    # tissue masks, harmonization, and (when headmask_file is not given)
    # internal headmask computation. aseg/aparc live in FreeSurfer's native
    # (unconformed, typically LIA) orientation, same as ref_image before
    # conforming -- conform=True reorients them to RAS to stay voxel-aligned
    # with img_ras/img_harmonized, since matching shape alone (both 256^3
    # cubes) doesn't guarantee matching orientation.
    aseg_path = os.path.join(subjects_dir, subject, "mri", aseg_image)
    aparc_path = os.path.join(subjects_dir, subject, "mri", aparc_image)
    seg = {}
    for seg_name, seg_path in (("aseg", aseg_path), ("aparc", aparc_path)):
        try:
            seg[seg_name] = _load_external_mask(
                seg_path, seg_name, img_ras.shape[:3], binarize=False, conform=True
            )
        except Exception as exc:
            warnings.warn(
                "WARNING: could not use " + seg_name + " " + seg_path
                + " (" + str(exc) + "), returning NaNs.",
                stacklevel=2,
            )
            return _nan_metrics_dict()
    aseg_data = seg["aseg"]
    aparc_data = seg["aparc"]

    # rotmask: externally supplied, or computed internally
    if rotmask_file is not None:
        try:
            rotmask = _load_external_mask(rotmask_file, "rotmask", img_ras.shape[:3])
            logging.info("Using external rotmask " + rotmask_file)
        except Exception as exc:
            warnings.warn(
                "WARNING: could not use external rotmask " + rotmask_file
                + " (" + str(exc) + "), returning NaNs.",
                stacklevel=2,
            )
            return _nan_metrics_dict()
    else:
        rotmask = _computeRotmaskMortamet(img_ras)

    # headmask: externally supplied, or computed internally via Otsu
    # thresholding unioned with the aparc+aseg segmentation
    if headmask_file is not None:
        try:
            headmask = _load_external_mask(headmask_file, "headmask", img_ras.shape[:3])
            logging.info("Using external headmask " + headmask_file)
        except Exception as exc:
            warnings.warn(
                "WARNING: could not use external headmask " + headmask_file
                + " (" + str(exc) + "), returning NaNs.",
                stacklevel=2,
            )
            return _nan_metrics_dict()
    else:
        headmask = _computeHeadmaskOtsu(
            img_nu, aparc_data, rotmask=rotmask, nb_dilate=nb_dilate_headmask
        )

    # airmask: externally supplied, or computed internally as the
    # complement of headmask
    if airmask_file is not None:
        try:
            airmask = _load_external_mask(airmask_file, "airmask", img_ras.shape[:3])
            logging.info("Using external airmask " + airmask_file)
        except Exception as exc:
            warnings.warn(
                "WARNING: could not use external airmask " + airmask_file
                + " (" + str(exc) + "), returning NaNs.",
                stacklevel=2,
            )
            return _nan_metrics_dict()
    else:
        airmask = _computeAirmask(headmask, rotmask=rotmask)

    if write_masks and output_dir is not None:
        _save_nii(rotmask, ref_img.affine, os.path.join(output_dir, "rotmask.nii.gz"))
        _save_nii(headmask, ref_img.affine, os.path.join(output_dir, "headmask.nii.gz"))
        _save_nii(airmask, ref_img.affine, os.path.join(output_dir, "airmask.nii.gz"))

        # debug: label each connected component of headmask individually,
        # so a fragmented (non-single-component) head mask is visible
        headmask_components, _ = ndimg.label(headmask)
        _save_nii(
            headmask_components, ref_img.affine,
            os.path.join(output_dir, "headmask_components.nii.gz"), dtype="int32",
        )

    gm_mask = _tissue_mask_from_labels(aseg_data, _GM_LABELS, nb_erode=0)
    wm_mask_cerebrum = _tissue_mask_from_labels(aparc_data, _WM_LABELS, nb_erode=nb_erode_wm)
    wm_mask_cerebellum = _tissue_mask_from_labels(aparc_data, _WM_LABELS_CEREBELLUM, nb_erode=0)
    wm_mask = wm_mask_cerebrum | wm_mask_cerebellum
    csf_mask = _tissue_mask_from_labels(aseg_data, _CSF_LABELS, nb_erode=nb_erode_csf)

    if write_masks and output_dir is not None:
        _save_nii(gm_mask, ref_img.affine, os.path.join(output_dir, "gmmask.nii.gz"))
        _save_nii(wm_mask, ref_img.affine, os.path.join(output_dir, "wmmask.nii.gz"))
        _save_nii(csf_mask, ref_img.affine, os.path.join(output_dir, "csfmask.nii.gz"))

    # harmonize: rescale so the white-matter mask's median intensity is
    # 1000, mirroring mriqc's in_noinu
    img_harmonized = _harmonizeImage(img_nu, wm_mask)
    if img_harmonized is None:
        warnings.warn(
            "WARNING: could not harmonize reference image for " + subject
            + " (empty or degenerate white-matter mask), returning NaNs.",
            stacklevel=2,
        )
        return _nan_metrics_dict()

    if write_masks and output_dir is not None:
        _save_nii(
            img_harmonized, ref_img.affine, os.path.join(output_dir, "harmonized.nii.gz"),
            dtype="float32",
        )

    # one summary_stats() call, on the harmonized image, feeds tissue SNR,
    # head SNR, and background stats
    stats = summary_stats(
        img_harmonized,
        {"gm": gm_mask, "wm": wm_mask, "csf": csf_mask, "head": headmask, "bg": airmask},
    )

    tissue_snr = {}
    for label in ("gm", "wm", "csf"):
        tissue_snr["snr_tissue_" + label] = snr(
            stats[label]["median"], stats[label]["stdv"], stats[label]["n"]
        )
    finite_tissue_snr = [v for v in tissue_snr.values() if np.isfinite(v)]
    tissue_snr["snr_tissue_total"] = (
        float(np.mean(finite_tissue_snr)) if finite_tissue_snr else np.nan
    )

    snr_head_value = snr(stats["head"]["median"], stats["head"]["stdv"], stats["head"]["n"])

    bg_stats = {
        "bg_mean": stats["bg"]["mean"],
        "bg_median": stats["bg"]["median"],
        "bg_std": stats["bg"]["stdv"],
        "bg_mad": stats["bg"]["mad"],
        "bg_kurtosis": stats["bg"]["k"],
        "bg_p05": stats["bg"]["p05"],
        "bg_p95": stats["bg"]["p95"],
        "bg_n": int(stats["bg"]["n"]),
    }

    metrics = {
        "efc": efc(img_harmonized, framemask=rotmask),
        "qi2": _computeQi2(img_ras, airmask=airmask),
        "fber": fber(img_harmonized, headmask=headmask, rotmask=rotmask),
        "snr_head": snr_head_value,
    }
    metrics.update(tissue_snr)
    metrics.update(bg_stats)

    # Summary logging for quick visual sanity-checking in pipeline logs.
    logging.info("EFC: " + f"{metrics['efc']:.4}" if np.isfinite(metrics["efc"]) else "EFC: nan")
    logging.info("QI2: " + f"{metrics['qi2']:.4}" if np.isfinite(metrics["qi2"]) else "QI2: nan")
    logging.info("FBER: " + f"{metrics['fber']:.4}" if np.isfinite(metrics["fber"]) else "FBER: nan")
    logging.info(
        "SNR_HEAD: " + f"{metrics['snr_head']:.4}"
        if np.isfinite(metrics["snr_head"])
        else "SNR_HEAD: nan"
    )
    logging.info(
        "SNR_TISSUE_TOTAL: " + f"{metrics['snr_tissue_total']:.4}"
        if np.isfinite(metrics["snr_tissue_total"])
        else "SNR_TISSUE_TOTAL: nan"
    )

    return metrics