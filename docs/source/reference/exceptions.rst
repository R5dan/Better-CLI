==========
Exceptions
==========

.. currentmodule:: bettercli

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

.. autoclass:: BetterCLIException
    :members:

**************
InvalidOption
**************

``InvalidOption`` is the base class for invalid option exceptions.

.. autoclass:: InvalidOption
    :members:

****************
InvalidType
****************

``InvalidType`` is raised when an option is not of the correct type.

*****************
InvalidLength
*****************

``InvalidLength`` is raised when an option is not the correct length.