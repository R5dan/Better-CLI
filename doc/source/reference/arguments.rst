=============
Arguments
=============

.. currentmodule:: bettercli.option

Positional arguments
--------------------
Positional arguments are arguments that are passed to a command as a list of strings. They are defined using the :func:`pos_option` decorator.

.. literalinclude:: ../examples/arguments/positional.py
   :language: python

This  returns a instance of the :class:`Positional_option` class.

.. autosummary::
   :toctree: api/

   Positional_option

Keyword arguments
-----------------
Keyword arguments are arguments that are passed to a command as a dictionary of strings. They are defined using the :func:`kw_option` decorator.

.. literalinclude:: ../examples/arguments/keyword.py
   :language: python

This  returns a instance of the :class:`Keyword_option` class.

.. autosummary::
   :toctree: api/

   Keyword_option