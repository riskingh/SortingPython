import os, glob, shutil, mimetypes, math
from sorting_types.global_variables import SORT_KEYS
def dictUnion(d1, d2):
    '''
    Returns dict that is union of two dicts d1, d2
    If k is key of d1 but not d2 (or vice versa) then d[k] = d1[k]
    If k is key of both d1 and d2 then d[k] = d1[k] + d2[k]
    '''
    d = {}

    for k in d1.keys():
        d[k] = d1[k]

    for k in d2.keys():
        if k in d:
            d[k] += d2[k]
        else:
            d[k] = d2[k]

    return d


def fileTypes(fpath):
    '''
    Returns dict where keys are files' types and values are counts
    '''
    mime = mimetypes.MimeTypes()
    os.chdir(fpath)
    types = {}
    for item in glob.iglob("*"):
        if os.path.isdir(item):
            types = dictUnion(types, fileTypes(item))
            os.chdir("..")
        else:
            ext = "NoType"
            if "." in item:
                ext = item.split(".")[-1]
            if ext in types:
                types[ext] += 1
            else:
                types[ext] = 1
    return types

def unpack(fpath, destination):
    '''
    Copies all files from fpath to destination
    '''

    os.chdir(fpath)

    for item in glob.iglob("*"):
        if os.path.isdir(item):
            unpack(item, destination)
            os.chdir("..")
        else:
            shutil.copy(item, destination)

def sortByType(fpath):
    '''
    Moves every file into folder with name equals to this type.
    For files with no type after "." there is folder called NoType
    '''

    os.chdir(fpath)

    for item in glob.iglob("*"):
        if os.path.isdir(item):
            continue
        else:
            ext = "NoType"
            if "." in item:
                ext = item.split(".")[-1]
            if not os.path.isdir(ext):
                os.mkdir(ext)
            shutil.move(item, ext)

def clearDir(fpath):
    '''
    Removes everything in fpath
    '''

    os.chdir(fpath)

    for item in glob.iglob("*"):
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

def sortAndRename(fileType):
    '''
    os.path must be in folder that includes only files with type fileType
    This function creates dir "tmp" and moves every file in it.
    Then it sorts files, using key from SORT_KEYS.
    Moves files out of "tmp" and rename it according to it's position in array.
    After all it removes "tmp"
    '''

    os.mkdir("tmp")
    for item in glob.iglob("*"):
        shutil.move(item, "tmp")
    items = glob.glob("tmp/*")
    print("items", items)
    items.sort(key = SORT_KEYS[fileType])
    name_len = len(str(len(items)))
    print("glob *: ", glob.glob("*"))
    for i in range(len(items)):
        print("file", items[i])
        shutil.move(items[i], (("0" * (name_len - len(str(i + 1)))) + str(i + 1)) + "." + fileType)
    os.rmdir("tmp")



def sortFiles(fpath):
    '''
    First moves into fpath.
    Then gets all types and sorts it if SORT_KEYS defined
    '''

    os.chdir(fpath)

    types = []
    for item in glob.iglob("*"):
        if os.path.isdir(item):
            types.append(item)
    
    for tp in types:
        if tp in SORT_KEYS:
            os.chdir(tp)
            sortAndRename(tp)
            os.chdir("..")

if __name__ == "__main__":
    print("folder_dfs.py called as main")
    fpath = input("Enter fpath: ")
    temp = input("Enter temp: ")
    clearDir(temp)
    print(fileTypes(fpath))
    unpack(fpath, temp)
    sortByType(temp)
    sortFiles(temp)
