from solver2 import Solver
from multiprocessing import Process


def run_in_parallel(*fns):
    proc = []
    for fn, ar in fns:
        p = Process(target=fn, args=[ar])
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def f(in_file):
    s = Solver(in_file)
    s.solve()


if __name__ == '__main__':
    run_in_parallel((f, 'data/a_example.txt'), (f, 'data/b_read_on.txt'),
                    (f, 'data/c_incunabula.txt'), (f, 'data/e_so_many_books.txt'),
                    (f, 'data/f_libraries_of_the_world.txt'))
