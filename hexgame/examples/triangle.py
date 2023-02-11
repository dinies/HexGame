import numpy as np
from OpenGL.GL import GL_VERTEX_ARRAY
from OpenGL.GL import GL_FLOAT
from OpenGL.GL import GL_TRIANGLES
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import glEnableClientState
from OpenGL.GL import glClear
from OpenGL.GL import glClearColor
from OpenGL.GL import glDrawArrays
from OpenGL.GL import glVertexPointer
import glfw


class Window(object):
    def __init__(self, name):
        glfw.init()
        # creating a window size having 900 as width and 700 as height
        self.glwindow = glfw.create_window(900, 700, name, None, None)
        glfw.set_window_pos(self.glwindow, 500, 300)
        glfw.make_context_current(self.glwindow)

    def __del__(self):
        glfw.terminate()


def drawTriangle(window):
    vertices = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0, 0.5, 0.0]

    v = np.array(vertices, dtype=np.float32)

    # this will draw a colorless triangle
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    # this will set a color for your background
    glClearColor(255, 180, 0, 0)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glfw.swap_buffers(window)


def main():
    window = Window("Triangle")
    drawTriangle(window.glwindow)


if __name__ == "__main__":
    main()
