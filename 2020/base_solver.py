from os import path


class BaseSolver:
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

    def score(self):
        score = sum(map(self.books.__getitem__, self.sent_books))
        return score

    def write_result(self):
        score = self.score()
        if self.out_file is None:
            self.out_file = path.basename(self.in_file)[0] + '_' + str(score) + '.txt'

        file = open(path.join('old_solvers/results', 'solver1', self.out_file), 'w+')
        file.write(f'Score = {score}')
        file.write(f'Out_libs = {self.out_libs}')
        file.write(f'Out_books = {self.out_books}')
        file.close()