from PIL import Image, ImageDraw, ImageColor

im = Image.open("templates/blackcreature.png", formats=["PNG"])
# colors = blackcreature.getcolors(99999)

def multiply(im, r, g, b):
    R, G, B = 0, 1, 2
    source = im.split()
    rr = source[R].point(lambda x: min(x*r,255))
    source[R].paste(rr)
    gg = source[G].point(lambda x: min(x*g,255))
    source[G].paste(gg)
    bb = source[B].point(lambda x: min(x*b,255))
    source[B].paste(bb)
    return Image.merge(im.mode, source)
def add(im, r, g, b):
    R, G, B = 0, 1, 2
    source = im.split()

    def avgmask(x, avg=[], count=[0]):
        if x==None:
            count+=1
            return avg
        if count[0]==0:
            avg.append(x)
        return x

    # im.point(runningextrema)
    # runningextrema(None)
    # mask = im.point(lambda x: x>1 and 255)
    rr = source[R].point(lambda x: min(x+r,255))
    source[R].paste(rr, mask)
    gg = source[G].point(lambda x: min(x+g,255))
    source[G].paste(gg, mask)
    bb = source[B].point(lambda x: min(x+b,255))
    source[B].paste(bb, mask)
    return Image.merge(im.mode, source)


im = add(im, 180, 80, 50)
im = multiply(im, 2, 2, 2)
# im.save("templates/bluecreature.png")
im.show()
# im.save()
# print(len(red[0]))
# blackcreature