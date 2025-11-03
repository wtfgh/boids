import tkinter as tk
import random
import numpy as np

class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Boid:
    def __init__(self, size = 10, speed = 10, color = 'white'):
        self.size = size
        self.position = Vector2D(random.randint(0, window_width), random.randint(0, window_height))
        self.shape = canvas.create_oval(self.position.x - size / 2, self.position.y - size / 2,
                                        self.position.x + size / 2, self.position.y + size / 2, fill = color)
        self.boundry_avoidance_strength = 100
        self.speed = speed
        self.velocity = Vector2D(random.random() * self.speed * 2 - self.speed,
                                 random.random() * self.speed * 2 - self.speed)
        self.avoidance_range = 20
        self.awareness_range = 100
        self.boids_in_awareness_range = 0
        self.boids_in_avoidance_range = 0
        self.perceived_flock_center_mass = Vector2D()
        self.perceived_flock_velocity = Vector2D()
        self.avoidance_vector = Vector2D()

    def start_moving(self):
        self.tick()

    def tick(self):
        self.surroundings_check()
        self.calculate_direction()
        self.move_self_and_update_pos()
        root.after(tick_length, self.tick)

    def surroundings_check(self):
        self.boids_in_awareness_range = 0
        self.boids_in_avoidance_range = 0
        self.perceived_flock_center_mass = Vector2D()
        self.perceived_flock_velocity = Vector2D()
        self.avoidance_vector = Vector2D()
        for boid in boids:
            if boid is not self:
                if self.is_distance_small_enough(boid.position.x, boid.position.y, self.awareness_range):
                    self.boids_in_awareness_range += 1
                    self.perceived_flock_center_mass.x += boid.position.x
                    self.perceived_flock_center_mass.y += boid.position.y
                    self.perceived_flock_velocity.x += boid.velocity.x
                    self.perceived_flock_velocity.y += boid.velocity.y
                    if self.is_distance_small_enough(boid.position.x, boid.position.y, self.avoidance_range):
                        self.boids_in_avoidance_range += 1
                        self.avoidance_vector.x -= (boid.position.x - self.position.x) / ticks_per_second
                        self.avoidance_vector.y -= (boid.position.y - self.position.y) / ticks_per_second
        self.perceived_flock_center_mass.x = self.perceived_flock_center_mass.x / (self.boids_in_awareness_range if self.boids_in_awareness_range else 1)
        self.perceived_flock_center_mass.y = self.perceived_flock_center_mass.y / (self.boids_in_awareness_range if self.boids_in_awareness_range else 1)
        self.perceived_flock_velocity.x = self.perceived_flock_velocity.x / (self.boids_in_awareness_range if self.boids_in_awareness_range else 1)
        self.perceived_flock_velocity.y = self.perceived_flock_velocity.y / (self.boids_in_awareness_range if self.boids_in_awareness_range else 1)


    def calculate_direction(self):
        cohesion_vector = self.calculate_cohesion_vector()
        separation_vector = self.calculate_avoidance_vector()
        alignment_vector = self.calculate_alignment_vector()
        boundry_avoidance_vector = self.calculate_boundry_avoidance_vector()

        self.velocity.x += cohesion_vector.x + separation_vector.x + alignment_vector.x + boundry_avoidance_vector.x
        self.velocity.y += cohesion_vector.y + separation_vector.y + alignment_vector.y + boundry_avoidance_vector.y

    def calculate_cohesion_vector(self):
        return (Vector2D((self.perceived_flock_center_mass.x - self.position.x) / 40 / ticks_per_second * cohesion_slider.get() / 100,
                        (self.perceived_flock_center_mass.y - self.position.y) / 40 / ticks_per_second * cohesion_slider.get() / 100)
            if use_cohesion.get() else Vector2D())

    def calculate_avoidance_vector(self):
        return Vector2D(self.avoidance_vector.x * avoidance_slider.get() / 100, self.avoidance_vector.y * avoidance_slider.get() / 100)\
            if use_avoidance.get() else Vector2D()

    def calculate_alignment_vector(self):
        return (Vector2D((self.perceived_flock_velocity.x - self.velocity.x) / ticks_per_second * 5 * alignment_slider.get() / 100,
                        (self.perceived_flock_velocity.y - self.velocity.y) / ticks_per_second * 5 * alignment_slider.get() / 100)
            if use_alignment.get() else Vector2D())

    def calculate_boundry_avoidance_vector(self):
        vector = Vector2D()
        if self.position.x >= window_width - 50:
            vector.x = -self.boundry_avoidance_strength / ticks_per_second
        elif self.position.x <= 50:
            vector.x = self.boundry_avoidance_strength / ticks_per_second
        elif self.position.y >= window_height - 50:
            vector.y = -self.boundry_avoidance_strength / ticks_per_second
        elif self.position.y <= 50:
            vector.y = self.boundry_avoidance_strength / ticks_per_second
        return vector

    def move_self_and_update_pos(self):
        self.velocity.x = np.clip(self.velocity.x, -self.speed, self.speed)
        self.velocity.y = np.clip(self.velocity.y, -self.speed, self.speed)

        canvas.move(self.shape, self.velocity.x, self.velocity.y)

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def is_distance_small_enough(self, x, y, distance):
        return abs(x - self.position.x) < distance and abs(y - self.position.y) < distance

ticks_per_second = 30
tick_length = 1000 // ticks_per_second

window_width = 800

window_height = 600
root = tk.Tk()

canvas = tk.Canvas(root, width = window_width, height = window_height, background = 'black')
canvas.grid(row = 1, column = 2, rowspan = 50)

use_cohesion = tk.BooleanVar(value = True)
use_cohesion_chkbx = tk.Checkbutton(root, text = 'Сплоченность', variable = use_cohesion)
use_cohesion_chkbx.grid(row = 1, column = 1)

cohesion_slider = tk.Scale(root, from_ = 0, to = 100, orient = 'horizontal', length = 100)
cohesion_slider.grid(row = 2, column = 1)
cohesion_slider.set(100)

use_avoidance = tk.BooleanVar(value = True)
use_avoidance_chkbx = tk.Checkbutton(root, text = 'Избежание\n соседей', variable = use_avoidance)
use_avoidance_chkbx.grid(row = 3, column = 1)

avoidance_slider = tk.Scale(root, from_ = 0, to = 100, orient = 'horizontal', length = 100)
avoidance_slider.grid(row = 4, column = 1)
avoidance_slider.set(100)

use_alignment = tk.BooleanVar(value = True)
use_alignment_chkbx = tk.Checkbutton(root, text = 'Выравнивание\n направления\n и скорости', variable = use_alignment)
use_alignment_chkbx.grid(row = 5, column = 1)

alignment_slider = tk.Scale(root, from_ = 0, to = 100, orient = 'horizontal', length = 100)
alignment_slider.grid(row = 6, column = 1)
alignment_slider.set(100)

number_of_boids = 150

boids = [Boid() for i in range(number_of_boids)]

for boid in boids:
    boid.start_moving()

root.mainloop()
