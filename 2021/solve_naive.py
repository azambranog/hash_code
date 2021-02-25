from argparse import ArgumentParser as AP
import random


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
            self.lights[inter]['durations'] = [1 for i in range(len(streets))]

        self.lights = {k:v for k, v in self.lights.items() if len(v['streets']) > 0}


if __name__ == '__main__':
    parser = AP(description='solveproblem')
    parser.add_argument('input_file')
    args = parser.parse_args()

    s = Solver(args.input_file)
    s.solve()
    s.write_result()
