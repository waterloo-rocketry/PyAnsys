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


def main():
    print("Atmospheric Properties Calculator")
    print("---------------------------------")

    altitude = float(input("Enter altitude (in meters): "))
    temperature_increment = float(input("Enter temperature increment (in degrees Celsius, 0 for standard): "))

    pressure, density, temperature, dynamic_viscosity = calculate_atmospheric_properties(
        altitude, temperature_increment
    )

    print("\nAtmospheric Properties:")
    print(f"Altitude: {altitude} meters")
    print(f"Pressure: {pressure:.2f} kPa")
    print(f"Density: {density:.2f} kg/m³")
    print(f"Temperature: {temperature:.2f} K")
    print(f"Dynamic Viscosity: {dynamic_viscosity:.9f} kg/(m*s)")


if __name__ == "__main__":
    main()