import tkinter as tk
import random
import math
import numpy as np

def average_vector(*vectors):
    return Vector2D(np.mean([vector.x for vector in vectors]),
                    np.mean([vector.y for vector in vectors]))

def distance_between_two_dots(x1, y1, x2, y2):
    return np.sqrt((y2 - y1)**2 + (x2 - x1)**2)

class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Boid:
    def __init__(self, size = 5, speed = 1, steering_speed = 0.2, color = 'white'):
        self.size = size
        self.position = Vector2D(random.randint(0, 500), random.randint(0, 500))
        self.shape = canvas.create_oval(self.position.x - size / 2, self.position.y - size / 2,
                                        self.position.x + size / 2, self.position.y + size / 2, fill = color)
        self.movement_vector = Vector2D(random.random() * 2 - 1, random.random() * 2 - 1)
        self.direction = Vector2D()
        self.speed = speed
        self.steering_speed = steering_speed
        self.boids_in_proximity = []
        self.proximity_range = 20

    def collision_check(self):
        if self.position.x > window_width:
            self.movement_vector.x = -self.movement_vector.x
        elif self.position.x < 0:
            self.movement_vector.x = -self.movement_vector.x
        elif self.position.y > window_height:
            self.movement_vector.y = -self.movement_vector.y
        elif self.position.y < 0:
            self.movement_vector.y = -self.movement_vector.y

    def start_moving(self):
        self.initial_surroundings_check()
        self.tick()
        print(self.boids_in_proximity)

    def tick(self):
        self.surroundings_check()
        self.calculate_direction()

        self.movement_vector.x += np.clip(self.steering_speed * np.clip((self.direction.x - self.movement_vector.x), -1, 1),
                                          -self.speed, self.speed)
        self.movement_vector.y += np.clip(self.steering_speed * np.clip((self.direction.y - self.movement_vector.y), -1, 1),
                                          -self.speed, self.speed)

        self.collision_check()
        self.move_self_and_update_pos()
        root.after(tick_length, self.tick)

    def initial_surroundings_check(self):
        for boid in boids:
            if (distance_between_two_dots(self.position.x, self.position.y, boid.position.x, boid.position.y) < self.proximity_range
            and boid is not self):
                self.boids_in_proximity.append(boid)

    def surroundings_check(self):
        for boid in self.boids_in_proximity:
            if (distance_between_two_dots(self.position.x, self.position.y,
                                          boid.position.x, boid.position.y) > self.proximity_range and
                boid is not self):
                self.boids_in_proximity.pop(self.boids_in_proximity.index(boid))
                continue

            for bds in boid.boids_in_proximity:
                if (distance_between_two_dots(self.position.x, self.position.y,
                                              bds.position.x, bds.position.y) < self.proximity_range
                        and bds not in self.boids_in_proximity and boid is not self):
                    self.boids_in_proximity.append(bds)

    def calculate_direction(self):
        vectors_away_from_boids = []
        distances_from_boids = []
        for boid in self.boids_in_proximity:
            angle = math.atan2(self.position.y - boid.position.y,
                               self.position.x - boid.position.x)

            distances_from_boids.append(distance_between_two_dots(self.position.x, self.position.y,
                                                                  boid.position.x, boid.position.y))

            vectors_away_from_boids.append(Vector2D(np.cos(angle), np.sin(angle))),

        separation_multiplier = np.mean(distances_from_boids) / self.proximity_range

        separation_vector = Vector2D(average_vector(*vectors_away_from_boids).x,
                                     average_vector(*vectors_away_from_boids).y)
        print(separation_vector.x, separation_vector.y, len(vectors_away_from_boids))

        alignment_vector = average_vector(*[boid.movement_vector for boid in self.boids_in_proximity])

        print(alignment_vector.x, alignment_vector.y)

        proximity_boid_center_mass = average_vector(*[boid.position for boid in self.boids_in_proximity])

        angle = math.atan2(proximity_boid_center_mass.y - self.position.y,
                           proximity_boid_center_mass.x - self.position.x)

        cohesion_vector = Vector2D(np.cos(angle), np.sin(angle))

        print(cohesion_vector.x, cohesion_vector.y)

        self.direction.x = separation_vector.x + alignment_vector.x + cohesion_vector.x
        self.direction.y = separation_vector.y + alignment_vector.y + cohesion_vector.y
        print(self.direction.x, self.direction.y)
        print(separation_multiplier)
        print()

    def move_self_and_update_pos(self):
        canvas.move(self.shape, self.movement_vector.x, self.movement_vector.y)
        self.position.x += self.movement_vector.x
        self.position.y += self.movement_vector.y

ticks_per_second = 20
tick_length = 1000 // ticks_per_second

window_width = 500
window_height = 500

root = tk.Tk()

canvas = tk.Canvas(root, width = window_width, height = window_height, background = 'black')
canvas.pack()

number_of_boids = 100

boids = [Boid() for i in range(number_of_boids)]
for boid in boids:
    boid.start_moving()

root.mainloop()
