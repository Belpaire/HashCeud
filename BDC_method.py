def getSchedule(libs,books,nbDays):
    schedule = []
    lib_book_dict = dict()
    readyTime = 0

    while readyTime<=nbDays and not len(libs)==0:
        libs = [lib for lib in libs if lib.sign_time<nbDays-readyTime] # only keep libraries who can still be signed up in time
        if len(libs)>0:
            libs.sort(key=lambda lib: sum([book.score for book in lib.books])) # sort libraries in decreasing order of total score
            lib = libs.pop(0)
            schedule.append(lib.id)
            readyTime += lib.sign_time
            scannedBooks = getScannedBooks(lib,readyTime,nbDays)
            lib_book_dict[lib.id] = scannedBooks
            for lib in libs:
                lib.books = [book for book in lib.books if book.id not in scannedBooks] # remove scannedBooks from other libs

    return (schedule,lib_book_dict)



def getScannedBooks(lib,fromDay,nbDays):
    scannedBooks = []
    day = fromDay
    avBooks = sorted(lib.books,key=lambda book: book.score)
    while day<=nbDays:
        scannedBooks.extend([book.id for book in avBooks[:lib.scan_books]])
        avBooks = avBooks[lib.scan_books:]
        day += 1
    return scannedBooks