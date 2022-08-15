import re
import numpy as np
import cv2
import os
import pytesseract
import pyautogui
from imutils import contours


def test_img():
    #time.sleep(1)
    #image1 = cv2.imread('res.png')
    #print('[image1]',image1)

    image2 = pyautogui.screenshot()
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)


    scale_percent = 1
    width = int(image2.shape[1] * scale_percent / 100)
    height = int(image2.shape[0] * scale_percent / 100)
    dsize = (width, height)
    image2 = cv2.resize(image2, dsize)

    cv2.imwrite("res.png", image2)
    #print('[image2]', image2)
    #image2.save('res.png')

def search_in_pictures():
    img = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    #cv2.imwrite('res.png',img )
    return img

def parse(name):
    image = cv2.imread(name)
    #image = cv2.imread('text1.png')
    #image = search_in_pictures()
    #height, widht, _ = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_OTSU)[1]
    #cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cnts, _ = contours.sort_contours(cnts[0])

    #custom_config = r'--oem 3 --psm 11'
    custom_config = r'--oem 3 --psm 11'
    text = pytesseract.image_to_data(image, config=custom_config)

    save_text_for_foto(gray,name,text)

    text = text.replace('\n',' ')
    for str in text.split():
        if (len(str) == 5) and str.isupper():
            res = re.sub("[^A-Z0-9?]", "", str)
            res = res.replace(' ','')
            if (len(res) == 5) and not check_bad_list(res):
                #print('[parse]', res,'   ', len(res))
                return res
                #return create_unknown_nums(res)




def save_text_for_foto(image,name,text):
    for i, el in enumerate(text.splitlines()):
        if i == 0:
            continue
        el = el.split()
       # print(">>>",el)
        try:
            # Создаем подписи на картинке и делаем картинку серой
            x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
            cv2.rectangle(image, (x, y), (w + x, h + y), (0, 0, 255), 1)
            cv2.putText(image, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            cv2.imwrite(name, image)
        except IndexError:
            print("Операция была пропущена")


# это костыль, надо исправить
def check_bad_list(find):
    bad_list = ['ARTES','ARTED','ARTER','RATER','MARTE','RARER','ARTE', 'MARTER', 'HARTER', 'KARTER', 'RARTER', 'WAITER', 'WARTER', 'KARTE', 'YARTER', 'CARTER', 'RUMEL', 'BAFOI', 'WAEN', 'PARTER', 'SAGES', 'WARTED', 'WARIEE', 'WARTEE', 'ROBIN', 'FARTER', 'WARTE', 'GARTER', 'WRITE','YARED', 'MARTEL', 'MATER', 'MADTER', 'ARIER', 'AARTER', 'PARTE',  'RTER', 'WATER']  # , 'POOLE','INNIN','DATOS','SARTO'
    res = False
    for bl in bad_list:
        if bl == find:
            res = True
    return res



def create_unknown_nums(s):
    ar = []
    if not s.isalpha():
        for i in range(10):
            ar.append(s.replace("?",str(i)))
    else:
        ar.append(s)
    return ar

PATH_IMG = 'temp/temp-img/'

def Go():
    lists = os.listdir(PATH_IMG)
    lists.sort()
    ar = []
    old = ''
    for addr in lists:
        if addr[-4:] == '.jpg':
            res = parse(PATH_IMG+addr)
            if res and res.strip() and res != old:
                ar.append(res)
                print('[add]',res,'  old=',old,'    ',addr)
                old = res
    print('[end]',ar)

def del_image():
    lists = os.listdir(PATH_IMG)
    for l in lists:
        os.remove(PATH_IMG+l)
