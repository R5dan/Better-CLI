==========
Exceptions
==========

.. currentmodule:: bettercli.exceptions

Exceptions
----------

Better CLI defines the following exceptions:

- `BetterCLIException <bettercli.BetterCLIException>`
- `InvalidOption <bettercli.InvalidOption>`
- `InvalidType <bettercli.InvalidType>`
- `InvalidLength <bettercli.InvalidLength>`

***************
BetterCLIException
***************

``BetterCLIException`` is the base class for all exceptions raised by Better CLI.
It is the base class for ``InvalidOption``

.. autosummary::
    :members:

    BetterCLIException

**************
InvalidOption
**************

``InvalidOption`` is the base class for invalid option exceptions.

.. autosummary::
    :members:

    exceptions.InvalidOption

****************
InvalidType
****************

``InvalidType`` is raised when an option is not of the correct type.

*****************
InvalidLength
*****************

``InvalidLength`` is raised when an option is not the correct length.