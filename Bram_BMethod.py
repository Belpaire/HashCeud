from Parser import *
from Result import *

def createResultObjects(libs,maxdays):
    best_results=libs
    best_results.sort(key=lambda x: x.scoresOfSignTime(),reverse=True)
    print(list(map(lambda x: x.scoresOfSignTime(),best_results)))
    returnLibs=[]
    returnbooks=[]
    beginday=0
    for lib in best_results:
        returnLibs.append(lib)
        beginday+=lib.sign_time
        beginday+=1
        if beginday>maxdays:
            break
        returnbooks+=lib.get_best_books()
    return (returnLibs,returnbooks)

def fromInfoGetBestResults(all_libs):
    get_libs_scores=[]
    for lib in all_libs:     
        best_scores=lib.scoresOfSignTime()
        get_libs_scores.append(best_scores)
    return get_libs_scores


def getSignUpTime(libs):
    return map(lambda x: x.sign_time,libs)

if __name__ == "__main__":
    info_obj=read_in_file("a_example.txt")
    maxdays=info_obj.nbdays
    all_libs=info_obj.libs
    result=fromInfoGetBestResults(all_libs)
    print(result)
    print(info_obj.nbdays)
    print(list(getSignUpTime(all_libs)))
    print(createResultObjects(all_libs,maxdays))