from PIL import Image
def make_thumb(path,size=150):
    pixbuf = Image.open(path)
    width, height = pixbuf.size
    if height > size:
        delta = height / size
        width = int(width / delta)
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)
        return pixbuf

def make_thumb_fixed(path,w=224,h=224):
    pixbuf = Image.open(path)
    width, height = pixbuf.size
    if height > h and width>w:
        pixbuf=pixbuf.resize((w, h), Image.ANTIALIAS)
        return pixbuf
    else:
        return pixbuf

if __name__=="__main__":
    pass