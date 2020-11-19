RetroRules's Documentation
==========================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _RetroRules: https://retrorules.org/
.. _RetroPath2.0: https://github.com/Galaxy-SynBioCAD/RetroPath2

Welcome RetroRules's documentation. This tool provides a docker that can be accessed using the command line interface for dynamically generating reaction rules file, from RetroRules_ that is RetroPath2.0_ friendly.  

To build the docker, you can use the following command:

.. code-block:: bash

   docker build -t brsynth/retrorules-standalone:v2 .

To return the reaction rules, you can call the run function using:

.. code-block:: bash

   python run.py -rule_type retro -output rules.tar -diameters 2,8 -output_format tar

API
###

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. currentmodule:: rpTool

.. autoclass:: passRules
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: rpToolServe

.. autoclass:: passRules
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:
