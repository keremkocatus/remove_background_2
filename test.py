from rembg import new_session, remove
from PIL import Image

img = Image.open("./images/beyaz-uzeri-serpme-tasli-tisort.jpeg")

session = new_session(model_name="u2net")
processed_image = remove(img, session=session)

processed_image.show()