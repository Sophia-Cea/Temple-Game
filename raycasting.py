from ast import Lambda
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
    def __init__(self, pos: Vector2, num_rays: int, start_angle=0, end_angle=360) -> None:
        # TODO replace radii with radius
        # TODO replace self.color with self.image
        self.pos = pos
        self.num_rays = num_rays
        self.rays: list[Ray] = []
        self.angles = [utils.deg2rad(start_angle), utils.deg2rad(end_angle)]
        self.surface = self.init_surface()
        self.init_rays()
        
    def init_rays(self):
        inc_angle = (self.angles[1] - self.angles[0]) / self.num_rays
        for i in range(self.num_rays):
            angle = self.angles[0] + (i * inc_angle)
            d = Vector2(math.cos(angle), math.sin(angle))
            self.rays.append(Ray(self.pos, d))

    def init_surface(self):
        return init_default_light_surface()

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
        p, pr = light_source._get_lighting_polygon()
        light_source._translate_polygon(p, pr.topleft)
        surf, mask_surf = draw_polygon_with_image(p, pr, light_source.surface, self.pos)
        screen.blit(mask_surf, camera.project(pr), pygame.BLEND_MULT)

    def _translate_polygon(self, polygon: list[Vector2], top_left: tuple[int, int]):
        for vertice in polygon:
            vertice.x -= top_left[0]
            vertice.y -= top_left[1]

    def _draw_polygon(self, polygon: list[Vector2], rect:Rect):
        self.poly_surf, self.mask_surf = draw_polygon_with_image(polygon, rect, self.surface)
        return self.poly_surf

    def _get_lighting_polygon(self):
        vertices: list[Vector2] = []
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        # collect polygon vertices (scale to pixels) (world position)
        for ray in self.rays:
            pt = ray.get_pt_at_radius(10) * Tile.tileSize
            if max_x is None:
                max_x = pt.x
                max_y = pt.y
                min_x = pt.x
                min_y = pt.y
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

def get_lighting_surfaces() -> tuple[Surface]:
    surf = pygame.Surface((utils.WIDTH, utils.HEIGHT))
    surf.set_colorkey((0,0,0))
    surf.fill((0,0,0))
    temp_surf = pygame.Surface((utils.WIDTH, utils.HEIGHT))
    temp_surf.set_colorkey((0,0,0))
    temp_surf.fill((0,0,0))
    return (surf, temp_surf)

def init_light_surface(num_layers, draw_layer, before_draw=None):
    surf, temp_surf = get_lighting_surfaces()
    center = (utils.WIDTH/2, utils.HEIGHT/2)
    if before_draw != None:
        before_draw(surf)

    for i in range(num_layers):
        draw_layer(temp_surf, i, center)
        surf.blit(temp_surf, (0,0), special_flags=pygame.BLEND_ADD)

    return surf

def init_fancy_light_surface():
    num_layers = 50
    max_radius = utils.HEIGHT/4
    color = [255/num_layers]*3

    t_initial = -5
    t_final = 1
    t_inc = (t_final - t_initial) / num_layers

    def draw_layer(surface, index, pos):
        t = t_initial + (t_inc * index)
        sigmoid = 1/(1+math.exp(-t))
        radius = sigmoid * max_radius
        pygame.draw.circle(surface, color, pos, radius)
        for i in range(50):
            ti = 2 * index / num_layers
            theta = (i + ti) * (183 * math.pi) / (index + 10)
            x = pos[0] + math.cos(theta)*radius
            y = pos[1] + math.sin(theta)*radius
            pygame.draw.circle(surface, color, (x,y), 10)

    return init_light_surface(num_layers, draw_layer)

# USAGE: 
# To create a new light surface, you must provide the number of layers to draw, and a draw_layer function to init_light_surface
# For each layer, init_light_surface will call draw_layer with arguments surface, index, and pos. Surface is the surface to be drawn on,
# index is the current layer index, and pos is the center of the 
# each layer will then be blended together into a final product
# example usage below 
def init_default_light_surface():
    num_layers = 50
    max_radius = utils.WIDTH/8
    max_brightness = 150
    color = [max_brightness/num_layers]*3
    
    def draw_layer(surface, index, pos):
        radius = (max_radius / num_layers) * index # change how this is defined to change how evenly spaced the layers are (could replace with cos/sin to make it more natural)
        pygame.draw.circle(surface, color, pos, radius)
    
    def before_draw(surface):
        # creates ambient light
        surface.fill((10,10,10))

    return init_light_surface(num_layers, draw_layer, before_draw)


def draw_polygon_with_image(polygon: list[Vector2], poly_rect: Rect, image: Surface, center: tuple):
    mask_surf = Surface(poly_rect.size)
    # expects polygon to be translated already
    pygame.draw.polygon(mask_surf, (255,255,255), polygon)

    surf = Surface(poly_rect.size)
    r = image.get_rect()
    r.center = center
    
    surf.blit(image, r)
    surf.blit(mask_surf, (0,0), special_flags=pygame.BLEND_RGB_MULT)
    pygame.draw.rect(surf, (255,0,0), surf.get_rect(), 2)
    return surf, mask_surf

if __name__ == "__main__":
    from utils import camera
    pygame.init()
    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
    clock = pygame.time.Clock()

    world = World()

    l_pos = Vector2(3.3,3.4)
    light_source = LightSource(l_pos, 120)

    ticks = 0
    running_time = 0

    temp_img =  pygame.transform.scale(pygame.image.load("assets/tiles/tile_15.png"), (400,400))
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
            print(light_source.pos)


        light_source.set_pos(l_pos)
        world.update()
        
        tiles = world.getCurrentChunk().getCurrentRoom().foregroundMap
        light_source.update(tiles)
    

        camera.lerp_to(light_source.pos.x * Tile.tileSize, light_source.pos.y * Tile.tileSize, 0.3)
    
        screen.fill((0,0,0))

        world.render(screen)

        p, pr = light_source._get_lighting_polygon()
        light_source._translate_polygon(p, pr.topleft)
        center = (light_source.pos * Tile.tileSize) - Vector2(pr.topleft)
        surf, mask_surf = draw_polygon_with_image(p, pr, light_source.surface, center)
        # mask_surf = pygame.transform.scale(mask_surf, (utils.WIDTH, utils.HEIGHT))
        # light_source.debug_draw(screen)
        # screen.blit(light_source.surface, (0,0))
        screen.blit(surf, camera.project(pr))
   
        pygame.display.flip()
