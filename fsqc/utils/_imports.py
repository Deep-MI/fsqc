"""Handle optional dependency imports.

Inspired from pandas: https://pandas.pydata.org/
"""

import importlib

# A mapping from import name to package name (on PyPI) when the package name
# is different.
INSTALL_MAPPING = {
    "sksparse": "scikit-sparse",
}


def import_optional_dependency(
    name: str,
    extra: str = "",
    raise_error: bool = True,
):
    """Import an optional dependency.

    By default, if a dependency is missing an ImportError with a nice message
    will be raised.

    Parameters
    ----------
    name : str
        The module name.
    extra : str, default=""
        Additional text to include in the ImportError message.
    raise_error : bool, default=True
        What to do when a dependency is not found.
        * True : Raise an ImportError.
        * False: Return None.

    Returns
    -------
    module : Optional[ModuleType]
        The imported module when found.
        None is returned when the package is not found and raise_error is
        False.

    Raises
    -------
    ImportError
        dependency not found; see raise_error
    """

    package_name = INSTALL_MAPPING.get(name)
    install_name = package_name if package_name is not None else name

    try:
        module = importlib.import_module(name)
    except ImportError as err:
        if raise_error:
            raise ImportError(
                f"Missing optional dependency '{install_name}'. {extra} "
                f"Use pip or conda to install {install_name}."
            ) from err
        else:
            return None

    return module
