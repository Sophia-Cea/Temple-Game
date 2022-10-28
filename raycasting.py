import math
from re import S
import pygame
from pygame import Vector2
import utils


class Wall:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, screen, camera: utils.Camera):
        pygame.draw.line(screen, (245, 225, 245), camera.projectPoint(self.p1), camera.projectPoint(self.p2), 2)

class Ray:
    color = (255, 0, 0)
    color2 = (20,50,21)
    def __init__(self, pos: Vector2, dir: Vector2) -> None:
        self.pos = pos
        self.dir = dir.normalize()
        self.p2 = self.pos + self.dir * 20
    
    def look_at(self, point: Vector2):
        self.dir = (point - self.pos).normalize()

    def cast(self, wall_pt_1: tuple, wall_pt_2: tuple) -> Vector2 | None:
        x1 = wall_pt_1[0]
        x2 = wall_pt_2[0]
        y1 = wall_pt_1[1]
        y2 = wall_pt_2[1]

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 -x4)
        if den == 0: 
            return None
        
        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / den
        u = -((x1-x2) * (y1-y3) - (y1-y2)*(x1-x3)) / den

        if t > 0 and t < 1 and u > 0:
            return Vector2(x1 + t *(x2-x1), (y1 + t * (y2 - y1)))
        else:
            return None

    def update(self, world: list[Wall]):
        closest_end_pt = Vector2(self.pos + self.dir * 1000000)
        closest_dist = 100000000
        for wall in world:
            end_pt = self.cast(wall.p1, wall.p2)
            if end_pt is None:
                continue
            d = self.pos.distance_squared_to(end_pt)
            if d < closest_dist:
                closest_end_pt = end_pt
                closest_dist = d
        self.p2 = closest_end_pt
        
    def get_pt_at_radius(self, r):
        d = self.pos.distance_to(self.p2)
        if d < r:
            return self.p2
        return Vector2(self.pos + r * self.dir)
        
    def draw(self, screen, camera: utils.Camera):
        pygame.draw.line(screen, Ray.color, camera.projectVector(self.pos), camera.projectVector(self.p2))

def draw_lighting(screen:pygame.Surface, camera: utils.Camera, radius):
    vertices: list[Vector2] = []
    max_x = -1000000
    min_x = 10000000
    max_y = -1000000
    min_y = 1000000
    for ray in rays:
        pt = ray.get_pt_at_radius(radius)
        max_x = max(pt.x, max_x)
        max_y = max(pt.y, max_y)
        min_x = min(pt.x, min_x)
        min_y = min(pt.y, min_y)
        vertices.append(ray.get_pt_at_radius(radius))
    
    polygon_width = abs(max_x - min_x)
    polygon_height = abs(max_y - min_y)

    for vertice in vertices:
        vertice.x -= min_x
        vertice.y -= min_y

    temp_surf = pygame.Surface((int(polygon_width), int(polygon_height)))
    bounding_rect = pygame.draw.polygon(temp_surf, Ray.color2, vertices)
    screen.blit(temp_surf, camera.projectPoint((min_x, min_y)), special_flags=pygame.BLEND_RGB_ADD)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
    clock = pygame.time.Clock()
    camera = utils.Camera()

    rays: list[Ray] = []
    num_rays = 60
    spacing = 360 / (num_rays-1)
    for i in range(num_rays):
        angle_rad = utils.deg2rad(i*spacing)
        direction = Vector2(math.cos(angle_rad), math.sin(angle_rad))
        rays.append(Ray(Vector2(utils.WIDTH/2, utils.HEIGHT/2), direction))
    walls = [Wall((10,10), (10,-500)), Wall((10,10), (500, 10))]

    while True:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.yOffest -= 50 * delta
        if keys[pygame.K_a]:
            camera.xOffset -= 50 * delta
        if keys[pygame.K_s]:
            camera.yOffest += 50 * delta
        if keys[pygame.K_d]:
            camera.xOffset += 50 * delta
               
        mouse_pos = pygame.mouse.get_pos()
        rays_pos = camera.unprojectPoint(mouse_pos)
        for ray in rays:
            ray.pos.x = rays_pos[0]
            ray.pos.y = rays_pos[1]
            ray.update(walls)  
            
        screen.fill((0,0,0))

        draw_lighting(screen, camera, 100)
    
        for ray in rays:
            ray.draw(screen, camera)
        for wall in walls:
            wall.draw(screen, camera)

        pygame.display.flip()
