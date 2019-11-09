import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math


class Way:
    def __init__(self, args, longitude, latitude, altitude, roll, pitch, yaw, height, width):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.photos = args
        self.scree = 0
        self.check_bool = [False]*len(self.photos[0])
        self.textures = []
        self.polygons = []
        self.meters_per_pixel_h = 1 / 600
        self.meters_per_pixel_w = 1 / 600
        for i in range(len(self.photos)):
            self.createPoly(math.sqrt(0.8**2 + 1.25**2), self.roll[i], self.latitude[i] * self.meters_per_pixel_w,
                            self.longitude[i] * self.meters_per_pixel_h, 1.25)
        self.display()

    def createPoly(self, r, s, x_coord, y_coord, width):  # r - radius s - angle
        w = 360 / 4
        point = []
        polygon = []

        t1 = w * 0 + s + 45
        x1 = r * math.cos(math.radians(t1))
        y1 = r * math.sin(math.radians(t1))
        point.append(np.array([x1, y1, 0]))

        t2 = w * 1 + s + 45
        x2 = r * math.cos(math.radians(t2))
        y2 = r * math.sin(math.radians(t2))
        point.append(np.array([x2, y2, 0]))

        t3 = w * 2 + s + 45
        x3 = r * math.cos(math.radians(t3))
        y3 = r * math.sin(math.radians(t3))
        point.append(np.array([x3, y3, 0]))

        t4 = w * 3 + s + 45
        x4 = r * math.cos(math.radians(t4))
        y4 = r * math.sin(math.radians(t4))
        point.append(np.array([x4, y4, 0]))

        len1 = np.linalg.norm(point[3] - point[0])
        temp_point1 = point[3] + (point[0] - point[3]) * ((len1 + width) / len1)

        len2 = np.linalg.norm(point[2] - point[1])
        temp_point2 = point[2] + (point[1] - point[2]) * ((len2 + width) / len2)

        len3 = np.linalg.norm(point[1] - point[2])
        temp_point3 = point[1] + (point[2] - point[1]) * ((len3 + width) / len3)

        len4 = np.linalg.norm(point[0] - point[3])
        temp_point4 = point[0] + (point[3] - point[0]) * ((len4 + width) / len4)

        polygon.append([x_coord + temp_point1[0], y_coord + temp_point1[1]])
        polygon.append([x_coord + temp_point2[0], y_coord + temp_point2[1]])
        polygon.append([x_coord + temp_point3[0], y_coord + temp_point3[1]])
        polygon.append([x_coord + temp_point4[0], y_coord + temp_point4[1]])
        self.polygons.append(polygon)

    def loadTexture(self, photo, i):
        textureSurface = pygame.image.load(photo).convert()
        textureSurface = pygame.transform.scale(textureSurface, (800, 600))
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.check_bool[i] = True
        self.textures.append(texid)

    def display(self):
        pygame.init()
        display = (800, 640)
        self.scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

        sphere = gluNewQuadric()

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()

        # init mouse movement and center mouse on screen
        displayCenter = [self.scree.get_size()[i] // 2 for i in range(2)]
        mouseMove = [0, 0]
        pygame.mouse.set_pos(displayCenter)

        up_down_angle = 0.0
        left_right_angle = 0.0
        paused = False
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        run = False
                    if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_pos(displayCenter)
                if not paused:
                    if event.type == pygame.MOUSEMOTION:
                        mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                    pygame.mouse.set_pos(displayCenter)

            if not paused:
                # get keys
                keypress = pygame.key.get_pressed()
                # mouseMove = pygame.mouse.get_rel()

                # init model view matrix
                glLoadIdentity()

                # apply the look up and down
                up_down_angle += mouseMove[1] * 0.1
                glRotatef(up_down_angle, 1.0, 0.0, 0.0)

                # init the view matrix
                glPushMatrix()
                glLoadIdentity()

                # apply the movment
                if keypress[pygame.K_w]:
                    glTranslatef(0, 0, 0.1)
                if keypress[pygame.K_s]:
                    glTranslatef(0, 0, -0.1)
                if keypress[pygame.K_d]:
                    glTranslatef(-0.1, 0, 0)
                if keypress[pygame.K_a]:
                    glTranslatef(0.1, 0, 0)
                if keypress[pygame.K_q]:
                    glTranslatef(0, -0.1, 0)
                if keypress[pygame.K_e]:
                    glTranslatef(0, 0.1, 0)

                # apply the left and right rotation
                glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

                # multiply the current matrix by the get the new view matrix and store the final vie matrix
                glMultMatrixf(viewMatrix)
                viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

                glPopMatrix()
                glMultMatrixf(viewMatrix)
                glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                glPushMatrix()

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glEnable(GL_TEXTURE_2D)
                glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                for i in range(len(self.photos)):
                    if not self.check_bool[i]:
                        self.loadTexture(self.photos[i], i)
                    glBindTexture(GL_TEXTURE_2D, self.textures[i])
                    glBegin(GL_QUADS)
                    glTexCoord(0, 0)
                    glVertex3f(self.polygons[i][0][0],
                               self.polygons[i][0][1],
                               -5)
                    print(self.latitude[i] * self.meters_per_pixel_w)
                    glTexCoord(0, 1)
                    glVertex3f(self.polygons[i][1][0],
                               self.polygons[i][1][1],
                               -5)
                    glTexCoord(1, 1)
                    glVertex3f(self.polygons[i][2][0],
                               self.polygons[i][2][1],
                               -5)
                    glTexCoord(1, 0)
                    glVertex3f(self.polygons[i][3][0],
                               self.polygons[i][3][1],
                               -5)
                    glEnd()

                glPopMatrix()

                pygame.display.flip()
                pygame.time.wait(10)

        pygame.quit()
