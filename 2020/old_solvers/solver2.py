from itertools import accumulate
import random
from os import path


class Solver:
    def __init__(self, file_path, out_file=None):
        self.in_file = file_path
        self.out_file = out_file

        self.time_left = None
        self.out_libs = []
        self.out_books = []
        self.signing = {}
        self.signing_time_left = 0
        self.sending = {}
        self.sent_books = set()

        # code for each line as list element
        file = open(file_path, mode='r')
        data = file.read().split('\n')
        file.close()

        # nice code to read a line of ints
        self.B, self.L, self.D = map(int, data.pop(0).split())
        self.time_left = self.D
        # nice code to read a line of ints as list
        self.books = list(map(int, data.pop(0).split()))
        self.libs = {}
        for ii in range(self.L):
            n_books, sign, ships = map(int, data.pop(0).split())
            lib = {'n_books': n_books, 'sign': sign, 'ships': ships}

            books = list(map(int, data.pop(0).split()))
            # books scores (nice code to index a list based on another)
            book_scores = list(map(self.books.__getitem__, books))

            # sort books by score (nice code to get the indexes to sort an array)
            ix_sorted = [i for (v, i) in sorted(((v, i) for (i, v) in enumerate(book_scores)), reverse=True)]
            books = list(map(books.__getitem__, ix_sorted))
            book_scores = list(map(book_scores.__getitem__, ix_sorted))

            lib.update({'books': books, 'book_scores': book_scores})

            self.libs.update({ii: lib})
        return

    def update_future_steps(self):
        def helper(lib):
            # nice code to group lists into smaller ones
            n = lib['ships']  # size of smaller group
            step_books = [lib['books'][i:i + n] for i in range(0, len(lib['books']), n)]
            step_score = [lib['book_scores'][i:i + n] for i in range(0, len(lib['book_scores']), n)]
            step_score = [sum(s) for s in step_score]

            # code for cumulative sum
            acc_step_score = list(accumulate(step_score))
            lib.update({'step_books': step_books, 'step_score': step_score, 'acc_step_score': acc_step_score})

        for lib in self.libs.values():
            helper(lib)
        for lib in self.sending.values():
            helper(lib)
        for lib in self.signing.values():
            helper(lib)

    def find_promising_lib(self):

        if len(self.libs) == 0:
            return None

        self.update_future_steps()

        days_left = self.time_left
        scores = {}
        signs = {}

        for i, lib in self.libs.items():
            last_possible = days_left - lib['sign'] - 1
            if last_possible < 0 or len(lib['acc_step_score']) == 0:
                continue
            ix = min(last_possible, len(lib['acc_step_score']) - 1)
            scores.update({i: lib['acc_step_score'][ix]})
            signs.update({i: lib['sign']})

        # code to find indices of the maximum
        best_libs = [i for i, j in scores.items() if j == max(scores.values())]
        # If several have maximum value we go for the one that signs faster
        # if several sign fast, do random
        # TODO improve this strategy
        fastest_signs = [k for k in signs if k in best_libs]
        result = random.choice(fastest_signs)
        return result

    def remove_books(self, book_list):

        def _helper(lib, book_list):
            for b in book_list:
                try:
                    ix = lib['books'].index(b)
                    lib['books'].pop(ix)
                    lib['book_scores'].pop(ix)
                except ValueError:
                    next

        for lib in self.libs.values():
            _helper(lib, book_list)
        for lib in self.sending.values():
            _helper(lib, book_list)
        for lib in self.signing.values():
            _helper(lib, book_list)

        self.update_future_steps()

    def remove_libs_with_no_chance(self):
        to_pop = []
        for i, lib in self.libs.items():
            if lib['sign'] >= self.time_left:
                to_pop.append(i)

        [self.libs.pop(x) for x in to_pop]

    def solve(self, checkpoint=None):
        if checkpoint is None:
            checkpoint = int(self.D / 10) + 1

        while self.time_left > 0:

            sending_libs = list(self.sending.keys())
            random.shuffle(sending_libs)

            for sending_lib in sending_libs:
                if len(self.sending[sending_lib]['step_books']) > 0:
                    x = self.sending[sending_lib]['step_books'].pop(0)
                    sending_lib_index = self.out_libs.index(sending_lib)
                    self.out_books[sending_lib_index] += x
                    self.sent_books = self.sent_books.union(set(x))
                    self.remove_books(x)
                    #in case the lib is empty after sendinf this batch
                    if len(self.sending[sending_lib]['step_books']) == 0:
                        self.sending.pop(sending_lib)
                else:
                    #can happen that a lib is empty after doing the remove list operation
                    self.sending.pop(sending_lib)


            # shall we sign a library?
            if self.signing_time_left == 0:
                # make signing lib part of sending libs
                self.sending.update(self.signing)
                self.signing = {}
                self.remove_libs_with_no_chance()
                if not len(self.libs) == 0:
                    #get another lib
                    lx = self.find_promising_lib()
                    self.signing = {lx: self.libs.pop(lx)}
                    self.signing_time_left = self.signing[lx]['sign']
                    self.out_libs.append(lx)
                    self.out_books.append([])

            self.time_left -= 1
            self.signing_time_left -= 1

            if self.time_left % checkpoint == 0 or self.time_left == 0:
                print(f'({self.in_file}).. Time Left = {self.time_left}.. Score = {self.score()}')

        self.write_result()
        return self.score()

    def score(self):
        score = sum(map(self.books.__getitem__, self.sent_books))
        return score

    def print(self):
        for i in dir(self):
            if (i[0] != '_') and (i != 'print'):
                print(f'{i} = {getattr(self, i)}')

    def print_res(self):
        print(self.out_libs)
        print(self.out_books)

    def write_result(self):
        score = self.score()
        if self.out_file is None:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(score) + '.txt'

        file = open(path.join('results', 'solver2', self.out_file), 'w+')
        file.write(f'Score = {score}\n')
        file.write(f'Out_libs = {self.out_libs}\n')
        file.write(f'Out_books = {self.out_books}\n')
        file.close()


if __name__ == '__main__':
    sol = Solver('../data/a_example.txt')
    sol.solve()



