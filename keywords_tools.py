import scel_parser

def getAllFileNames():
    scel_file_info = scel_parser.getScelNames()
    return list(map(lambda item: item[1], scel_file_info))

def getKeywords(number, files = None, ignore_keywords = list([])):
    if files is None:
        files = scel_parser.getAllFilesPath()

    return scel_parser.getKeywords(number, files, ignore_keywords)