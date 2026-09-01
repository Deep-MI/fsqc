import os
import time

import pytest

from fsqc.fsqcUtils import ensureDir


def test_ensure_dir_creates_missing_directories(tmp_path):
    """Test that missing directories, including parents, are created."""
    target = tmp_path / "metrics" / "subject-01"
    assert not target.is_dir()

    ensureDir(str(target))

    assert target.is_dir()


def test_ensure_dir_accepts_existing_directory(tmp_path):
    """Test that an existing directory is left alone."""
    target = tmp_path / "metrics"
    target.mkdir()
    (target / "metrics.csv").write_text("subject\n")

    ensureDir(str(target))

    assert target.is_dir()
    assert (target / "metrics.csv").read_text() == "subject\n"


def test_ensure_dir_recovers_from_outdated_metadata(tmp_path, monkeypatch):
    """Test that a FileExistsError for an existing directory is tolerated."""
    target = tmp_path / "metrics"
    target.mkdir()

    calls = []
    makedirs = os.makedirs

    def flaky_makedirs(path, *args, **kwargs):
        # emulate a filesystem whose outdated cache makes the os.path.isdir()
        # check within os.makedirs() fail for a directory that does exist
        calls.append(path)
        if len(calls) == 1:
            raise FileExistsError(17, "File exists", str(path))
        return makedirs(path, *args, **kwargs)

    monkeypatch.setattr(os, "makedirs", flaky_makedirs)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)

    ensureDir(str(target))

    assert calls == [str(target), str(target)]
    assert target.is_dir()


def test_ensure_dir_reports_persistent_errors(tmp_path):
    """Test that a file blocking the path raises and is not removed."""
    target = tmp_path / "metrics"
    target.write_text("not a directory\n")

    with pytest.raises(FileExistsError):
        ensureDir(str(target), retries=0)

    assert target.is_file()
    assert target.read_text() == "not a directory\n"
