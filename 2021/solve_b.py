from argparse import ArgumentParser as AP
import random
import numpy as np



from BaseSolver import BaseSolver


class Solver(BaseSolver):
    def solve(self):
        used_intersections = set([k for k, v in self.transited_inter.items() if len(v) > 0])
        used_streets = set([k for k, v in self.transited_str.items() if len(v) > 0])

        st = []
        tim = []
        for c, v in self.cars.items():
            st = st + v['route']
            tim = tim + v['Lcum']
        av = {s: [] for s in set(st)}
        for i in range(len(tim)):
            av[st[i]] = av[st[i]] + [tim[i]]
        av = {k: v for k,v in av.items() if len(v) > 0}
        av = {k: sum(v)/len(v) for k, v in av.items()}

        #usage = map(self.transited_str.__getitem__, used_streets)
        #n_cars = [len(x) for x in usage]

        for inter in used_intersections:
            streets = set(self.intersections[inter]['in'])
            streets = list(streets.intersection(used_streets))
            random.shuffle(streets)
            self.lights[inter]['streets'] = streets
            d = [1 for i in range(len(streets))]
            self.lights[inter]['durations'] = d

        self.lights = {k:v for k, v in self.lights.items() if len(v['streets']) > 0}

        #print(self.lights)

if __name__ == '__main__':
    parser = AP(description='solveproblem')
    parser.add_argument('input_file')
    args = parser.parse_args()

    s = Solver(args.input_file)
    s.solve()
    s.write_result()
