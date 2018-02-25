from PIL import image
import os

size_300 = (300,300)
size_700 = (700,700)

for img in os.listdir('.'):
    if img.endswith('.jpg'):
        pic = Image.open(img)
        img_name, img_ext = os.path.splittext(img)
        # pic.save('pngs/{}.png'.format(img_name))

        pic.thumbnail(size_700)
        pic.save('700/{}_700{}'.format(img_name, img_ext))

        pic.thumbnail(size_300)
        pic.save('300/{}_300{}'.format(img_name, img_ext))
# image1 = Image.open('pup1.jpg')
# image1.save('pup1.png')



