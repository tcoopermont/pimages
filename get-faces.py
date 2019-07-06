import cv2
import numpy
import math

def coords2img(srcImg,corner,size,destHeight):
# corner = (x,y), size = (h,w)
  x,y = corner
  h,w = size
  cr = srcImg[y:y+h,x:x+w]
  stx,sty = cr.shape[:2]
  factor = destHeight/sty
  return cv2.resize(cr,(int(stx*factor),int(sty*factor)))

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread('/Users/tomcooper/repos/pimages/small_img/a-0.png')       
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

cv2.imwrite("page1.png",destImg)

