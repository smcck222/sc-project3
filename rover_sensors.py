# class to define sensor functions for the routers mounted on the rover

import random


class rover_sensors:

    def __init__(self):
        #rover temparature in deg celcius
        self.temp = random.randint(15,40)

    def air_temp_sensor(self):
        #mars air temperature range 150K-300K
        return random.randint(150,300)

    def pressure_sensor(self):
        # mars air temperature range 600pa-750pa
        return random.randint(600,750)


    def thermal_infra_sensor(self):
        return random.uniform(10.0,20.0)

    def wind_sensor(self):
        #wind speed miles per hour
        return random.uniform(10.0,70.0)

    def radiation_dust_sensor(self):
        #dummy values for now
        return random.uniform(10.0,20.0)

    def humidity_sensor(self):
        return random.uniform(200.0,300.0)

    def rover_temp(self):
        return self.temp + 5

    def generate_sensor_data(self):
        data = {'air_temp':self.air_temp_sensor(),
                'pressure':self.pressure_sensor(),
                'thermal_infra':self.thermal_infra_sensor(),
                'wind_speed':self.wind_sensor(),
                'radiation_dust':self.radiation_dust_sensor(),
                'humidity':self.humidity_sensor()}
        return data

def main():
    s = rover_sensors()
    sensor_data = s.generate_sensor_data()
    print(sensor_data)

if __name__ == '__main__':
    main()
