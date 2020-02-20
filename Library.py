class Library :
    def __init__(self,id,books,sign_time,scan_books):
        self.id=int(id)
        self.books=books
        self.sign_time=int(sign_time)
        self.scan_books=int(scan_books)
    def scoresOfSignTime(self):
        self.books.sort(key=lambda x: x.score,reverse=True)
        return sum(map(lambda x: x.score,self.books[:self.scan_books]))
    def get_best_books(self):
        self.books.sort(key=lambda x: x.score,reverse=True)
        return self.books