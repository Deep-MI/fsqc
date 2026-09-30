"""Tests for the configurable screenshot overlay alpha (--screenshots_alpha)."""

import inspect
import re
import sys

import pytest

from fsqc.createScreenshots import createScreenshots
from fsqc.evaluateFornixSegmentation import evaluateFornixSegmentation
from fsqc.evaluateHippocampalSegmentation import evaluateHippocampalSegmentation
from fsqc.evaluateHypothalamicSegmentation import evaluateHypothalamicSegmentation
from fsqc.fsqcMain import (
    _check_arguments,
    _do_fsqc,
    _parse_arguments,
    run_fsqc,
)

# The pre-existing public parameter lists, pinned verbatim so that appending the
# alpha parameter can never silently move an existing positional index.
PREEXISTING = {
    "createScreenshots": [
        "SUBJECT",
        "SUBJECTS_DIR",
        "OUTFILE",
        "INTERACTIVE",
        "LAYOUT",
        "BASE",
        "OVERLAY",
        "LABELS",
        "SURF",
        "SURFCOLOR",
        "VIEWS",
        "XLIM",
        "YLIM",
        "BINARIZE",
        "ORIENTATION",
    ],
    "run_fsqc": [
        "subjects_dir",
        "output_dir",
        "argsDict",
        "subjects",
        "subjects_file",
        "shape",
        "screenshots",
        "screenshots_html",
        "screenshots_base",
        "screenshots_overlay",
        "screenshots_surf",
        "screenshots_views",
        "screenshots_layout",
        "screenshots_orientation",
        "surfaces",
        "surfaces_html",
        "surfaces_views",
        "skullstrip",
        "skullstrip_html",
        "fornix",
        "fornix_html",
        "hypothalamus",
        "hypothalamus_html",
        "hippocampus",
        "hippocampus_html",
        "hippocampus_label",
        "outlier",
        "outlier_table",
        "fastsurfer",
        "no_group",
        "group_only",
        "exit_on_error",
        "skip_existing",
        "motion_rotmask",
        "motion_headmask",
        "motion_airmask",
        "logfile",
    ],
    "evaluateFornixSegmentation": [
        "SUBJECT",
        "SUBJECTS_DIR",
        "OUTPUT_DIR",
        "CREATE_SCREENSHOT",
        "SCREENSHOTS_OUTFILE",
        "RUN_SHAPEDNA",
        "N_EIGEN",
        "WRITE_EIGEN",
    ],
    "evaluateHippocampalSegmentation": [
        "SUBJECT",
        "SUBJECTS_DIR",
        "OUTPUT_DIR",
        "CREATE_SCREENSHOT",
        "SCREENSHOTS_OUTFILE",
        "SCREENSHOTS_ORIENTATION",
        "HEMI",
        "LABEL",
    ],
    "evaluateHypothalamicSegmentation": [
        "SUBJECT",
        "SUBJECTS_DIR",
        "OUTPUT_DIR",
        "CREATE_SCREENSHOT",
        "SCREENSHOTS_OUTFILE",
        "SCREENSHOTS_ORIENTATION",
    ],
}

# alpha parameter name per callable
ALPHA_NAME = {
    "createScreenshots": "ALPHA",
    "run_fsqc": "screenshots_alpha",
    "evaluateFornixSegmentation": "SCREENSHOTS_ALPHA",
    "evaluateHippocampalSegmentation": "SCREENSHOTS_ALPHA",
    "evaluateHypothalamicSegmentation": "SCREENSHOTS_ALPHA",
}

CALLED_BY_NAME = {
    "createScreenshots": createScreenshots,
    "run_fsqc": run_fsqc,
    "evaluateFornixSegmentation": evaluateFornixSegmentation,
    "evaluateHippocampalSegmentation": evaluateHippocampalSegmentation,
    "evaluateHypothalamicSegmentation": evaluateHypothalamicSegmentation,
}


def _argv(tmp_path, *extra):
    """Build a minimal argv that satisfies the two required CLI arguments."""
    return [
        "run_fsqc",
        "--subjects_dir",
        str(tmp_path),
        "--output_dir",
        str(tmp_path),
        *extra,
    ]


# ---------------------------------------------------------------------------
# parser


def test_parser_default_alpha(tmp_path, monkeypatch):
    """--screenshots_alpha defaults to 0.5 when the option is not given."""
    monkeypatch.setattr(sys, "argv", _argv(tmp_path))
    argsDict = _parse_arguments()
    assert argsDict["screenshots_alpha"] == 0.5


