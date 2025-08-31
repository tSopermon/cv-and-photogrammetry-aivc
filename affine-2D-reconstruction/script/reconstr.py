import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

points = np.zeros((4, 3), dtype=float)
counter = 0
Hp_computed = False
Hp = None

def MousePoints(event, x, y, flags, params):
    global counter 
    global Hp
    global Hp_tr
    if event == cv.EVENT_LBUTTONDBLCLK:
        points[counter] = [x, y, 1.0]
        print(f"Point {counter + 1}: ({x}, {y})")
        counter = counter + 1
        if counter == 4:
            # computing lines
            l1 = np.cross(points[0], points[1]) # top line
            l2 = np.cross(points[2], points[3]) # bottom line
            l3 = np.cross(points[0], points[3]) # left line
            l4 = np.cross(points[1], points[2]) # right line

            # computing vanishing points
            v1 = np.cross(l1, l2)
            v2 = np.cross(l3, l4)
            print(f"\n Vanishing Points: {v1}, {v2}")

            # Computing vanishing line
            lv = np.cross(v1, v2) 
            lv = lv / lv[2] # converting lv[2] to 1 (normalization)
            print(f"\n Vaninshing Line: {lv}")
            
            Hp = np.array([[1, 0, 0], 
                           [0, 1, 0], 
                           [lv[0], lv[1], lv[2]]]) # affine transformation matrix, replacing the last row with vanishing line's coefficients
            
            print(f"\nTransformation Matrix: \n{Hp}\n")

            Hp_inv = np.linalg.inv(Hp) 
            Hp_tr = np.transpose(Hp_inv) # inverse of the transpose of the transformation matrix
            print(f"\nInverse Transpose Transformation Matrix: \n{Hp_tr}\n")
            print(f"Vanishing line must be [0, 0, 1]\n\nProof: \n{np.dot(Hp_tr, lv)}\n")

def resize_img(img, num):
    width, height = img.shape[1], img.shape[0]
    print(f"Original Image Size: \nWidth: {width}, Height: {height}\n")
    resized_width, resized_height = int(width / num), int(height / num)
    print(f"Image resized to {num} times smaller: \nWidth: {resized_width}, Height: {resized_height}")
    resized_img = cv.resize(img, (resized_width, resized_height), interpolation=cv.INTER_AREA)
    return resized_img

img_path = "Your_Image_Directory/Brueghel.jpg" # Change this to your image path
img = cv.imread(img_path)

resized_img = resize_img(img, 3)

cv.imshow('Perpectively distorted image', resized_img)

width, height = resized_img.shape[1], resized_img.shape[0]

cv.setMouseCallback('Perpectively distorted image', MousePoints)
while True:
    if counter == 4:
        # to compute new dimensions
        last_img_pixel = np.array([width, height, 1])
        # using transformation matrix to generate new coordinates of last pixel
        new_last_pixel = np.dot(Hp, last_img_pixel)
        new_last_pixel /= new_last_pixel[2] # normalization to scale the two coordinates
        new_width, new_height = int(new_last_pixel[0]), int(new_last_pixel[1]) # new dimensions of the image
        transformed_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                original_pixel = np.array([j, i, 1])
                # transform pixel coordinates
                transformed_pixel = np.dot(Hp, original_pixel)
                transformed_pixel /= transformed_pixel[2]  # normalization

                x, y = int(round(transformed_pixel[0])), int(round(transformed_pixel[1]))
                transformed_img[y, x] = resized_img[i, j]

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # 27 is ESC key
        break
cv.destroyAllWindows()

comp_img = cv.warpPerspective(resized_img, Hp, (new_width, new_height))

plt.figure(figsize=(20, 10))
plt.subplot(1, 3, 1)
plt.title('Distorted Image', fontsize=15)
plt.imshow(cv.cvtColor(resized_img, cv.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(1, 3, 2)
plt.title('Reconstructed Image', fontsize=15)
plt.imshow(cv.cvtColor(transformed_img, cv.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(comp_img, cv.COLOR_BGR2RGB))
plt.title('OpenCV image reconstruction with WarpPerspective', fontsize=15)
plt.axis('off')
plt.show()