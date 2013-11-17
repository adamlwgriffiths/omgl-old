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

* SVO?
* RLE / Hilbert Curve?





Shader
------

Add glsl version to methods or have sub functions per method?
  def func(self):
    def glsl_120():
        return 'abc'
    def glsl_320():
        return 'def'

  or

  def func(self):
    if glsl_version() <= 120:
        return 'abc'
    else:
        return 'def'

  or

  @glsl(versions=[150])
  def func(self):
    pass

  @glsl(versions=[120])
  def func(self):
    pass


Add 'global' location dictionary?
 Shader.locations['in_position'] = 2


VertexBuffer
------------

v = VertexBuffer(100, [('in_position', np.float32, 3),('in_normal', np.int32, 3)])
v['in_position'] = [1,2,3,4,5]

v2 = InterleavedVertexBuffer(100, [('in_position', np.float32, 3),('in_normal', np.int32, 3)])
v2['in_position'] = [1,2,3,4,5]
v2.sync()






VertexBuffer  <- ArrayBuffer
              <- ElementBuffer
              <- TextureBuffer



ArrayBuffer(100, in_position=(np.float32, 3))
ArrayBuffer(100, [('in_position, np.float32, 3)])






# vertex weights
w = VertexBuffer(100, [('in_weights', np.float32, 16), ('in_weight_indices', np.int16, 4)])

# indices
e1 = ElementBuffer([('triangles', GL.GL_TRIANGLES, 100), ('quads', GL.GL_QUADS, 120)])
e2 = ElementBuffer([('triangle_strip', GL.GL_TRI_STRIP, 100)])

# bones
s = TextureBuffer(50, np.float32, GL.GL_RGBA32F)
t = s.texture






glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, data.nbytes, data.data, GL_STATIC_DRAW`)



# texture buffer for Random-access of bones
glBindBuffer(GL_TEXTURE_BUFFER, self.vbo)
glBufferData(GL_TEXTURE_BUFFER, matrices.nbytes, matrices.data, GL_STATIC_DRAW)

glBindTexture(GL_TEXTURE_BUFFER, self.tbo)
glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, self.vbo)

glActiveTexture(GL_TEXTURE0 + 4)
glBindTexture(GL_TEXTURE_BUFFER, self.tbo)




# index array
glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, bo )
glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data.data, GL_STATIC_DRAW)
glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.vbos.indices )
glDrawElements(GL_TRIANGLES, num_indices, GL_UNSIGNED_INT, offset)





glEnableVertexAttribArray(3)
glVertexAttribPointer(index, count, GL_FLOAT, GL_FALSE, stride, offset)



Materials
---------


m = Material
m['in_tex_diffuse'] = texture
m['in_tex_normal'] = texture

s = TextureBuffer(50, np.float32, GL.GL_RGBA32F)
m['in_bones'] = s.texture





SharedVertexBuffer
------------------

Create buffer's from a single global buffer like Doom 3

buffer = MyBuffer.create(num_vertices)
# uses the attributes to determine size, ie
# size = sum([attr.type * attr.count * num_vertices for attr in attrs])


AutoVertexBuffer
----------------

class MyBuffer(AutoVertexBuffer):
    in_position = BufferDataType('float32', 3)

buffer = MyBuffer()
buffer.in_position = [1,2,3,4,5,6]





Shader
------

p = Program(VertexShader(source), FragmentShader(source), in_position=1)
p['in_uniform'] = [4,5,6]

AutoShader
----------
shader model



Renderable / VAO
----------------

Auto binding vertex buffers to shader locations

s = Shader()
b1 = ArrayBuffer(100, [('in_position', np.float32, 3)])
b2 = ArrayBuffer(100, [('in_normal', np.float32, 3)])
e1 = EnumerationBuffer([('triangles', GL.GL_TRIANGLES, 100), ('quads', GL.GL_QUADS, 120)])
e2 = EnumerationBuffer([('triangle_strip', GL.GL_TRI_STRIP, 100)])


r = RenderState(shader, b1, b2, e1, e2)
r.shader = shader
r.add_buffer(b1)
r.remove_buffer(b2)
r.add_buffer(e1)

r.push()
r.render(GL.GL_TRIANGLES)
r.render('triangles')
r.render('quads')
r.render() # renders all
r.pop()



glEnableVertexAttribArray( 3 )
glVertexAttribPointer( 3, 4, GL_FLOAT, GL_FALSE, stride, offset + (4 * 0) )



Scene Graph
-----------

Auto bind variables?
  matrix
  frame count
  time










BufferObject
------------


from omgl.buffer import ArrayBuffer
b = ArrayBuffer(target, [('in_position', np.float, 100, 3)])
b['in_position'] = [1,2,3,4,5] * 20
b.push()
b.pop()



ArrayBuffer.allocate(target, nbytes)
b = ArrayBuffer.aquire(nbytes)
# re-allocate
# same as release / aquire with same size
b.allocate()
b.release()



locations = {
  'in_position': 1,
  'in_diffuse': 2,
}
buffer.bind(locations)





m = Material()
m['in_diffuse'] = texture()
m['in_skeleton'] = TextureBuffer.texture


b = BufferArray()
with b:
  b.push(buffer1)
  b.push(buffer2)

with b:
  with material1:
    b.draw('quads')
    b.draw('body')
  with material2:
    b.draw('triangles')
    b.draw('head')




ArrayBuffer
------------
n = np.empty(5, dtype=np.float32)
b = ArrayBuffer(n)
b[:] = n
b.bind()
# bind = 1 value per vertex

n = np.empty(5, dtype=(np.float32, 3))
b = ArrayBuffer(n)
b[:] = n
b.bind()

n = np.empty(5, dtype=[('in_position', np.float32, 3)])
b = ArrayBuffer(n)
b[:] = n
b['in_position'] = n
b.bind(in_position=5)

n = np.empty(1, dtype=[('triangles', np.int32, 100)])
b = ElementBuffer(n)

n = np.empty(1, dtype=[('triangles', np.int32, 3)], polygons={'triangles': GL.GL_TRIANGLES})
b = ElementBuffer(n)

Texture
-------

n = np.empty((32,32), dtype=np.float32)
t = Texture2D(n)




UI
--

integrate pyui
-in pygly virtualenv



Design
------
-create lower level state management functions
-implement higher level objects ontop of these calls


-Consider using Direct State Acces
 https://www.opengl.org/registry/specs/EXT/direct_state_access.txt
This would ease state management massively
instead of managing the state machine, most functions take a handle
allows state to change without object being active


consider using more extensions
-many good ones in valve opengl talk
 https://www.youtube.com/watch?v=btNVfUygvio
-Direct State Access
-multi texturing (glBindMultiTexture(unit, target, handle))
provide alternate function with same api for non supporting platforms





Auto-Binding to Shaders
-----------------------

GlobalState.set_variable('abc', a)
# abc is visible, def is hidden from autobind
GlobalState.enable_variables(abc=True, def=False)
GlobalState.auto_bind(shader)


OpenGL 3.3 features
-------------------
geometry shader
sampler objects
swizzling


OpenGL 4 features
-----------------
https://en.wikipedia.org/wiki/OpenGL#OpenGL_4.0

texture barrier
texture buffer
seperate shader objects
tesselation shaders
instancing
compute / draw indirect
uniform buffers - read / write
es2 compatibility









State Management
----------------


texture[100] = 50
# preserve existing bindings and update data
texture.sync()

gl.state.texture(0, texture)
gl.state.texture(1, texture)

def sync(self):
  with gl.state.texture.preserve(0, texture):
    GL.glTexSubImage(...)


with texture:
  texture.blah = blah

with BindTexture(0, texture):
  texture.blah = blah







Mesh
----

mesh(shader, np_data, material)

mesh(vertices=[], normals=[], indices=[])



