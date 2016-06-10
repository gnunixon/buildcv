Work
====
Each user can have a lot of works. The base class for this is :py:class:`udata.models.Work`. The name of employer (`inst` attribute) is language independent (alos `begin_year` and `end_year`). The position and comments can be translated (`function` and `comments` attribute).

Descrition of the class and inner methods
-----------------------------------------

.. autoclass:: udata.models.Work
    :members:


Additional functions
--------------------
At the same time we have some additional functions for hepling us in our work.

.. automodule:: udata.views
    :members: create_work
