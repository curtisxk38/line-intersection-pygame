import pygame
import control
import colors

class MainState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.SCREEN_SIZE = pygame.display.get_surface().get_size()
        self.pressed_keys = pygame.key.get_pressed()
        self.vertex_control = 0
        self.vertex_list = []

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(self.vertex_list) < 4:
                self.vertex_list.append(pygame.math.Vector2(*pygame.mouse.get_pos()))
            else:
                self.vertex_list[self.vertex_control] = pygame.math.Vector2(*pygame.mouse.get_pos())
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            self.pressed_keys = pygame.key.get_pressed()
            if self.pressed_keys[pygame.K_ESCAPE]:
                self.quit = True
            elif self.pressed_keys[pygame.K_TAB]:
                self.change_control()

    def update(self, screen):
        # Draw
        screen.fill(colors.WHITE)
        for i, vertex in enumerate(self.vertex_list):
            color = colors.RED if i == self.vertex_control else colors.BLUE
            pygame.draw.circle(screen, color, vec_ituple(vertex), 7)
        if len(self.vertex_list) >= 2:
            pygame.draw.line(screen, colors.BLACK, vec_tuple(self.vertex_list[0]), vec_tuple(self.vertex_list[1]), 3)
        if len(self.vertex_list) == 4:
            pygame.draw.line(screen, colors.BLACK, vec_tuple(self.vertex_list[2]), vec_tuple(self.vertex_list[3]), 3)
            poi = intersect(self.vertex_list[0],
                      self.vertex_list[2],
                      self.vertex_list[1] - self.vertex_list[0],
                      self.vertex_list[3] - self.vertex_list[2]
            )
            if poi is not None:
                pygame.draw.circle(screen, colors.GREEN, vec_ituple(poi), 4)

    def change_control(self):
        self.vertex_control += 1
        if self.vertex_control > len(self.vertex_list)-1:
            self.vertex_control = 0

def vec_tuple(vec):
    return vec.x, vec.y

def vec_ituple(vec):
    return int(vec.x), int(vec.y)

def intersect(p, q, r, s):
    """
    https://stackoverflow.com/questions/563198/whats-the-most-efficent-way-to-calculate-where-two-line-segments-intersect/565282#565282
    https://github.com/pgkelley4/line-segments-intersect/blob/master/js/line-segments-intersect.js
    """
    diff = q - p
    r_x_s = r.cross(s)
    diff_x_r = diff.cross(r)

    if r_x_s == 0:
        if diff_x_r == 0:
            print("collinear")
            t_0 = diff.dot(r) / r.dot(r)
            t_1 = (q+s-p).dot(r) / r.dot(r)
            raise NotImplemented("Collinear case not implemented")
        else:
            print("parallel")
            return None

    t = diff.cross(s) / r_x_s
    u = diff_x_r / r_x_s

    if 0 <= t <= 1 and 0 <= u <= 1:
        print("intersect")
        return p + t * r
    print("do not intersect")
    return None


