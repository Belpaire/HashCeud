from Book import Book
from Library import Library
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


if __name__ == "__main__":
    all_info=read_in_file("input/a_example.txt")
    print(all_info.libs)
    print(all_info.nbdays)
    print(all_info.allbooks)