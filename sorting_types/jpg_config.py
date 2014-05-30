from PIL import Image
import os, glob, shutil

def sortKey(filename):
    ans = "Z" * 30
    try: 
        ans = Image.open(filename)._getexif()[306] 
    except KeyError: 
        try: 
            ans = Image.open(filename)._getexif()[36868] 
        except KeyError: 
            print("No timestamp")
    return ans

def sortJpgByDate(fileType = "jpg"):
    os.mkdir("tmp")
    for item in glob.iglob("*"):
        shutil.move(item, "tmp")
    items = glob.glob("tmp/*")
    print("items", items)
    items.sort(key = sortKey)
    name_len = len(str(len(items)))
    print("glob *: ", glob.glob("*"))
    for i in range(len(items)):
        print("file", items[i])
        shutil.move(items[i], (("0" * (name_len - len(str(i + 1)))) + str(i + 1)) + "." + fileType)

    for item in glob.iglob("*"):
        shutil.move(item, "tmp")

    items = glob.glob("tmp/*")
    for i in range(len(items)):
        sk = sortKey(items[i])
        if not sk:
            if not os.path.isdir("без даты"):
                os.mkdir("без даты")
            shutil.move(items[i], "без даты/" + (("0" * (name_len - len(str(i + 1)))) + str(i + 1)) + "." + fileType)
        else:
            y, m, d = sk.split()[0].split(":")
            if not os.path.isdir(y):
                os.mkdir(y)
            if not os.path.isdir(y + "/" + m):
                os.mkdir(y + "/" + m)
            if not os.path.isdir(y + "/" + m + "/" + d):
                os.mkdir(y + "/" + m + "/" + d)
            shutil.move(items[i], y + "/" + m + "/" + d)

    os.rmdir("tmp")