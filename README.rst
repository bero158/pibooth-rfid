============
pibooth-rfid
============

|PythonVersions| 

``pibooth-rfid`` is a plugin for `pibooth` application.

It allows to read NFC tags in "Choose" screen

Install
-------

    Clone this repository to your Raspberry Pi and set plugin path at ~/.config/pibooth/pibooth.cfg

Configuration
-------------

In config.py:
  comment DEVEL = 1
  Set PLUGIN_ROOT to the absolute plugin path.
  
Below are the new configuration options available in the `pibooth`_ configuration.
**The keys and their default values are automatically added to your configuration after first** `pibooth`_ **restart.**

.. code-block:: ini

    [RFID]
    # Json file with badge, uid and ID database
    DB File = "/home/pi/pibooth/pibooth-rfid/data/badges_db.json

    # Folder with badges (jpeg image cca 100x100px, RGB, with .jpg extension)
    Badge Folder = "/home/pi/pibooth/pibooth-rfid/data/badges"

    # Path to Default image. This image is used if there's no badge image.
    Default image = "/home/pi/pibooth/pibooth-rfid/nobody.jpg"


.. note:: Edit the configuration by running the command ``pibooth --config``.

!!! Write sructure of badge_db.json !!!

.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+
