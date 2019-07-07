import cv2
import numpy
import math
from pathlib import Path
import pytesseract
import os
from PIL import Image,ImageDraw,ImageFont

srcDir = Path("/Users/tomcooper/repos/pimages/small_img")
cwd = Path.cwd() #used multiple places

txtDir = cwd / 'txt'
Path.mkdir(txtDir,exist_ok=True)
faceDir = cwd / 'png'
Path.mkdir(faceDir,exist_ok=True)

srcFileList = list(srcDir.glob('*.png'))

def buildCacheFilePath(src,atype):
    suff = "." + atype
    cwd = Path.cwd() #used multiple places
    subDir = cwd / atype 
    #handle case with multiple dots
    fnSplit = os.path.basename(f).split('.')
    fnSplit.pop()
    cacheName = ".".join(fnSplit) + suff 
    return subDir / cacheName 

def coords2img(srcImg,corner,size,destHeight):
# corner = (x,y), size = (h,w)
  x,y = corner
  h,w = size
  cr = srcImg[y:y+h,x:x+w]
  stx,sty = cr.shape[:2]
  factor = destHeight/sty
  return cv2.resize(cr,(int(stx*factor),int(sty*factor)))

for f in srcFileList:
    txtPath = buildCacheFilePath(f,'txt')
    print(txtPath)
    words = ''
    #words = pytesseract.image_to_string(Image.open(f))
    with open(txtPath, 'w') as wordFile:
        wordFile.write(words)


cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
for f in srcFileList:
    facePath = buildCacheFilePath(f,'png')
    print(facePath)
    img = cv2.imread(str(f))       
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

    destHeight = math.ceil(len(rects)/5) * 200
    destImg = numpy.zeros((destHeight,200*5,3), numpy.uint8)
    print(f"dest size: {destImg.shape[:2]}")
    curX = 0
    curY = 0
    for x,y,h,w in rects:
      print(f"writing image at: {curX},{curY}:")
      faceImg = coords2img(img,(x,y),(h,w),200)
      destImg[curY:curY+200,curX:curX+200] = faceImg
      curX += 200
      if curX == 1000:
          curX = 0
          curY += 200

    cv2.imwrite(str(facePath),destImg)

