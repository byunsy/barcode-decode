"""============================================================================
TITLE: barcode.py
BY   : Sang Yoon Byun
============================================================================"""

import sys
import numpy as np
import cv2
import pyzbar.pyzbar as pz
from pyzbar.pyzbar import ZBarSymbol


"""============================================================================
PROCEDURE:
    draw_guide
PARAMETERS:
    img, a source image frame
PURPOSE:
    draws a simple, transparent border box for users to place the barcode.
PRODUCES:
    dst, an image frame overlayed with guidance border box
============================================================================"""
def draw_guide(img):

    # Set Colors
    # COLOR_1 = (192, 192, 255)
    COLOR_1 = (0,255,255)

    # Create a copy of the original image
    cp = img.copy()
    img_h, img_w = img.shape[:2]

    dist1 = round((img_w//2)*0.6)
    dist2 = round((img_h//2)*0.5)

    # Set corners
    top_l = (img_w//2 - dist1, img_h//2 - dist2)
    top_r = (img_w//2 + dist1, img_h//2 - dist2)
    bot_l = (img_w//2 - dist1, img_h//2 + dist2)
    bot_r = (img_w//2 + dist1, img_h//2 + dist2)

    # Draw a border box
    cv2.line(cp, top_l, (top_l[0]+20, top_l[1]), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, top_l, (top_l[0], top_l[1]+20), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, top_r, (top_r[0]-20, top_r[1]), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, top_r, (top_r[0], top_r[1]+20), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, bot_l, (bot_l[0]+20, bot_l[1]), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, bot_l, (bot_l[0], bot_l[1]-20), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, bot_r, (bot_r[0]-20, bot_r[1]), COLOR_1, 6, cv2.LINE_AA)
    cv2.line(cp, bot_r, (bot_r[0], bot_r[1]-20), COLOR_1, 6, cv2.LINE_AA)

    # This makes the lines a little transparent
    dst = cv2.addWeighted(img, 0.5, cp, 0.5, 0)

    return dst

"""============================================================================
PROCEDURE:
    decode
PARAMETERS:
    img, a source image frame
PURPOSE:
    takes in img, decodes a barcode if it exists, and visualizes the scanned
    region of barcode.
PRODUCES:
    barcode_num, decoded barcode number
============================================================================"""
def decode(img):

    _, img_w = img.shape[:2]

    # Find barcodes
    decoded = pz.decode(img, symbols=[ZBarSymbol.EAN13, ZBarSymbol.ISBN13])
    
    if decoded:

        # Find one decoded object
        obj = decoded[0]

        # Attain the coordinates of the detected barcode
        coords = np.array([point for point in obj.polygon], dtype=np.int32)

        # Only if its area is big enough
        # if cv2.contourArea(coords) >= 1000:

        coords = coords.reshape((-1,1,2))

        # Simplify contour lines with Douglas–Peucker algorithm
        approx = cv2.approxPolyDP(coords, 
                                    cv2.arcLength(coords, True) * 0.02, True)

        # Ignore if non-rectangle
        if len(approx) == 4 and cv2.contourArea(coords) >= 5000:
 
            # Draw border lines around the detected barcode
            cv2.polylines(img, [approx], True, (0,255,255), 5, cv2.LINE_AA)
            
            text = "Scanning..."
            t_wh, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            text_pos = (img_w//2 - t_wh[0]//2, 50)

            cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 255, 255), 2, cv2.LINE_AA)
        
            cv2.imshow('frame', img)
            cv2.waitKey(1000)

            return int(obj.data)
    
    cv2.imshow('frame', img)

"""============================================================================
                                     MAIN
============================================================================"""
def main():

    # Initialize and open default camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Check for any errors opening the camera
    if not cap.isOpened():
        print("Error: Failed to open camera.")
        sys.exit()

    # Keep running until barcode is detected
    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = draw_guide(frame)

        # decode barcode if it exists
        barcode_num = decode(frame)

        # if successfully decoded
        if barcode_num:
            print(barcode_num)
            break

        # exit if pressed ESC
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()    