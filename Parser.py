from Book import Book
from Library import Library
import numpy as np
#Input reader whaddafak

class AllInfo():
    def __init__(self,libs,nbdays,allbooks):
            self.libs=libs
            self.nbdays=int(nbdays)
            self.allbooks=allbooks

def read_in_file(file_name):
    
    with open(file_name, "r") as input_file:
        firstline=input_file.readline()
        split_nb=firstline.strip().split()
        nbbooks=split_nb[0]
        nblibs=split_nb[1]
        nbdays=split_nb[2]
        bookscores=input_file.readline().strip().split()
        all_books={}
        for bookid in range(len(bookscores)):
            all_books[bookid]=Book(int(bookid),int(bookscores[bookid]))
        all_libs=[]
        lib_id=0
        while True:
            line=input_file.readline()           
            if not line:
                break
            split_line=line.strip().split()
            if len(split_line)==0:
                break
            nb_books_lib=split_line[0]
            nb_days_sign=split_line[1]
            nb_per_day=split_line[2]
            books_in_lib=[]
            split_book_ids=input_file.readline().strip().split()
            for bookid in split_book_ids:
                books_in_lib.append(all_books[int(bookid)])
            all_libs.append(Library(lib_id,books_in_lib,nb_days_sign,nb_per_day))
            lib_id += 1
    return AllInfo(all_libs,nbdays,all_books)

def write_output_file(solution_file_name, libs, lib_book_dict):
    with open(solution_file_name, "w") as f:

        f.write("{}\n".format(len(libs)))
        for key in lib_book_dict:
            f.write("{} {}\n".format(key,len(lib_book_dict[key])))
            f.write(" ".join(map(str,lib_book_dict[key])) + "\n")


def read_in_file2(file_name):
    with open(file_name, "r") as f:
        data = dict()
        fl = f.readline()
        fl = fl.strip().split()
        nbooks = int(fl[0])
        nlibs = int(fl[1])
        days = int(fl[2])
        data["days"] = days
        data["libs"] = np.array(range(0, nlibs))
        data["score"] = np.array(f.readline().strip().split()).astype(int)
        data["books"] = []
        data["signup"] = np.zeros_like(data["libs"])
        data["ships"] = np.zeros_like(data["libs"])
        data["nbooks"] = nbooks
        data["totbooks"] = 0
        data["cumscore"] = []
        for i in range(0, nlibs):
            nl = f.readline().strip().split()
            data["signup"][i] = nl[1]
            data["ships"][i] = nl[2]
            nl = np.array(f.readline().strip().split()).astype(int)
            sort_idx = data["score"][nl].argsort()[::-1]
            sorted_books = nl[sort_idx]
            data["books"].append(sorted_books)
            if data["ships"][i] > sorted_books.size:
                data["ships"][i] = len(sorted_books)
            data["totbooks"] += len(sorted_books)
            data["cumscore"].append(data["score"][sorted_books].cumsum())
    return data


def write_output_file2(file_name, sol, data):
    with open(file_name, "w") as f:
        day = 0
        for i in range(0, sol.size):
            lib = sol[i]
            day += data["signup"][lib]
            if day >= data["days"]:
                break
            n_ship = (data["days"]-day)*data["ships"][lib]
            # with np.errstate(over='raise'):
            #     try:
            #         n_ship = (data["days"]-day)*data["ships"][lib]
            #     except FloatingPointError:
            #         n_ship = data["books"][lib].size
            n_ship = min(n_ship, data["books"][lib].size)
            data["books"][lib] = data["books"][lib][0:n_ship]

        f.write(str(i)+"\n")
        for j in range(0, i):
            lib = sol[j]
            books = data["books"][lib]
            f.write(str(lib)+" "+str(books.size)+"\n")
            for book in books:
                f.write(str(book)+" ")
            f.write("\n")


if __name__ == "__main__":
    all_info=read_in_file("input/a_example.txt")
    print(all_info.libs)
    print(all_info.nbdays)
    print(all_info.allbooks)