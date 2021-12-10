# class to define sensor functions for the routers mounted on the rover

import random
import math

class rover_sensors:
    overheating_rate = 0.5  # 0.5 degree / seconds when doing task
    decreasing_rate = 5  # 5 degree / seconds when sleeping
    # status = 1  # Activate:1, Sleep:0, Leader:3
    # temperature = 40
    rover_speed = 10

    def __init__(self):
        #rover temparature in deg celcius
        self.temp = random.randint(15,40)

    def do_rover_task(self,task,location_x,location_y,temperature,status):
        # global rover_speed, location_x, location_y, temperature, overheating_rate, status

        if task['type'] == 'move+collect':
            target_x = task['task_location_x']
            target_y = task['task_location_y']

            # Finding distance to dest location + time taken to get there.
            dist_x = target_x - location_x
            dist_y = target_y - location_y
            total_dist = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2))
            task_require_time = total_dist / self.rover_speed

            # Increasing temp of rover as it moves, include after sensor data if that counts in task_require_time.
            temperature = temperature + self.overheating_rate * task_require_time
            if temperature > 90:  # Overheat threshold.
                temperature = 91
                status = 0

        return target_x,target_y,temperature,status,task_require_time

    def air_temp_sensor(self):
        #mars air temperature range 220K-300K
        return random.randint(220,300)

    def pressure_sensor(self):
        # mars air temperature range 600pa-750pa
        return random.randint(600,750)


    def thermal_infra_sensor(self):
        return random.uniform(10.0,20.0)

    def wind_sensor(self):
        #wind speed km per hour
        return random.uniform(2.0,10.0)

    def radiation_dust_sensor(self):
        return random.uniform(10.0,20.0)

    def humidity_sensor(self):
        return random.uniform(80.0,100.0)

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
