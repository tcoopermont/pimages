import PIL
from PIL import Image,ImageDraw,ImageFont

#orig image 800 × 450
#contactsheet  - 1200x675 
#contactsheet with footer - 1200x750 
#75/3 = 25 pixels/footer
R, G, B = 0, 1, 2

fnt = ImageFont.truetype("readonly/fanwood-webfont.ttf",46)
# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')

# build a list of 9 images which have different channel/intensitie
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

# create a contact sheet from different channel/intensities
first_image=images[0]
#print("width: " + str(first_image.width))
#print("height: " + str(first_image.height))
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,(first_image.height+50)*3))
draw = ImageDraw.Draw(contact_sheet)
x=0
y=0


#x: 0 y: 0
#x: 800 y: 0
#x: 1600 y: 0
#x: 0 y: 450
#x: 800 y: 450
#x: 1600 y: 450
#x: 0 y: 900
#x: 800 y: 900
#x: 1600 y: 900
for i in range(len(images)):
    img = images[i]
    #print("x: {} y: {}".format(x,y))
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    txt = "channel: {} intensity: {}".format(channels[i],intensities[i])
    pixColor = img.getpixel((0,0))
    print(pixColor)
    draw.text((x,y+450),txt,fill=pixColor,font=fnt)
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.

    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height + 50 
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
#display(contact_sheet)
contact_sheet.show()
