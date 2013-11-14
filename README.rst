====
OMGL
====

A Pythonic 2D / 3D framework providing power through simplicity.


Dependencies
============

* Python 2.7
* NumPy
* PyOpenGL
* Schematics


Design
======

OMGL is designed to be similar to numpy in usage, specifically using functions as proxies to object creation rather than directly instantiating objects.

For example::

    omgl.array_buffer.empty((2,2))

    omgl.vertex_shader.create('source code')


By calling creation functions, implementation details can be abstracted from the user, and the classes can undergo heavy modification without difficulty supporting the existing API.

This also allows OMGL to be accessable with a single import call, which avoids the complexity of importing from large libraries.
