from Parser import *
from Result import *



def writeOutput(libids,lib_book_dict,outputname):
    with open(outputname,"w+") as output_file:
        result=""
        result+=str(len(libids))+"\n"
        for key in lib_book_dict:
            result+=str(key)+" "+ str(len(lib_book_dict[key])) +" \n"
            for book_id in lib_book_dict[key]:
                result+=str(book_id)+" "
            result+="\n"
        output_file.write(result)

def reSort(libs,already_read):
    libs.sort(key=lambda x: x.scoresOfSignTime(already_read),reverse=True)
    return libs

def createResultObjects(libs,maxdays):
    temp_libs=libs
    already_read_ids=set()
    reSort(temp_libs,already_read_ids)
    print(list(map(lambda x: x.scoresOfSignTime(already_read_ids),temp_libs)))
    returnLibs=set()
    returnbooks=dict()
    beginday=0
    while beginday<=maxdays:   
        lib=temp_libs[0]   
        returnLibs.add(lib.id)
        lib_id=lib.id 
        best_results=lib.get_best_books(already_read_ids)
        best_results_ids=set(map(lambda x: x.id,best_results))
        if lib.id not in already_read_ids:
            beginday+=lib.sign_time
        beginday+=1
        already_read_ids.update(best_results_ids)
        if lib_id in returnbooks:
            returnbooks[lib_id].update(best_results_ids)
        else:
            returnbooks[lib_id]=best_results_ids
        
        reSort(temp_libs,already_read_ids)
    return (returnLibs,returnbooks)

def fromInfoGetBestResults(all_libs):
    get_libs_scores=[]
    for lib in all_libs:     
        best_scores=lib.scoresOfSignTime(set())
        get_libs_scores.append(best_scores)
    return get_libs_scores


def getSignUpTime(libs):
    return map(lambda x: x.sign_time,libs)
import sys
if __name__ == "__main__":
    info_obj=read_in_file(sys.argv[1])
    maxdays=info_obj.nbdays
    all_libs=info_obj.libs
    result=fromInfoGetBestResults(all_libs)
    #print(result)
    #print(info_obj.nbdays)
    #print(list(getSignUpTime(all_libs)))
    entire_result=createResultObjects(all_libs,maxdays)
    print(entire_result)
    writeOutput(entire_result[0],entire_result[1],sys.argv[2])