from math import *

from Settings import *

def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # rotates point around another point
    def rotate(self, degrees, center):
        angle = degrees * pi / 180
        new_x = cos(angle) * (self.x - center.x) - sin(angle) * (self.y - center.y)
        new_y = sin(angle) * (self.x - center.x) + cos(angle) * (self.y - center.y)

        self.x = new_x + center.x
        self.y = new_y + center.y


class movable:
    def __init__(self, x, y, x_size, y_size, vx = 0, vy = 0):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def off_map(self):
        if self.x + self.x_size < 0 or res_x + 150 < self.x - self.x_size:
            return True
        if self.y + self.y_size < 0 or res_y < self.y - self.y_size:
            return True
        return False
    

        # shows text on screen
class text_window:
    def __init__(self, x, y, width = 200, height = 150, text_list = [], timer = 240):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_list = text_list
        self.timer = timer

    # adds text to queue
    def add_text(self, text):
        self.text_list.append( [font.render(str(text), False, (255,255,255)), self.timer, text] )

    # shows texts on screen
    def show_text(self, window):
        position_y = self.y
        for text in self.text_list:

            position_x = self.x + self.width - len(text[2]) * 10 - 20
            window.blit(text[0], (position_x, position_y))
            position_y += font_size + 5

            text[1] -= 1
            if text[1] <= 0:
                self.text_list.remove(text)