import math
from re import S
from numpy import poly
import pygame
from pygame import Rect, Surface, Vector2
from tile import Tile
import utils
from world import World

class LightSource:
    ambient_light = 0.2
    color = (0.5, 0.4, 0.3) # orange-y red
    _ambient_color = (255*ambient_light, 255*ambient_light, 255*ambient_light)
    def __init__(self, pos: Vector2, num_rays: int, radii: list[float]) -> None:
        self.pos = pos
        self.num_rays = num_rays
        self.rays: list[Ray] = []
        self.radii = radii
        self.radii.sort()

        c = LightSource.color
        strength = 255/len(radii)
        self.color = (c[0] * strength, c[1]*strength, c[2]*strength)
    
        spacing = 360 / (num_rays-1)
        for i in range(num_rays):
            angle_rad = utils.deg2rad(i*spacing)
            direction = Vector2(math.cos(angle_rad), math.sin(angle_rad))
            self.rays.append(Ray(self.pos, direction))

    def set_pos(self, pos: Vector2):
        for ray in self.rays:
            ray.pos = pos

    def update(self, tile_map: list[list[Tile]]):
        for ray in self.rays:
            ray.update(tile_map)

    def debug_draw(self, screen: pygame.Surface):
        for ray in self.rays:
            ray.draw(screen)

    def draw(self, screen: pygame.Surface):
        # draw full lighting onto temp surface with blend_add, then blit with blend_mult onto dest
        polygons: list[tuple[list[Vector2], Rect]] = []
        
        for radius in self.radii:
            polygons.append(self._get_lighting_polygon(radius))

        biggest = polygons[-1][1]
        top_left = biggest.topleft

        temp_surf = pygame.Surface(biggest.size) # last polygon is the biggest, and thus the polygon we want to make the surface surround
        temp_surf.set_colorkey((0,0,0))
        for polygon in polygons:
            self._translate_polygon(polygon[0], top_left)
            self._draw_polygon(polygon[0], temp_surf)
        
        t = pygame.Surface((utils.WIDTH, utils.HEIGHT))
        t.fill(LightSource._ambient_color)
        t.blit(temp_surf, camera.project(biggest))
        screen.blit(t, (0,0), special_flags=pygame.BLEND_MULT)

    def _translate_polygon(self, polygon: list[Vector2], top_left: tuple[int, int]):
        for vertice in polygon:
            vertice.x -= top_left[0]
            vertice.y -= top_left[1]

    def _draw_polygon(self, polygon: list[Vector2], surface: pygame.Surface):
        temp_surf = Surface(surface.get_size())
        pygame.draw.polygon(temp_surf, self.color, polygon)
        surface.blit(temp_surf, (0,0), special_flags=pygame.BLEND_ADD)

    def _get_lighting_polygon(self, radius):
        vertices: list[Vector2] = []
        max_x = -1000000
        min_x = 10000000
        max_y = -1000000
        min_y = 1000000
        # collect polygon vertices (scale to pixels) (world position)
        for ray in self.rays:
            pt = ray.get_pt_at_radius(radius) * Tile.tileSize
            max_x = max(pt.x, max_x)
            max_y = max(pt.y, max_y)
            min_x = min(pt.x, min_x)
            min_y = min(pt.y, min_y)
            vertices.append(pt)
            
        # find bounds of polygon
        polygon_width = abs(max_x - min_x)
        polygon_height = abs(max_y - min_y)

        return vertices, Rect(min_x, min_y, polygon_width, polygon_height)
        

class Ray:
    color2 = (198,255,180)
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



if __name__ == "__main__":
    from utils import camera
    pygame.init()
    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
    clock = pygame.time.Clock()

    world = World()

    l_pos = Vector2(4,5)
    light_source = LightSource(l_pos, 120, [1.5,2.5,3.5,5])

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
            l_pos.y -= ray_spd * delta
        if keys[pygame.K_a]:
            l_pos.x -= ray_spd * delta
        if keys[pygame.K_s]:
            l_pos.y += ray_spd * delta
        if keys[pygame.K_d]:
            l_pos.x += ray_spd * delta
        if keys[pygame.K_RETURN]:
            print(pygame.mouse.get_pos())


        light_source.set_pos(l_pos)
        world.update()
        
        tiles = world.getCurrentChunk().getCurrentRoom().foregroundMap
        light_source.update(tiles)
    

        camera.lerp_to(light_source.pos.x * Tile.tileSize, light_source.pos.y * Tile.tileSize, 0.3)
    
        screen.fill((0,0,0))
        world.render(screen)
        
        light_source.debug_draw(screen)
        light_source.draw(screen)

        pygame.display.flip()
