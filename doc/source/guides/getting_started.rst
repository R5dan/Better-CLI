***************
Getting Started
***************

This guide will walk you through the process of creating a simple CLI application using Better CLI.

Installation
============

To install Better CLI, you can use pip:

.. code-block:: bash

    pip install bettercli

Creating a CLI
==============

To create a CLI, you first need to import the ``CLI`` class from the ``bettercli`` module:

.. literalinclude:: ../examples/cli.py
   :language: python
   :lines: 1-3

Adding commands
===============

Next, you need to add commands to the CLI. Commands are defined using the ``command`` decorator:

.. literalinclude:: ../examples/command.py
   :language: python

``command`` takes a single argument, which is the name of the command. The name of the command is used to identify the command when running the CLI.

Running the CLI
===============

Finally, you can run the CLI by calling the ``run`` method of the CLI object:

.. literalinclude:: ../examples/cli.py
   :language: python
   :lines: 5-

Adding arguments
================

You can add arguments to your commands by using the ``pos_option`` and ``kw_option`` decorators. These decorators take the following arguments:



To add a positional argument, you can use the ``pos_option`` decorator:

.. literalinclude:: ../examples/arguments/positional.py
   :language: python

To add a keyword argument, you can use the ``kw_option`` decorator:

.. literalinclude:: ../examples/arguments/keyword.py
   :language: python

