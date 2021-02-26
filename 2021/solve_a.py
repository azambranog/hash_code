from argparse import ArgumentParser as AP
import random
import numpy as np



from BaseSolver import BaseSolver


class Solver(BaseSolver):
    def solve(self):
        used_intersections = set([k for k, v in self.transited_inter.items() if len(v) > 0])
        used_streets = set([k for k, v in self.transited_str.items() if len(v) > 0])

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
    parser.add_argument('-p', dest="problem", default='a,b,c,d,e,f', help='problem a,b,c,d,e,f')
    args = parser.parse_args()
    probs = args.problem.split(',')

    for p in probs:
        print(f'solving {p}')
        s = Solver(p)
        s.solve()
        s.write_result()
    print('Done')
