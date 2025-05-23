import cv2

def click_event(event, x, y, flags, params):
 
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 1)
        cv2.imshow('image', img)

    if event==cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 1)
        cv2.imshow('image', img)
 
# driver function
if __name__=="__main__":

    image = r'D:/fern/project_Fern/OCRmarkingValidation/V4/Sample Mark for OCR Test/1.jpg'
    img = cv2.imread(image, 1)

    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
