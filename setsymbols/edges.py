from PIL import Image, ImageFilter, ImageChops
 

base_path = r"Warframe-Logo.png"
thickness = 2
def generate_edge_mask(base_path, thickness):
    base_img = Image.open(base_path)
    edge_path = base_path[:-4]+"_edge_mask.png"
    big_path = base_path[:-4]+"_common.png"

    # Converting the image to grayscale, as Sobel Operator requires
    # input image to be of mode Grayscale (L)
    img = base_img.convert("L")
    
    # Calculating Edges using the passed laplacian Kernel
    # img.show()
    img = img.filter(ImageFilter.FIND_EDGES)
    # img.show()
    margin=3
    img = img.crop((margin, margin, img.width-margin, img.height-margin))
    def uncrop(img, margin):
        width, height = img.size
        new_width = width + 2 * margin
        new_height = height + 2 * margin
        new_img = Image.new('L', (new_width, new_height), (0))
        new_img.paste(img, (margin, margin))
        return new_img
    img = uncrop(img, 3)


    img = img.point(lambda x: 255 if x > 130 else 0, mode='L')

    for _ in range(thickness):
        img = img.filter(ImageFilter.MaxFilter(size=5))
        img = img.filter(ImageFilter.GaussianBlur(radius=2))


    img = img.point(lambda x: 255 if x > 100 else 0, mode='L')

    img.save(edge_path)

    # Mask for opacity
    def alpha_mask(base_img, alpha_img):
        base_img = base_img.convert('RGBA')
        result_img = base_img.copy()
        result_img.putalpha(alpha_img)
        return result_img

    _,_,_,inner_mask = base_img.split()
    big_mask = ImageChops.add(inner_mask, img)
    img = alpha_mask(img, big_mask)

    final=img
    final.save(big_path)

    return edge_path, big_path