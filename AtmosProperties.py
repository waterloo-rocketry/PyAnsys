import tkinter as tk
from tkinter import ttk, scrolledtext

class AtmoProperties:
    def __init__(self, altitude, temperature_increment):
        self.altitude = altitude
        self.temperature_increment = temperature_increment

    @staticmethod
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


class AtmoPropertiesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Atmospheric Properties Calculator")

        self.altitude_label = ttk.Label(master, text="Altitude (m):")
        self.altitude_entry = ttk.Entry(master)
        self.altitude_label.grid(row=0, column=0, padx=10, pady=10)
        self.altitude_entry.grid(row=0, column=1, padx=10, pady=10)

        self.temp_increment_label = ttk.Label(master, text="Temperature Increment (K):")
        self.temp_increment_entry = ttk.Entry(master)
        self.temp_increment_label.grid(row=1, column=0, padx=10, pady=10)
        self.temp_increment_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_button = ttk.Button(master, text="Calculate", command=self.calculate_atmospheric_properties)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.result_text.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_atmospheric_properties(self):
        try:
            altitude = float(self.altitude_entry.get())
            temp_increment = float(self.temp_increment_entry.get())
            result = AtmoProperties.calculate_atmospheric_properties(altitude, temp_increment)
            result_str = (f"Pressure: {result[0]:.2f} kPa\nDensity: {result[1]:.5f} kg/m^3\n"
                          f"Temperature: {result[2]:.2f} K\nDynamic Viscosity: {result[3]:.7e} kg/(m·s)")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_str)
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AtmoPropertiesGUI(root)
    root.mainloop()