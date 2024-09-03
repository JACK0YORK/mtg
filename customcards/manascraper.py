from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import hashlib
from PIL import Image, ImageChops, ImageDraw
import io

def get_html_hash(file_path:str):
    hash256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        for line in file.readlines():
            hash256.update(line)
    return hash256.hexdigest()

def add_corners(im, rad=100):
    circle = Image.new('L', (rad * 6, rad * 6), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 6, rad * 6), fill=255)
    circle = circle.resize(im.size)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

    alpha = ImageChops.darker(alpha, im.split()[-1])
    
    im.putalpha(alpha)
    return im



def extract_symbol_from_driver(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
    width = element.size["width"]
    icon_image = Image.open(io.BytesIO(element.screenshot_as_png))
    return add_corners(icon_image, int(width/2)+1)

def extract_icons_from_local_html(html_path, css_selectors):
    options = Options()
    options.headless = True
    
    local_url = f'{os.path.abspath(html_path)}'.replace("\\","/")
    with webdriver.Chrome(options=options) as driver:
        driver.get(local_url)
        for selector in css_selectors:
            extract_symbol_from_driver(driver, "i.ms-cost."+selector).save("mana-icons/"+selector+".png")

        

if __name__=="__main__":
    mana_symbols = ["ms-untap", "ms-tap", "ms-wup", "ms-wbp", "ms-ubp", "ms-urp", "ms-brp", "ms-bgp", "ms-rwp", "ms-rgp", "ms-gwp", "ms-gup", "ms-wu", "ms-wb", "ms-ub", "ms-ur", "ms-br", "ms-bg", "ms-rw", "ms-rg", "ms-gw", "ms-gu", "ms-2w", "ms-2u", "ms-2b", "ms-2r", "ms-2g", "ms-wp", "ms-up", "ms-bp", "ms-rp", "ms-gp", "ms-s", "ms-c", "ms-0", "ms-1", "ms-2", "ms-3", "ms-4", "ms-5", "ms-6", "ms-7", "ms-8", "ms-9", "ms-10", "ms-11", "ms-12", "ms-13", "ms-14", "ms-15", "ms-16", "ms-17", "ms-18", "ms-19", "ms-20", "ms-w", "ms-u", "ms-b", "ms-r", "ms-g"]
    extract_icons_from_local_html("mana-master/index.html", mana_symbols)
    print("done")
    # w = 59*7
    # circle = Image.new("L", (w,w))
    # draw = ImageDraw.Draw(circle)
    # draw.ellipse((0, 0, w, w), fill=255)
    # smaller = circle.resize((59, 59), Image.LANCZOS)
    # smaller.save("mana-icons/mask.png")
    # add_corners()



# ms-e


# "{0}", "{1}", "{2}", "{3}", "{4}"
    
# "{X}"
# "{W/U}", "{W/B}", "{U/B}", "{U/R}", "{B/R}", "{B/G}", "{R/G}", "{R/W}", "{G/W}", "{G/U}"
# "{2/W}", "{2/U}", "{2/B}", "{2/R}", "{2/G}"
# "{W/P}", "{U/P}", "{B/P}", "{R/P}", "{G/P}"
# "{W/U/P}", "{W/B/P}", "{U/B/P}", "{U/R/P}", "{B/R/P}", "{B/G/P}", "{R/G/P}", "{R/W/P}", "{G/W/P}", "{G/U/P}"
# "{S}"