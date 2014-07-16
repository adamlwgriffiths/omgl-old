OpenGL
======

* Support or drop legacy?
* ES2.0 compatible?
* GL3.3 or GL4+?


Buffers
=======

[X] ArrayBuffer
[X] ElementBuffer
[ ] TextureBuffer


Shared Buffers
==============


Textures
========

[X] Texture1D
[X] Texture2D
[X] Texture3D
[ ] CubeMap
[ ] Skybox
[ ] TextureBuffer
[ ] Channel swizzle


Shaders
=======

[X] Vertex Shaders
[X] Fragment Shaders
[ ] Geometry Shaders
[ ] Tesselation Shaders(?)
[X] Program


AutoShader
==========

[X] GLSL decorator
[X] GLSL version handling in decorator

* Use Schematics or take what we need and drop it?


Shader / Buffer Bindings
========================

[ ] Shader
[ ] Buffers
[ ] Textures
[ ] Set / unset attributes
[ ] Resync when buffer changes(?)


Shader Library
==============

[ ] Fixed function replacements
[ ] Deferred lighting
[ ] Skinning

* Wrappers for GLSL functions > current version


Maths
=====

[ ] Matrix3 class
[ ] Matrix4 class
[ ] Vector3
[ ] Quaternion


Windowing
=========

[ ] Window class
[ ] Viewport class


Shapes
======

[ ] UV Generators
[ ] Rect generator
[ ] Cube generator
[ ] Sphere generator


Scene Management
================

[ ] Scene Graph
[ ] QuadTree
[ ] Octree
[ ] Kd-Tree (scipy?)
[ ] Portals
[ ] 2D Tile map
[ ] 3D Tile map
[ ] 2D Tile map zooming / LOD
[ ] 2D Isometric


Mesh
====

[ ] Mesh
[ ] Skeleton
[ ] Animation
[ ] Sprite
[ ] Billboard (axis-aligned sprite)

Mesh Formats
============

[ ] MD2
[ ] MD3
[ ] MD4
[ ] MD5
[ ] MD5r
[ ] MD6
[ ] OBJ
[ ] 3DS
[ ] ASE
[ ] DMX
[ ] SMD
[ ] MS3D
[ ] X
[ ] IQM (Inter-Quake Model format)
[ ] UDMF (Universal Doom Map Format)
[ ] Doom BSP

* Use PyAssimp? Docs are horrible, especially for custom python bindings


UI
==

* Create GL3+ PyUI(?)


Physics
=======

[ ] Bullet
[ ] Box2D

* Seperate lib?


Audio
=====

?

* Seperate lib?


IPC / Parallelism
=================

?

* Seperate lib?


Voxel
=====

* 3D Numpy Array
* Volume Ray Tracing Shader
* SVO?
* RLE / Hilbert Curve?
