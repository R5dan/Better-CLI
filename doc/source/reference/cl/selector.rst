=================
Selector
=================

.. currentmodule:: bettercli.cl

The ``Selector`` class is a subclass of the ``bettercli.cl.CommandLine`` class and is used to create a selector for selecting an option from a list of options.

.. autosummary::
   :toctree: api/

   Selector

Example
----------

Here is an example of how to create a selector:

.. literalinclude:: ../../examples/cl/selector/multi.py
   :language: python
   :lines: 1-10

This creates a selector with the following options:

- Option 1: "option1 description"
- Option 2: "option2 description"
- Option 3: "option3 description"

And the following question: "What do you want to do?"

Validator
----------

The ``validator`` method is used to validate the selected options. It takes a list of selected options as an argument and returns either ``True`` if the options are valid or a string describing the error if they are not valid.

Here is an example of how to use the ``validator`` method:

.. literalinclude:: ../../examples/cl/selector/validator.py
   :language: python
   :lines: 12-17

This validator checks that at least two options are selected. If less than two options are selected, it returns an error message.

Style
------

The ``style`` parameter is used to customize the appearance of the selector. It is a dictionary that maps the style of the selector to a dictionary of style attributes. The available style attributes are:

- ``bg-color``: The background color of the selector.
- ``fg-color``: The foreground color of the selector.
- ``symbol``: The symbol to use for the selector.
- ``width``: The width of the selector.
- ``height``: The height of the selector.

Here is an example of how to customize the appearance of the selector:

.. literalinclude:: ../../examples/cl/selector/style.py
   :language: python
   :lines: 1-10

This customizes the appearance of the selector to have a red background color, white foreground color, and a symbol of ``●``.

.. autosummary::
   :toctree: api/

   Selector.style

Keybinds
---------

The ``keybinds`` parameter is used to customize the keybinds of the selector. It is a dictionary that maps the name of the keybind to a function that is called when the keybind is pressed. The available keybinds are:

- ``left``: Select all options.
- ``right``: Unselect all options.
- ``up``: Move the cursor up.
- ``down``: Move the cursor down.
- ``space``: Toggle the selection of the current option.
- ``enter``: Select the current option.

Here is an example of how to customize the keybinds of the selector:
Use the ``hook.name`` of ``keyboard`` to add keybinds to the selector:

Single Selector
----------------

The ``SingleSelector`` class is a subclass of the ``Selector`` class and is used to create a selector for selecting a single option from a list of options.

Example
----------

Here is an example of how to create a single selector:

.. literalinclude:: ../../examples/cl/selector/single.py
   :language: python
   :lines: 1-10

This creates a single selector with the following options:

- Option 1: "option1 description"
- Option 2: "option2 description"
- Option 3: "option3 description"

And the following question: "What do you want to do?"

``SingleSelector`` has the same methods and attributes as ``Selector`` except:
* ``max`` is set to 1
* ``min`` is set to 1
* ``run`` returns a single option instead of a list of options


