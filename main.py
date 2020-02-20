import sys
import os
import shutil
from Parser import *
from BDC_method import getSchedule

def main(filename):
    data = read_in_file('input/{}.txt'.format(filename))

    output = getSchedule(data.libs,data.allbooks,data.nbdays)

    write_output_file('output/{}.txt'.format(filename), output)



if __name__ == "__main__":

    input_files = ['a_example','b_read_on','c_incunabula','d_tough_choices','e_so_many_books','f_libraries_of_the_world']
    files_to_zip = ['Book.py','Parser.py','Library.py']
    filename = 'b_read_on'
    if(len(sys.argv)>1):
        filename = sys.argv[1]

    if filename == 'all':
        for filename in input_files:
            print(filename)
            main(filename)
            pass
        os.makedirs("code", exist_ok=True)
        for file in files_to_zip:
            shutil.copyfile(file,'code/{}'.format(file))
        shutil.make_archive("output/code",'zip','code')
        shutil.rmtree("code")
    else:
        main(filename)