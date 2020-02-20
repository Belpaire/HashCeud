from Parser import *
from Result import *



def fromInfoGetResults(info_object):
    deadline_days=info_object.nbdays
    all_books=info_object.allbooks
    all_libs=info_object.libs
    for lib in all_libs:
        lib.scoresOfSignTime()



if __name__ == "__main__":
    fromInfoGetResults(read_in_file("a_example.txt"))