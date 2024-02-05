import math


class Calculations:

    # inputs angle of attack in degrees, speed
    # outputs x, y vector components
    @staticmethod
    def velocity_vectors_from_angle_of_attack(angle, speed):
        angle = math.radians(angle)
        return speed*math.cos(angle), speed*math.sin(angle)


print(Calculations.velocity_vectors_from_angle_of_attack(0, 1))
