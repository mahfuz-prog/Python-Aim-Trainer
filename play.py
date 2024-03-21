import cv2
import numpy as np
import pyautogui
import time

'''
Robot speed affected by tutorial module
MAX_SIZE = 30
GROWTH_RATE = .2

Robot speed affected by this code
area >= 500
'''

# find the target from the mask
# detect the target using Contours
def getContours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # holds all detected target (x_axis,y_axis) and return
    circle = []

    # findContours return a tuple of multiple detected object
    for contour in contours:

        # get total area of a contour
        area = cv2.contourArea(contour)

        # Minimum area for a contour get selected
        if area >= 300:
            # gives the center point location of detected target circle
            M = cv2.moments(contour)
            (x_axis,y_axis), _ = cv2.minEnclosingCircle(contour)
            circle.append((int(x_axis),int(y_axis)))

    return circle


def play_game(play_time):
    print('Robot playing...')
    # get the window of the game which have position, size
    # Aim Trainer is the title for our game defined in tutorial.py
    aim_window = pyautogui.getWindowsWithTitle("Aim Trainer")[0]

    # used for how long we want to play the game
    t_start = time.perf_counter()
    total_click = 0

    while True:
        '''
        take a screenshot over pygame window with a 83 padding from top.
        83 padding exclude the top bar from the screenshort
        region=(left, top, width, height))

        take the image in HSV color space and create a mask using cv2.inRange()
        lower_bound = Hue Min, Sat Min, Val Min
        upper_bound = Hue Max, Sat Max, Val Max
        cv2.inRange(hsv_img, lower_bound, upper_bound)

        for finding the bounds I used my detect module. our target is white color.
        hue, sat, val is for white min(0 0 0) max(0 0 255)


        '''

        img = pyautogui.screenshot(region=(aim_window.left, aim_window.top + 83,\
            aim_window.width, aim_window.height - 83))
        imgHSV = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, np.array([0, 0, 0]), np.array([0, 0, 255]))

        # uncomment to see the mask image
        # imgResult = cv2.bitwise_and(np.array(img),np.array(img),mask=mask)
        # cv2.imshow('img_', np.array(img))

        targets = getContours(mask)
        for target in targets:
            x_axis = target[0]
            y_axis = target[1]
            pyautogui.moveTo(x_axis + aim_window.left, y_axis + aim_window.top + 83)
            pyautogui.click()
            total_click+=1

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        t_end = time.perf_counter()
        if t_end >= t_start+play_time:
            break

    print('Robo clicks:', total_click)

# play_time is how many seconds we want to play
play_game(play_time=10)