from os import path
from collections import OrderedDict

class BaseSolver:
    def __init__(self, file_path, out_file=None):
        self.in_file = file_path
        self.out_file = out_file

        self.time_left = None
        self.out_libs = []
        self.out_books = []
        self.signing_time_left = 0
        self.signing = {}
        self.sending = {}
        self.pending = {}
        self.sent_books = set()

        # code for each line as list element
        file = open(file_path, mode='r')
        data = file.read().split('\n')
        file.close()

        # nice code to read a line of ints
        self.B, self.L, self.D = map(int, data.pop(0).split())
        self.time_left = self.D

        # nice code to read a line of ints as list
        self.book_scores = list(map(int, data.pop(0).split()))
        for i in range(self.L):
            n_books, signs, ships = map(int, data.pop(0).split())
            lib = {'n_books': n_books, 'signs': signs, 'ships': ships}

            this_books = list(map(int, data.pop(0).split()))
            # books scores (nice code to index a list based on another)
            this_book_scores = list(map(self.book_scores.__getitem__, this_books))

            # sort books by score (nice code to get the indexes to sort aa list)
            ix_sorted = [i for (v, i) in sorted(((v, i) for (i, v) in enumerate(this_book_scores)), reverse=True)]
            this_books = list(map(this_books.__getitem__, ix_sorted))
            this_book_scores = list(map(this_book_scores.__getitem__, ix_sorted))

            # books and scores ordered by score
            lib.update({'books': this_books, 'book_scores': this_book_scores})

            self.pending.update({i: lib})

        return

    def running_score(self):
        score = sum(map(self.book_scores.__getitem__, self.sent_books))
        return score

    def write_result(self):
        score = self.running_score()
        if self.out_file is None:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(score) + '.txt'
        else:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(score) + '_' + self.out_file + '.txt'
        file = open(path.join('results', self.out_file), 'w+')
        n_libs = len(self.out_libs)
        file.write(f'{n_libs}\n')
        for i in range(n_libs):
            file.write(f'{self.out_libs[i]} {len(self.out_books[i])}\n')
            file.write('{}\n'.format(' '.join([str(x) for x in self.out_books[i]])))
        file.close()

