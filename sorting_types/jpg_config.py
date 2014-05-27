from PIL import Image

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