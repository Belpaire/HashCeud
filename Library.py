def mySorter(inputBook,already_read):
    if inputBook.id in already_read:
        return 0
    else:
        return inputBook.score

class Library :
    def __init__(self,id,books,sign_time,scan_books):
        self.id=int(id)
        self.books=books
        self.sign_time=int(sign_time)
        self.scan_books=int(scan_books)
    def scoresOfSignTime(self,already_read):       
        self.books.sort(key=lambda x: mySorter(x,already_read) ,reverse=True)
        return sum(map(lambda x: x.score,self.books[:self.scan_books]))
    def get_best_books(self,already_read):
        self.books.sort(key=lambda x: mySorter(x,already_read),reverse=True)
        return self.books[:self.scan_books]