def test_parser_explicit_alpha(tmp_path, monkeypatch):
    """--screenshots_alpha is parsed as a float and forwarded to argsDict."""
    monkeypatch.setattr(sys, "argv", _argv(tmp_path, "--screenshots_alpha", "0.15"))
    argsDict = _parse_arguments()
    assert argsDict["screenshots_alpha"] == 0.15


# ---------------------------------------------------------------------------
# validation


@pytest.mark.parametrize("value", [-0.01, 1.5])
def test_check_arguments_rejects_out_of_range_alpha(tmp_path, value):
    """Out-of-range alpha is rejected and the message names the offending value."""
    argsDict = {"subjects_dir": str(tmp_path), "screenshots_alpha": value}
    message = re.escape(
        f"screenshots_alpha must be between 0 and 1, got {value}"
    )
    with pytest.raises(ValueError, match=message):
        _check_arguments(argsDict)


def test_check_arguments_accepts_valid_alpha(tmp_path):
    """A valid alpha passes the guard and validation continues to later checks.

    The dict is deliberately minimal: it satisfies the alpha guard and the
    subjects-directory check (tmp_path exists), then stops at the first
    unrelated key it needs ("subjects"). The KeyError therefore proves the
    alpha guard did not fire.
    """
    argsDict = {"subjects_dir": str(tmp_path), "screenshots_alpha": 0.25}
    with pytest.raises(KeyError):
        _check_arguments(argsDict)


def test_check_arguments_defaults_missing_alpha(tmp_path):
    """A legacy argsDict without the key is defaulted to 0.5."""
    argsDict = {"subjects_dir": str(tmp_path)}
    assert "screenshots_alpha" not in argsDict

    with pytest.raises(KeyError):
        _check_arguments(argsDict)

    assert argsDict["screenshots_alpha"] == 0.5


@pytest.mark.parametrize("value", [-0.5, 1.2])
def test_create_screenshots_rejects_out_of_range_alpha(value):
    """createScreenshots validates ALPHA before touching any image data.

    A non-existent subjects directory is passed on purpose: the ValueError
    proves the guard runs ahead of the image-loading stage.
    """
    with pytest.raises(ValueError, match="ALPHA must be between 0 and 1"):
        createScreenshots("subj", "/nonexistent-subjects-dir", "out.png", ALPHA=value)


# ---------------------------------------------------------------------------
# signature compatibility


@pytest.mark.parametrize("name", sorted(PREEXISTING))
def test_alpha_parameter_appended_last(name):
    """The alpha parameter is appended last; no pre-existing index moves."""
    func = CALLED_BY_NAME[name]
    params = list(inspect.signature(func).parameters)

    assert params[:-1] == PREEXISTING[name]
    assert params[-1] == ALPHA_NAME[name]
    assert inspect.signature(func).parameters[params[-1]].default == 0.5


# ---------------------------------------------------------------------------
# forwarding
#
# Driving run_fsqc() and the evaluators to their screenshot call sites requires
# processed FreeSurfer/FastSurfer MRI data, which this repository has no fixture
# for. Forwarding is therefore asserted against the call sites in the function
# source. The counts below are the full set of forwarding sites.


def test_fsqc_main_forwards_alpha_to_all_call_sites():
    """fsqc passes alpha to both createScreenshots and all three evaluators."""
    # run_fsqc() is a thin wrapper that delegates to _do_fsqc(), which holds
    # the actual module call sites.
    src = inspect.getsource(_do_fsqc)

    # regular screenshot call + skull-strip screenshot call
    # (lookbehind so the SCREENSHOTS_ALPHA keyword is not counted here)
    create_calls = re.findall(
        r'(?<!SCREENSHOTS_)ALPHA=argsDict\["screenshots_alpha"\],', src
    )
    assert len(create_calls) == 2
    # hypothalamus, hippocampus lh, hippocampus rh, fornix
    assert src.count('SCREENSHOTS_ALPHA=argsDict["screenshots_alpha"],') == 4


@pytest.mark.parametrize(
    "func", [evaluateFornixSegmentation, evaluateHippocampalSegmentation,
             evaluateHypothalamicSegmentation]
)
def test_evaluator_forwards_alpha_to_create_screenshots(func):
    """Each evaluator passes its alpha through to createScreenshots."""
    assert "ALPHA=SCREENSHOTS_ALPHA," in inspect.getsource(func)
