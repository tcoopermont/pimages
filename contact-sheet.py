import PIL
from PIL import Image,ImageDraw

R, G, B = 0, 1, 2

# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')
height,width = image.size 
#draw = ImageDraw.Draw(image)
#draw.text((10,400),"testxxx")

# build a list of 9 images which have different brightnesses
#enhancer=ImageEnhance.Brightness(image)
images=[]
channels = [0,0,0,1,1,1,2,2,2]
intensities = [0.1,0.5,0.9]*3
for i in range(0, 9):
    source = image.split()
    out = source[channels[i]].point(lambda x: x * intensities[i])
    source[channels[i]].paste(out)
    images.append(Image.merge(image.mode,source))
    #images.append(enhancer.enhance(i/10))

# create a contact sheet from different brightnesses
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
#display(contact_sheet)
contact_sheet.show()
