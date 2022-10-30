import math
from re import S
import pygame
from pygame import Vector2
from tile import Tile
import utils
from world import World


class GridRay:
    color2 = (20,80,1)
    def __init__(self, pos: Vector2, dir: Vector2) -> None:
        self.pos = pos
        self.dir = dir
        self.intersect = Vector2(0,0)

    def update(self, world: list[list[Tile]]):
        # protect from division by 0
        if self.dir.x == 0:
            self.dir.x = 0.000001
        if self.dir.y == 0:
            self.dir.y = 0.000001
        self.dir.normalize_ip() # ensures dir is normalized
        dy_dx = self.dir.y / self.dir.x
        dx_dy = self.dir.x / self.dir.y

        step_x = math.sqrt(1 + (dy_dx**2))
        step_y = math.sqrt(1 + (dx_dy**2))

        unit_step = Vector2(step_x, step_y)

        map_pos = Vector2(int(self.pos.x), int(self.pos.y)) 
        ray_length = Vector2(0,0)

        step = Vector2(0,0)

        if self.dir.x < 0:
            step.x = -1
            ray_length.x = (self.pos.x - map_pos.x) * unit_step.x
        else:
            step.x = 1
            ray_length.x = (map_pos.x + 1 - self.pos.x) * unit_step.x
    
        if self.dir.y < 0:
            step.y = -1
            ray_length.y = (self.pos.y - map_pos.y) * unit_step.y
        else:
            step.y = 1
            ray_length.y = (map_pos.y + 1 - self.pos.y) * unit_step.y

        endTileFound = False
        maxDistance = 100
        currentDistance = 0
        while (not endTileFound) and currentDistance < maxDistance:
            if ray_length.x < ray_length.y:
                map_pos.x += step.x
                currentDistance = ray_length.x
                ray_length.x += unit_step.x
            else:
                map_pos.y += step.y
                currentDistance = ray_length.y
                ray_length.y += unit_step.y

            # in bounds
            if map_pos.x >= 0 and map_pos.y >= 0 and map_pos.x < len(world[0]) and map_pos.y < len(world):
                if world[int(map_pos.y)][int(map_pos.x)] != 0:
                    endTileFound = True


        self.intersect = self.pos + self.dir * currentDistance
        
    def draw(self, screen):
        pygame.draw.line(screen, (255,230,255), camera.projectVector(self.pos * Tile.tileSize), camera.projectVector(self.intersect * Tile.tileSize))

    def get_pt_at_radius(self, radius):
        if radius > self.pos.distance_to(self.intersect):
            return self.intersect
        return self.pos + (self.dir * radius)

def draw_lighting(screen:pygame.Surface, camera: utils.Camera, radius):
    vertices: list[Vector2] = []
    max_x = -1000000
    min_x = 10000000
    max_y = -1000000
    min_y = 1000000
    for ray in rays:
        pt = ray.get_pt_at_radius(radius) * Tile.tileSize
        max_x = max(pt.x, max_x)
        max_y = max(pt.y, max_y)
        min_x = min(pt.x, min_x)
        min_y = min(pt.y, min_y)
        vertices.append(pt)
    
    polygon_width = abs(max_x - min_x)
    polygon_height = abs(max_y - min_y)

    for vertice in vertices:
        vertice.x -= min_x
        vertice.y -= min_y

    temp_surf = pygame.Surface((int(polygon_width), int(polygon_height)))
    bounding_rect = pygame.draw.polygon(temp_surf, GridRay.color2, vertices)
    screen.blit(temp_surf, camera.projectPoint((min_x, min_y)), special_flags=pygame.BLEND_RGB_ADD)


if __name__ == "__main__":
    from utils import camera
    pygame.init()
    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
    clock = pygame.time.Clock()

    world = World()

    rays_pos = Vector2(5,4)
    rays: list[GridRay] = []
    num_rays = 60
    spacing = 360 / (num_rays-1)
    

    for i in range(num_rays):
        angle_rad = utils.deg2rad(i*spacing)
        direction = Vector2(math.cos(angle_rad), math.sin(angle_rad))
        rays.append(GridRay(rays_pos, direction))
    

    # ray = GridRay(Vector2(5,5), Vector2(1,0))

    ticks = 0
    running_time = 0
    while True:
        delta = clock.tick() / 1000
        ticks+=1
        running_time += delta
        if running_time >= 1:
            print(f"Ticks per second: {ticks}")
            ticks = 0
            running_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        ray_spd = 2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            rays_pos.y -= ray_spd * delta
        if keys[pygame.K_a]:
            rays_pos.x -= ray_spd * delta
        if keys[pygame.K_s]:
            rays_pos.y += ray_spd * delta
        if keys[pygame.K_d]:
            rays_pos.x += ray_spd * delta
        if keys[pygame.K_RETURN]:
            print(pygame.mouse.get_pos())

        # mouse_pos = pygame.mouse.get_pos()
        # mouse_tile_pos = Vector2(camera.unprojectPoint(mouse_pos)) / Tile.tileSize

        world.update()
        
        tiles = world.getCurrentChunk().getCurrentRoom().foregroundMap
        for ray in rays:
            ray.pos = rays_pos
            ray.update(tiles)
    

        # i hate this btw, just make a getForegroundTiles() function in World. Also,
        # what is the difference between foregroundMap and foregroundTiles?
        # ray.dir = Vector2(mouse_tile_pos - ray.pos)

        camera.lerp_to(rays[0].pos.x * Tile.tileSize, rays[0].pos.y * Tile.tileSize, 0.3)

    
        screen.fill((0,0,0))
        world.render(screen)
        # pygame.draw.circle(screen, (255,120,0), screen_ray_start_pos, 10)
        # pygame.draw.line(screen, (230,230,230), screen_ray_start_pos, screen_ray_end_pos, 3)
        # draw_lighting(screen, camera, 200)
        # # draw_lighting(screen, camera, 200)
        # draw_lighting(screen, camera, 500)
        # draw_lighting(screen, camera, 1000)
        
        for ray in rays:
            ray.draw(screen)
        draw_lighting(screen, camera, 2)
        # for wall in walls:
        #     wall.draw(screen, camera)


        pygame.display.flip()
