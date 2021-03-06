from argparse import ArgumentParser as AP
import random
import math


from BaseSolver import BaseSolver


class Solver(BaseSolver):
    def solve(self, max_light_duration):

        #number of cars using a street
        n_cars_street = {k:len(v) for k, v in self.transited_str.items() if len(v) > 0}
        # number of cars using an intersection
        n_cars_intert = {k: len(v) for k, v in self.transited_inter.items() if len(v) > 0}

        for inter in n_cars_intert:
            streets = set(self.intersections[inter]['in'])
            streets = list(streets.intersection(set(n_cars_street)))
            random.shuffle(streets)
            self.lights[inter]['streets'] = streets

            ncs = [n_cars_street[s] for s in streets]
            m = max(ncs)
            f = math.ceil
            ncs = [f(max_light_duration*(n/m)) for n in ncs]

            self.lights[inter]['durations'] = ncs

        self.lights = {k:v for k, v in self.lights.items() if len(v['streets']) > 0}

        #print(self.lights)

if __name__ == '__main__':
    parser = AP(description='solveproblem')
    parser.add_argument('-l', dest="max_light_duration", type=float, default=1, help='max duration of a light')
    parser.add_argument('-p', dest="problem", default='a,b,c,d,e,f', help='problem a,b,c,d,e,f')
    args = parser.parse_args()
    probs = args.problem.split(',')

    for p in probs:
        print(f'solving {p}')
        s = Solver(p)
        s.solve(args.max_light_duration)
        s.write_result()
    print('Done')
