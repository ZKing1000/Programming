import math
import sys

from pyglet.gl import *
import pyglet

class Sprite(pyglet.sprite.Sprite):

    def __init__(self,
                 img,
                 **kwargs):
                 
        self._z = kwargs.get('z', 0)
        super(Sprite, self).__init__(img, **kwargs)


    def _create_vertex_list(self):
        if self._batch is None:
            self._vertex_list = graphics.vertex_list(4,
                'v3f/%s' % self._usage, 
                'c4B', ('t3f', self._texture.tex_coords))
        else:
            self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
                'v3f/%s' % self._usage, 
                'c4B', ('t3f', self._texture.tex_coords))
        self._update_position()
        self._update_color()

    def _update_position(self):
        img = self._texture
        if not self._visible:
            self._vertex_list.vertices[:] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self._rotation:
            x1 = -img.anchor_x * self._scale
            y1 = -img.anchor_y * self._scale
            x2 = x1 + img.width * self._scale
            y2 = y1 + img.height * self._scale
            x = self._x
            y = self._y
            z = self._z
            
            r = -math.radians(self._rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            ax = int(x1 * cr - y1 * sr + x)
            ay = int(x1 * sr + y1 * cr + y)
            bx = int(x2 * cr - y1 * sr + x)
            by = int(x2 * sr + y1 * cr + y)
            cx = int(x2 * cr - y2 * sr + x)
            cy = int(x2 * sr + y2 * cr + y)
            dx = int(x1 * cr - y2 * sr + x)
            dy = int(x1 * sr + y2 * cr + y)

            self._vertex_list.vertices[:] = [ax, ay, z, bx, by, z, cx, cy, z, dx, dy, z]
        elif self._scale != 1.0:
            x1 = int(self._x - img.anchor_x * self._scale)
            y1 = int(self._y - img.anchor_y * self._scale)
            x2 = int(x1 + img.width * self._scale)
            y2 = int(y1 + img.height * self._scale)
            z = self._z
            
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]
        else:
            x1 = int(self._x - img.anchor_x)
            y1 = int(self._y - img.anchor_y)
            x2 = x1 + img.width
            y2 = y1 + img.height
            z = self._z
            
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]

    def _set_z(self, z):
        self._z = z
        self._update_position()

    z = property(lambda self: self._z, _set_z,
                 doc='''Z coordinate of the sprite.

    :type: int
    ''')


