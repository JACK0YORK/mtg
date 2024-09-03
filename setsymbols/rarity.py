from PIL import Image, ImageChops
# gradient_img = Image.open('diagonal_gradient.png')
# edge_mask = Image.open("edge_mask.png")
# big_mask = Image.open('big_mask.png') 

def make_icon(edge, big, gradient, target):
    gradient_img = Image.open(gradient)
    edge_mask = Image.open(edge)
    big_mask = Image.open(big) 

    if big_mask.size != gradient_img.size:
        gradient_img = gradient_img.resize(big_mask.size)
    if big_mask.mode != gradient_img.mode:
        gradient_img = gradient_img.convert(big_mask.mode)

    combined_image = ImageChops.add(big_mask, gradient_img)

    _,_,_,big_mask = big_mask.split()
    big_mask = ImageChops.add(big_mask, edge_mask)

    combined_image = ImageChops.subtract(combined_image, edge_mask.convert("RGBA"))

    combined_image.putalpha(big_mask)

    # combined_image = alpha_mask(combined_image, image1)


    combined_image.save(target)  # Save the image
    combined_image.show()  # Display the image