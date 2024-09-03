from PIL import Image, ImageDraw
import math

def diagonal_gradient(width, height, colors, angle):
    # Create a new RGB image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Calculate diagonal length
    angle_radians = math.radians(angle)
    dx = math.cos(angle_radians)
    dy = math.sin(angle_radians)

    # Draw diagonal gradient
    for y in range(height):
        for x in range(width):
            # Calculate normalized position along the gradient vector
            ratio = (dx * (x -width/8) + dy * (y-height/8)) / (math.sqrt(dx**2 + dy**2) * max(width, height))
            ratio = max(0, min(1, ratio))

            segment = ratio * (len(colors) -1)
            lower_index = math.floor(segment)
            upper_index = math.ceil(segment)
            
            # Interpolate colors based on ratio and segment
            if lower_index == upper_index:
                color = colors[int(segment)]
            else:
                ratio_in_segment = segment - lower_index
                lower_color = colors[int(lower_index)]
                upper_color = colors[int(upper_index)]
                
                # Interpolate between lower_color and upper_color
                r = int(lower_color[0] * (1 - ratio_in_segment) + upper_color[0] * ratio_in_segment)
                g = int(lower_color[1] * (1 - ratio_in_segment) + upper_color[1] * ratio_in_segment)
                b = int(lower_color[2] * (1 - ratio_in_segment) + upper_color[2] * ratio_in_segment)
                
                color = (r, g, b)
            
            
            # Draw pixel with calculated color
            draw.point((x, y), fill=color)

    return img

colors = {
    "mythic" : ((215, 95, 36), (237 , 139, 31), (215, 95, 36)),
    "rare" : ((159, 142, 87), (252, 226, 146), (159, 142, 87)),
    "uncommon" : ((111, 126, 139), (190, 215, 232), (111, 126, 139))
}

if __name__=="__main__":
    for color in colors:
        width = 1000
        height = 1000
        output_image_path = f'{color}_gradient.png'

        gradient_img = diagonal_gradient(width, height, colors[color], 15)
        gradient_img.save(output_image_path)
        gradient_img.show()  # Optionally display the image