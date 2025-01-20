=============
Input Widget
=============

.. currentmodule:: bettercli.cl

The ``Input`` class is a widget that allows the user to enter text. It can be used to create a simple command line interface (CLI) that prompts the user for input.

.. autosummary::
   :toctree: api/

   Input

Example
-------

Here is an example of how to use the ``Input`` class to create a simple CLI that prompts the user for their name:

.. code-block:: python

   from bettercli.cl import Input

   name = Input("What is your name? ").run()
   print(f"Hello, {name}!")

This code will display a prompt asking the user to enter their name, and then print a greeting message with their name.

Customization
-------------

The ``Input`` class can be customized in several ways to create a more interactive and user-friendly CLI. Here are some examples of how to customize the ``Input`` class:

- Change the prompt message:

  .. code-block:: python

     from bettercli.cl import Input

     name = Input("What is your name? ").run()
     print(f"Hello, {name}!")

- Add a validator function to check the input:

  .. code-block:: python

     from bettercli.cl import Input

     def validate_name(input):
         if len(input) < 3:
             return "Name must be at least 3 characters long"
         return True

     name = Input("What is your name? ", validator=validate_name).run()
     print(f"Hello, {name}!")

- Add a style to the input:

  .. code-block:: python

     from bettercli.cl import Input

     name = Input("What is your name? ", style={"fg-color": "red"}).run()
     print(f"Hello, {name}!")

- Add a keybind to the input:

  .. code-block:: python

     from bettercli.cl import Input

     name = Input("What is your name? ", keybinds={"enter": Input.select_and_enter}).run()
     print(f"Hello, {name}!")