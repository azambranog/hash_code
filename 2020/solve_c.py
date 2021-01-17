from base_solver import BaseSolver
import random

class Solver(BaseSolver):
    # all libs can send all their books in one go
    # i select the lib with a best score/ship ratio
    def solve(self, checkpoint=None):
        if checkpoint is None:
            checkpoint = int(self.D / 20) + 1

        self.signing = None
        while self.time_left > 0:

            if self.signing_time_left == 0:
                if self.signing is None:
                    self.signing = self.get_best_lib()
                    self.signing_time_left = self.pending[self.signing]['signs']
                else:
                    books_to_send = self.pending[self.signing]['books']
                    self.out_libs.append(self.signing)
                    self.out_books.append(books_to_send)
                    self.pending.pop(self.signing)

                    self.remove_books(books_to_send)

                    if len(self.pending) != 0:
                        self.signing = self.get_best_lib()
                        self.signing_time_left = self.pending[self.signing]['signs']
                    else:
                        self.signing_time_left = -1

            self.time_left -= 1
            self.signing_time_left -= 1

            if self.time_left % checkpoint == 0 or self.time_left == 0:
                print(f'({self.in_file}).. Time Left = {self.time_left}.. Score = {self.running_score()}')

    def get_best_lib(self):
        #libs with best scre/ship ratio. If many are same then get the quickest
        ppd = {k: sum(v['book_scores']) / v['signs'] for k, v in self.pending.items()}
        maxval = max(ppd.values())
        bestlibs = [k for k, v in ppd.items() if v == maxval]

        ships = {k: self.pending[k]['ships'] for k in bestlibs}
        minship = min(ships.values())
        bestlibs = [k for k, v in ships.items() if v == minship]

        return random.choice(bestlibs)

    def remove_books(self, books):
        empty_libs=[]
        for b in books:
            for i, l in self.pending.items():
                try:
                    ix = l['books'].index(b)
                    l['books'].pop(ix)
                    l['book_scores'].pop(ix)
                    if len(l['books']) == 0:
                        empty_libs.append(i)
                except:
                    pass

        for i in empty_libs:
            self.pending.pop(i)

    def running_score(self):
        #code to unlist stuf
        x = [item for sublist in self.out_books for item in sublist]
        self.sent_books = set(x)
        return super().running_score()


if __name__ == '__main__':

    s = Solver('data/c_incunabula.txt')
    s.solve()
    s.write_result()

