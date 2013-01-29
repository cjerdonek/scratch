Releasing Pizza
===============

This document contains detailed step-by-step instructions for Pizza maintainers
on how to release both the first version and new versions of Pizza.
For instructions on installing or using the application, or for instructions
on contributing, consult the README or
[project page](https://github.com/cjerdonek/groome-python-expected) instead.

Table of contents:

1.  Background
2.  One-time setup
    * 2.1. Set up PyPI user accounts
    * 2.2. Create `.pypirc` file
3.  Releasing a new version
    * 3.1. Finalize source
      * 3.1.1. Review issues
      * 3.1.2. Update HISTORY file
      * 3.1.3. Double-check the `sdist`
      * 3.1.4. Bump version number
      * 3.1.5. Update `long_description` file
      * 3.1.6. Make sure tests pass
    * 3.2. Merge to release branch, if necessary
    * 3.3. Register version on PyPI
    * 3.4. Upload version to PyPI
    * 3.5. Tag the commit


