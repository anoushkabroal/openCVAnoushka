import cv2
import numpy as np
import os #for saving the file
import streamlit as st

img = cv2.imread("C:\\Users\\gaurav\\Desktop\\IMG_6160.jpg")

cv2.imshow("Display window", img)
# convert the image to grayscale format (black and white and gray image)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply binary thresholding
ret, threshImg = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

#show image
cv2.imshow('Binary image', threshImg)
cv2.destroyAllWindows()


#channel is grayscale image made up of only one of the primary colors specified (transparent in this case)
alpha_channel = np.ones(threshImg.shape, dtype=threshImg.dtype) * 255
#np.ones gives array with shape and type of all pixels in threshImage

# Set all pixels that I made 255 to have 0 alpha value
alpha_channel[threshImg == 255] = 0

# Merge the thresholded image and the alpha channel array to get transparent background
result_image = cv2.merge((threshImg, alpha_channel))
#gave it an alpha layer basically

# Convert the thresholded image to have 4 channels (RGBA)
result_image = cv2.cvtColor(threshImg, cv2.COLOR_GRAY2RGBA)

# Set the alpha channel in the result image
result_image[:, :, 3] = alpha_channel
#3 is index for alpha channel

# Save/display result
path = 'C:\\Users\\gaurav\\Desktop\\openCVSaving'
cv2.imwrite(os.path.join(path , 'result_image.png'), result_image)
cv2.imshow('Result Image', result_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

def change_pen_color(s, result_image1):
    black_pixels = (result_image1[:, :, 0] == 0) & (result_image1[:, :, 1] == 0) & (result_image1[:, :, 2] == 0)
    #BGR NOT RGB!!!
    if (s == "Red"):
        result_image1[black_pixels, 0] = 255
        result_image1[black_pixels, 1] = 0
        result_image1[black_pixels, 2] = 0
    elif (s == "Blue"):
        result_image1[black_pixels, 0] = 0
        result_image1[black_pixels, 1] = 0
        result_image1[black_pixels, 2] = 255
    elif (s == "Green"):
        result_image1[black_pixels, 0] = 0
        result_image1[black_pixels, 1] = 255
        result_image1[black_pixels, 2] = 0
    elif (s == "Black"):
        result_image1[black_pixels, 0] = 0
        result_image1[black_pixels, 1] = 0
        result_image1[black_pixels, 2] = 0

    return result_image1

def save_To(saveVal, the_image):
    path = saveVal.replace("\"","\'")
    path2 = rf"{path}"
    if not os.path.isdir(path2):
        st.write("Please enter a valid folder path. (Without quotations)")
        st.write(path2)
    else:
        cv2.imwrite(os.path.join(path2, 'streamLit_image.png'), the_image)
        st.write(path2)
        st.success(f"Image saved successfully")
       # path = rf"{saveVal}" #make a raw string
        #path2 = path.replace("\"","\'")
        #cv2.imwrite(os.path.join(path , 'streamLit_image.png'), the_image)
        #st.write("Image saved successfully")

st.title("Welcome to the Signature Editor!")
mainImage = st.image(result_image)

col1, col2, = st.columns(2)
with col1:
    color = st.radio(
        "Choose a pen color",
        ["Red", "Blue", "Green", "Black"])

    if color == 'Red':
        st.write('You selected red.')
        mainImage.image(change_pen_color("Red", result_image))
    if color == "Blue":
        st.write('You selected blue.')
        mainImage.image(change_pen_color("Blue", result_image))
    if color == "Green":
        st.write('You selected green.')
        mainImage.image(change_pen_color("Green", result_image))
    if color == "Black":
        st.write('You selected black.')
        mainImage.image(change_pen_color("Black", result_image))
with col2:
    saveVal = st.text_input("Input Path Location to Save: ")
    if st.button('Apply'):
        if(saveVal):
            imageToSave = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            #changing alpha when saving again
            alpha_channel2 = np.ones((imageToSave.shape[0], imageToSave.shape[1]), dtype=np.uint8) * 255
            finalImageToSave = cv2.merge([imageToSave, alpha_channel])
            save_To(saveVal, finalImageToSave)
        else:
            st.write("No value was specified. Try again")






