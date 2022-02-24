from os import path
from time import time
import numpy as np


class BaseSolver:
    mapping = {
        'a': "a_an_example.in.txt",
        'b': "b_better_start_small.in.txt",
        'c': "c_collaboration.in.txt",
        'd': "d_dense_schedule.in.txt",
        "e": "e_exceptional_skills.in.txt",
        "f": "f_find_great_mentors.in.txt"
    }

    def __init__(self, problem, out_file=None):
        self.in_file = f"data/{BaseSolver.mapping[problem]}"
        self.out_file = out_file

        file = open(self.in_file, mode='r')
        data = file.read().split('\n')
        file.close()
        self.PROJECTS = []
        self.C, self.P = map(int, data.pop(0).split())
        self.s = set()
        self.c = {}
        for i in range(self.C):
            [name, n_skill] = data.pop(0).split()

            my_skills = {}
            for j in range(int(n_skill)):
                [s, l] = data.pop(0).split()
                self.s.add(s)
                my_skills.update({s: int(l)})
            self.c.update({name: my_skills})

        self.p_sco = {}
        self.p_day = {}
        self.p_best = {}
        self.p_rol = {}
        self.p_lev = {}
        for i in range(self.P):
            [pname, di, si, bi, ri] = data.pop(0).split()
            self.p_sco.update({pname: int(si)})
            self.p_day.update({pname: int(di)})
            self.p_best.update({pname: int(bi)})
            p_roles = []
            for j in range(int(ri)):
                [r, l] = data.pop(0).split()
                p_roles.append([r, int(l), ''])
            self.p_rol.update({pname: p_roles})

        for n in self.c:
            self.c[n].update({k: (0 if k not in self.c[n] else self.c[n][k]) for k in self.s})

        self.refresh_skills()

        if False:
            print('####contri')
            print(self.c)
            print('####skills')
            print(self.s)
            print('####proj roles')
            print(self.p_rol)
            print('####proj days')
            print(self.p_day)
            print('####proj best')
            print(self.p_best)
            print('####proj score')
            print(self.p_sco)

    def refresh_skills(self):
        self.s = {k: [] for k in self.s}
        for n in self.c:
            [self.s[s].append((n, l)) for s, l in self.c[n].items()]
        [self.s[s].sort(key=lambda x: x[1]) for s in self.s]

    def write_result(self):
        if self.out_file is None:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(int(time())) + '.txt'
        else:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(int(time())) + '_' + self.out_file + '.txt'

        file = open(path.join('results', self.out_file), 'w+')

        file.write(f'{len(self.PROJECTS)}\n')
        for p in self.PROJECTS:
            file.write(f'{p}\n')
            ppl = [x[2] for x in self.p_rol[p]]
            file.write(f'{" ".join(ppl)}\n')
        file.close()
