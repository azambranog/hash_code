from os import path
from time import time
import numpy as np



class BaseSolver:
    def __init__(self, file_path, out_file=None):
        self.in_file = file_path
        self.out_file = out_file

        file = open(file_path, mode='r')
        data = file.read().split('\n')
        file.close()

        self.D, self.I, self.S, self.V, self.F = map(int, data.pop(0).split())
        self.time_left = self.D

        self.streets = {}
        self.intersections = {i: {'in': [], 'out': []} for i in range(self.I)}
        self.lights = {i: {'streets': [], 'durations': []} for i in range(self.I)}
        for i in range(self.S):
            st = data.pop(0).split()
            s = int(st[0])
            e = int(st[1])
            st_name = st[2]
            self.streets.update({st_name: {'s': s, 'e': e, 'L': int(st[3])}})
            self.streets.update({st_name: {'s': s, 'e': e, 'L': int(st[3])}})
            self.intersections[s]['out'].append(st_name)
            self.intersections[e]['in'].append(st_name)

        self.cars = {}
        self.transited_inter = {i: [] for i in self.intersections}
        self.transited_str = {i: [] for i in self.streets}
        for i in range(self.V):
            car = data.pop(0).split()
            car_route = car[1:]
            STS = list(map(self.streets.__getitem__, car_route))
            L = [x['L'] for x in STS][1:]
            LCUM= [0] + list(np.cumsum(L))
            INTS = [x['e'] for x in STS]
            self.cars.update({i: {'L': L, 'route': car_route, 'intersections': INTS, 'Lcum': LCUM}})
            [self.transited_inter[inter].append(i) for inter in INTS]
            [self.transited_str[st].append(i) for st in car_route]

        self.transited_inter = {k:v for k,v in self.transited_inter.items() if len(v) > 0}
        self.transited_str = {k: v for k, v in self.transited_str.items() if len(v) > 0}

        #print('####streets')
        #print(self.streets)
        #print('####intersections')
        #print(self.intersections)
        #print('####cars')
        #print(self.cars)
        #print('####lights')
        #print(self.lights)
        #print('####transited_inter')
        #print(self.transited_inter)
        #print('####transited_str')
        #print(self.transited_str)

    def write_result(self):
        if self.out_file is None:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(int(time())) + '.txt'
        else:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(int(time())) + '_' + self.out_file + '.txt'

        lights = {k: v for k, v in self.lights.items() if len(v['streets']) > 0}
        file = open(path.join('results', self.out_file), 'w+')

        file.write(f'{len(lights)}\n')
        for l in lights:
            file.write(f'{l}\n')
            n_streets = len(lights[l]["streets"])
            file.write(f'{n_streets}\n')
            for i in range(n_streets):
                file.write(f'{lights[l]["streets"][i]} {lights[l]["durations"][i]}\n')
        file.close()
