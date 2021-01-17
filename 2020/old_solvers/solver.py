from itertools import accumulate
import random
from os import  path


class Solver:
    def __init__(self, file_path, out_file=None):
        self.in_file = file_path
        self.out_file = out_file

        self.time_left = None
        self.out_libs = []
        self.out_books = []
        self.signing_time_left = 0
        self.signing = 0
        self.empty_libs = []
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
        self.libs = []
        for i in range(self.L):
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

            self.libs.append(lib)
        return

    def update_future_steps(self):

        for lib in self.libs:
            # nice code to group lists into smaller ones
            n = lib['ships']  # size of smaller group
            step_books = [lib['books'][i:i + n] for i in range(0, len(lib['books']), n)]
            step_score = [lib['book_scores'][i:i + n] for i in range(0, len(lib['book_scores']), n)]
            step_score = [sum(s) for s in step_score]

            # code for cumulative sum
            acc_step_score = list(accumulate(step_score))
            lib.update({'step_books': step_books, 'step_score': step_score, 'acc_step_score': acc_step_score})

    def find_promising_lib(self):

        available_libs = list(set(range(len(self.libs))) - set(self.out_libs))
        if len(available_libs) == 0:
            return None

        self.update_future_steps()

        days_left = self.time_left
        scores = []
        signs = []

        for lib in available_libs:
            last_possible = days_left - self.libs[lib]['ships'] - 1
            if last_possible < 0 or len(self.libs[lib]['acc_step_score']) == 0:
                scores.append(-1)
                signs.append(self.D)
                continue
            ix = min(last_possible, len(self.libs[lib]['acc_step_score']) - 1)
            scores.append(self.libs[lib]['acc_step_score'][ix])
            signs.append(self.libs[lib]['sign'])


        # code to find indices of the maximum
        i_max = [i for i, j in enumerate(scores) if j == max(scores)]
        # If several have maximum value we go for the one that signs faster
        # if several sign fast, do random
        # TODO improve this strategy
        signs = list(map(signs.__getitem__, i_max))
        i_min = random.choice([i for i, j in enumerate(signs) if j == min(signs)])

        return available_libs[i_max[i_min]]

    def remove_books(self, book_list):
        for lib in self.libs:
            for b in book_list:
                try:
                    ix = lib['books'].index(b)
                    lib['books'].pop(ix)
                    lib['book_scores'].pop(ix)
                except ValueError:
                    next

        self.update_future_steps()

    def solve(self, checkpoint=None):
        if checkpoint is None:
            checkpoint = int(self.D / 10) + 1

        all_libs_taken = False
        while self.time_left > 0:
            if self.signing_time_left == 0 and not all_libs_taken:
                curr_lib = self.find_promising_lib()
                self.signing = curr_lib
                if curr_lib is None:
                    all_libs_taken = True
                else:
                    self.signing_time_left = self.libs[curr_lib]['sign']
                    self.out_libs.append(curr_lib)
                    self.out_books.append([])

            # send books
            sending_libs = set(self.out_libs) - {self.signing}
            sending_libs = list(sending_libs - set(self.empty_libs))
            random.shuffle(sending_libs)

            for sending_lib in sending_libs:
                try:
                    x = self.libs[sending_lib]['step_books'].pop(0)
                    sending_lib_index = self.out_libs.index(sending_lib)
                    self.out_books[sending_lib_index] += x
                    self.sent_books = self.sent_books.union(set(x))
                    self.remove_books(x)
                except IndexError:
                    self.empty_libs.append(sending_lib)

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

        file = open(path.join('results', 'solver1', self.out_file), 'w+')
        file.write(f'Score = {score}')
        file.write(f'Out_libs = {self.out_libs}')
        file.write(f'Out_books = {self.out_books}')
        file.close()


if __name__ == '__main__':
    sol = Solver('../data/a_example.txt')
    sol.solve()



