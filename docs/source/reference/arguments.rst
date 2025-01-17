=============
Arguments
=============

Positional arguments
--------------------
Positional arguments are arguments that are passed to a command as a list of strings. They are defined using the :func:`pos_option` decorator.

.. literalinclude:: examples/arguments/positional.py
   :language: python

Keyword arguments
-----------------
Keyword arguments are arguments that are passed to a command as a dictionary of strings. They are defined using the :func:`kw_option` decorator.

.. literalinclude:: examples/arguments/keyword.py
   :language: python