from base_solver import BaseSolver

class Solver(BaseSolver):
    # all libs have different books, all send one book, all have same amount of books
    def solve(self, checkpoint= None):
        if checkpoint is None:
            checkpoint = int(self.D / 20) + 1

        # order libs by speed
        signs = {k: v['signs'] for k, v in self.pending.items()}
        ix_sorted = [i for (v, i) in sorted(((v, i) for (i, v) in enumerate(signs.values())), reverse=False)]
        lib_order = list(map(list(signs.keys()).__getitem__, ix_sorted))

        # could theoretically just fill the file with all the books to save time.
        # But I don't have a file scorer yet so go the slow route
        self.signing = None
        while self.time_left > 0:
            if self.signing_time_left == 0:
                if self.signing is not None:
                    self.out_libs.append(self.signing)
                    self.out_books.append([])
                if len(signs) != 0:
                    self.signing = lib_order.pop(0)
                    self.signing_time_left = signs.pop(self.signing)
                else:
                    self.signing = None

            for i, lib in enumerate(self.out_libs):
                for b in range(self.pending[lib]['ships']):
                    try:
                        self.out_books[i].append(self.pending[lib]['books'].pop(0))
                    except:
                        break
            self.time_left -= 1
            self.signing_time_left -= 1

            if self.time_left % checkpoint == 0 or self.time_left == 0:
                print(f'({self.in_file}).. Time Left = {self.time_left}.. Score = {self.running_score()}')

        pass

    def running_score(self):
        #code to unlist stuf
        x = [item for sublist in self.out_books for item in sublist]
        self.sent_books = set(x)
        return super().running_score()

if __name__ == '__main__':

    s = Solver('data/b_read_on.txt')
    s.solve()
    s.write_result()

