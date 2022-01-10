====================================
**bananaBread**: *A Bot for Discord*
====================================

**bananaBread** is a Python library for managing a Discord Bot

* Scripts are written in Python 3.9.7

* This project is under active development.

* Documentation can be found `here <https://kktnl.github.io/functional-discord-bot/>`_ << - This project is not functional :))

* Currently supported modules are:

    * ``pycmd``

    * ``getmedia``
    

"""""""""""""
(Some) Changes Made:
"""""""""""""

* Started employing ``pdoc3`` instead of ``sphinx`` for documentation.

* Changed the content of ``.gitignore``, so that the documentation files with .html extension that are created via ``pdoc3`` will not be committed. This means there is no on-the-go documentation for the program hosted over github-pages. You have to run ``pdoc3`` on your own machine.

* Filing structure is changed.

* Primitive use of ``config.py`` is employed. (More to come..)

""""""""""""""""""""
Identified Problems:
""""""""""""""""""""

* pdoc3 cannot document most of the functions in ``handle_discord``. Refer to script until fixed.

* Due to an error yet unknown, media downloads are sometimes halted, but does not break the code. Check terminal to ensure there is no error until it is fixed.

* Not sure which req.txt is more suitable so included both for now.

* Guide for reStructuredText is used when writing docstrings. Therefore documentation may look a bit bizarre until fixed.

**Currently supported modules are**

    #. ``pydiscmd``

    #. ``getmedia``
