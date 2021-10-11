import cv2
import os
import Utils
import numpy as np
import easyocr

id = 0
vid = cv2.VideoCapture(id)
imgKTP = cv2.imread("Template_KTP(850x540).jpg")

reader = easyocr.Reader(['en'])

def main():
    
    while True:
        _, img = vid.read()
        #print(img.shape)

        scale = calculateScale(imgKTP.shape, img.shape)
        imgNewKTP = Utils.resize(imgKTP, scale)
        imgNewKTP, y,x = sameSize(imgNewKTP, img.shape)

        imgMerge = merge(imgNewKTP, img)

        cv2.imshow("merge", imgMerge)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord('s'):
            cv2.destroyAllWindows()

            KTPfix, newscale = rescale(img, y,x, scale)
            
            KTPfix = Utils.resize(KTPfix, newscale)
            cv2.imshow("KTPfix", KTPfix)
            keyFix = cv2.waitKey(0)
            if keyFix == ("q"):
                pass
            elif keyFix == ord("s"):
                # OCR
                KTPDetail = OCR(KTPfix)
                print(KTPDetail)
            cv2.destroyAllWindows()
                

    cv2.destroyAllWindows()
    vid.release()

def OCR(img):
    detailOCR = reader.readtext(img)
    return detailOCR
    
def rescale(img, y,x, scale):
    img = img[y:img.shape[0] - y - 1, x:img.shape[1] - x - 1]
    rescale = 1 / scale

    return img, rescale

def merge(imgKTP, img):
    imgKTP_inv = cv2.bitwise_not(imgKTP)

    imgKTPFix = cv2.addWeighted(imgKTP, 1, img, 1, 1)
    img = cv2.subtract(img, np.array([50.0]))
    imgKTPSide = cv2.addWeighted(imgKTP_inv, 1, img, 1, 1)

    bitwise_and1 = cv2.bitwise_and(imgKTPFix, imgKTP_inv)
    bitwise_and2 = cv2.bitwise_and(imgKTPSide, imgKTP)

    imgMerge = cv2.add(bitwise_and1, bitwise_and2)
    
    return imgMerge

def sameSize(imgKTP, shapeVid):
    blankImage = np.zeros((shapeVid), np.uint8)
    blankImage[:] = (255,255,255)
    

    y = int ((shapeVid[0] - imgKTP.shape[0]) / 2)
    x = int ((shapeVid[1] - imgKTP.shape[1]) / 2)

    blankImage[y:shapeVid[0] - y - 1, x:shapeVid[1] - x - 1] = imgKTP
    
    return blankImage, y,x

def calculateScale(shapeKTP, shapeVid):

    yKTP, wKTP, _ = shapeKTP
    yVid, wVid, _ = shapeVid

    toleranceY = yVid/10
    toleranceX = wVid/10

    y = yVid - yKTP
    w = wVid - wKTP
    if y > 0 & w > 0:
        pass
    else:
        if y > w:
            w = wVid - toleranceX
            scale = w / wKTP
            pass
        else:
            y = yVid - toleranceY
            scale = y / yKTP
            pass

    scale = round(scale,1)
    return scale

if __name__ == '__main__':
    main()