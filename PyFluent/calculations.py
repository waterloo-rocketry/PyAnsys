import math


# inputs angle of attack in degrees, speed
# outputs x, y vector components
def velocity_vectors_from_angle_of_attack(angle, speed):
    angle = math.radians(angle)
    return speed*math.cos(angle), speed*math.sin(angle)


# calculates pressure, air density, temp, and air viscosity at
# a given altitude
# For Ansys sims we only care about density and viscosity
# Also for our purposes we don't need to worry about temperature increments
def calculate_atmospheric_properties(altitude, temperature_increment=0):
    # U.S. Standard Atmosphere 1976 calculations
    if altitude <= 11000:  # Troposphere
        temperature = 288.15 - 0.00649 * altitude + temperature_increment
        pressure = 101325 * (1 - 0.00649 * altitude / 288.15) ** 5.2561
    elif altitude <= 25000:  # Stratosphere
        temperature = 216.65 + temperature_increment
        pressure = 22632.06 * 2.71828 ** (-0.000157 * (altitude - 11000))
    else:  # Mesosphere
        temperature = 273.15 - 0.0028 * altitude
        pressure = 5474.89 * (1 - 0.0028 * altitude / 273.15) ** 5.2561

    density = pressure / (287.05 * temperature)
    dynamic_viscosity = 1.458e-6 * (temperature ** 1.5) / (temperature + 110.4)

    # Convert units
    pressure /= 1000  # Convert Pa to kPa

    return pressure, density, temperature, dynamic_viscosity
