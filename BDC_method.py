def getSchedule(libs,books,nbDays):
    schedule = []
    scannedBooks = []
    readyTime = 0

    while readyTime<=nbDays:
        libs = [lib for lib in libs if lib.sign_time<nbDays-readyTime] # only keep libraries who can still be signed up in time
        libs.sort(key=lambda lib: sum(map(lambda book: book.score,lib.books))) # sort libraries in decreasing order of total score
        lib = libs.pop(0)
        schedule.append(lib)
        newScannedBooks = getScannedBooks(lib,readyTime,nbDays)
        for lib in libs:
            lib.books.remove(newScannedBooks)
        scannedBooks.append(newScannedBooks)




def getScannedBooks(lib,fromDay,nbDays):
    scannedBooks = []
    day = fromDay
    avBooks = lib.get_best_books()
    while day<=nbDays:
        scannedBooks.append(avBooks[:lib.scan_books])
        avBooks = avBooks[lib.scan_books+1:]
        day += 1
    return scannedBooks