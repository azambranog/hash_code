from argparse import ArgumentParser as AP
import random
from numpy.random import choice


from BaseSolver import BaseSolver


class Solver(BaseSolver):
    def solve(self, max_iter=1000):
        iter=0
        project_value = {p: (self.p_sco[p]/self.p_day[p]) for p in self.p_day}
        self.PROJECTS = []

        while (len(project_value) != 0) and (iter<=max_iter):
            p = random.choices(list(project_value), weights=list(project_value.values()))[0]
            roles = self.p_rol[p]
            my_indexes = list(range(len(roles)))
            random.shuffle(my_indexes)
            for rol in my_indexes:
                s = roles[rol][0]
                l = roles[rol][1]
                candidates = list(filter(lambda c: c[1] >= l, self.s[s]))
                if len(candidates) == 0:
                    break
                cn, cl = random.choice(candidates)
                roles[rol][2] = cn

            if len(list(filter(lambda c: c[2] == '', roles))) == 0:
                self.p_rol[p] = roles
                self.refresh_skills()
                project_value.pop(p)
                self.PROJECTS.append(p)

            iter = iter + 1
        print(self.PROJECTS)


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
