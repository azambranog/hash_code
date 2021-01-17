from base_solver import BaseSolver
import random

class Solver(BaseSolver):
    # all libs send one book per day and all books have same value, all libs take teh same time
    def solve(self, checkpoint=None):
        if checkpoint is None:
            checkpoint = int(self.D / 1000) + 1

        self.signing = None
        while self.time_left > 0:

            if self.signing_time_left == 0:
                if len(self.pending) != 0:
                    if self.signing is None:
                        best_lib = self.get_best_lib()
                        self.signing = {best_lib: self.pending.pop(best_lib)}
                        self.signing_time_left = self.signing[best_lib]['signs']
                    else:
                        self.sending.update({k: v for k, v in self.signing.items()})
                        self.out_libs.append(list(self.signing)[0])
                        self.out_books.append([])

                        best_lib = self.get_best_lib()
                        self.signing = {best_lib: self.pending.pop(best_lib)}
                        self.signing_time_left = self.signing[best_lib]['signs']


            books_to_remove = []
            for l, lib in self.sending.items():
                ix = self.out_libs.index(l)
                b = lib['books'].pop(0)
                self.out_books[ix].append(b)
                books_to_remove.append(b)
            self.remove_books(books_to_remove, self.pending)
            self.remove_books(books_to_remove, self.sending)

            self.time_left -= 1
            self.signing_time_left -= 1

            if self.time_left % checkpoint == 0 or self.time_left == 0:
                print(f'({self.in_file}).. Time Left = {self.time_left}.. Score = {self.running_score()}')

    def get_best_lib(self):
        #lib that has more books
        morebooks = {k: len(v['books']) for k, v in self.pending.items()}
        maxval = max(morebooks.values())
        bestlibs = [k for k, v in morebooks.items() if v == maxval]

        return random.choice(bestlibs)

    def remove_books(self, books, remove_from):
        empty_libs=[]
        for b in books:
            for i, l in remove_from.items():
                if len(l['books']) == 0:
                    empty_libs.append(i)
                else:
                    try:
                        ix = l['books'].index(b)
                        l['books'].pop(ix)
                        l['book_scores'].pop(ix)
                        if len(l['books']) == 0:
                            empty_libs.append(i)
                    except:
                        pass

        for i in set(empty_libs):
            remove_from.pop(i)


    def running_score(self):
        #code to unlist stuf
        x = [item for sublist in self.out_books for item in sublist]
        self.sent_books = set(x)
        return super().running_score()


if __name__ == '__main__':

    s = Solver('data/d_tough_choices.txt')
    s.solve()
    s.write_result()

