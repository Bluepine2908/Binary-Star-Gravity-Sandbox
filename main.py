# Importing modules
import pygame
import math
pygame.init()

# Setting parameters for the display window
width, height = 1000, 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")

white = (253, 251, 212)
yellow = (255, 238, 140)
blue = (162, 191, 254)
red = (255, 116, 108)
grey = (151, 151, 127)
black =(23, 23, 23)

font = pygame.font.SysFont("Cavet", 16)

class Planet:
    au = 149.6e6 * 1000
    G = 6.67428e-11
    scale = 250/au  # 1au = 100 pixels
    timestep = 3600 * 6  # represents 1 day

    # Initialising planetary parameters
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    # Drawing the planets
    def draw(self, win):
        x = self.x * self.scale + width/2
        y = self.y * self.scale + height/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + width / 2
                y = y * self.scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = font.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, white)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/ 2))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    # Calculating distance
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt((distance_x ** 2) + (distance_y ** 2))

        # If other object is sun, will store distance in a property
        if other.sun:
            self.distance_to_sun = distance

        # Calculating force of attraction between the sun and the planet
        force = self.G * self.mass * other.mass / (distance ** 2)
        force_x = force * distance_x / distance
        force_y = force * distance_y / distance 
        return force_x, force_y
    

    # Calculating the forces of the planets with each other
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    
    # Each planet parameters
    star_1 = Planet(-0.8 * Planet.au, 0, 40, yellow, 1.98892e30)
    star_1.sun = True
    star_1.y_vel = 8_000

    star_2 = Planet(0.8 * Planet.au, 0, 40, yellow, 1.98892e30)
    star_2.sun = True
    star_2.y_vel = -8_000

    planet_1 = Planet(-1.5 * Planet.au, 0, 16, blue, 5.9742 * 10**24)
    planet_1.y_vel = 40_000

    planet_2 = Planet(-1.6 * Planet.au, 0, 12, red, 6.39 * 10**23)
    planet_2.y_vel = -42_000

    planet_3 = Planet(1.2 * Planet.au, 0, 8, grey, 0.330 * 10**24)
    planet_3.y_vel = 30_000

    planet_4 = Planet(1.4 * Planet.au, 0, 14, white, 4.8685 * 10**24)
    planet_4.y_vel = -35_000

    planets = [star_1, star_2, planet_1, planet_2, planet_3, planet_4]

    while run:
        clock.tick(60)  
        win.fill(black)

        # Setting the window in a loop till hitting X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(win)
        pygame.display.update()

    pygame.quit()

main()