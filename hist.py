import cv2
import numpy as np

image_resolution = (640, 480)
histogram_bin = 64 

target_hist_bar = None
hist_value_change = None
prev_hist_value = None
histogram = None
img = None

def hist_to_image(hist, colored_idx = -1):
    w, h = image_resolution
    hist_image = np.zeros((h, w, 3), dtype=np.uint8)
    unit_hist_box_width = int(w / histogram_bin)
    max_hist = np.max(hist)
    prev = 0
    for idx, ht in enumerate(hist):
        if idx == colored_idx:
            color = (0,0,255)
        else:
            color = (255,255,255)
        hist_image[h-int(ht / max_hist * h):h, prev:prev+unit_hist_box_width, :] = color
        prev = prev+unit_hist_box_width
    return hist_image

def print_image(target_image, hist):
    output = np.concatenate((target_image, hist), axis=1)
    cv2.imshow("Main Window", output)

def get_target_hist_bar(x):
    unit = int(image_resolution[0]/histogram_bin)
    print(unit)
    return int((x - image_resolution[0])/unit)

def deform_histogram(target_bar_idx, amount):
    global histogram
    histogram[target_bar_idx] += amount
    if histogram[target_bar_idx] < 0:
        histogram[target_bar_idx] = 0

def DO_YOUR_METHOD():
    pass

def mouse_event_handler(event, x, y, flags, param):
    global target_hist_bar
    global hist_value_change
    global prev_hist_value
    if event == cv2.EVENT_LBUTTONDOWN:
        target_hist_bar = get_target_hist_bar(x)
        prev_hist_value = y
        print("target : ", target_hist_bar, "original_value :", prev_hist_value)
    elif flags == cv2.EVENT_FLAG_LBUTTON:  
        print("mouse moving", x, y)
        hist_value_change = 30*(prev_hist_value - y)
        prev_hist_value = y
        print("original : ",prev_hist_value,"y : ",y,"change : ", hist_value_change)
        deform_histogram(target_hist_bar, hist_value_change)
    elif event == cv2.EVENT_LBUTTONUP:
        hist_value_change = prev_hist_value - y
        deform_histogram(target_hist_bar, hist_value_change)
        target_hist_bar = -1


    elif event == cv2.EVENT_RBUTTONDOWN:
        DO_YOUR_METHOD()

    hist_image = hist_to_image(histogram, target_hist_bar)
    print_image(img, hist_image)

def run_main():
    cv2.namedWindow("Main Window")
    cv2.setMouseCallback("Main Window", mouse_event_handler)
    global histogram, img
    img = cv2.imread('./target.jpg',cv2.IMREAD_COLOR)
    img = cv2.resize(img, image_resolution)

    histogram = cv2.calcHist(images=[img],channels=[0],mask=None,histSize=[histogram_bin],ranges=[0,256])
    hist_image = hist_to_image(histogram)
    print_image(img, hist_image)

    cv2.waitKey(0)      
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_main()