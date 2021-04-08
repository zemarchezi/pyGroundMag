"""Print the version number for the current installation."""


def version():
    """
    Print the pygroundmag version number.

    Returns
    -------
    None.

    """
    import pkg_resources
    ver = pkg_resources.get_distribution("pygroundmag").version
    print("pygroundmag version: " + ver)
