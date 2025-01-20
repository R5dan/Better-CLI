=================
Spinner
=================

.. currentmodule:: bettercli.cl

The ``Spinner`` class is used to create a terminal spinner animation.

.. autosummary::
   :toctree: api/

   Spinner

Example
----------

Here is an example of how to create a spinner:

.. literalinclude:: ../../examples/cl/spinner.py
   :language: python

Style
------

The ``style`` parameter is used to customize the appearance of the spinner. It is a dictionary that maps the style of the spinner to a dictionary of style attributes. The available style attributes are:

- ``bg-color``: The background color of the spinner.
- ``fg-color``: The foreground color of the spinner.
- ``states``: A list of dictionaries that define the states of the spinner. Each dictionary has the following keys:
    - ``symbol``: The symbol to use for the state.
    - ``wait``: The time to wait before switching to the next state.
    - ``message``: A dictionary that defines the message to display for the state. The dictionary has the following keys:
        - ``fg-color``: The foreground color of the message.
        - ``bg-color``: The background color of the message.
        - ``message``: The message to display.

Here is an example of how to customize the appearance of the spinner:

.. literalinclude:: ../../examples/cl/spinner/style.py
   :language: python