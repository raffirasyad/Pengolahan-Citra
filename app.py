import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def rgb_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

def calculate_histogram(image):
    color = ('b','g','r')
    plt.figure()
    for i, col in enumerate(color):
        histr = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title('Histogram')
    plt.xlabel('Pixel value')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    brightness = int((brightness - 50) * 2.55)  # Convert to range -255 to 255
    contrast = int((contrast - 50) * 2.55)      # Convert to range -127 to 127
    B = brightness / 255.0
    c = contrast / 127.0
    k = np.tan((45 + 44 * c) / 180 * np.pi)

    img = (image - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
    img = np.clip(img, 0, 255).astype(np.uint8)
    return img

def detect_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = image.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    return contour_img

st.title("Image Manipulation Web App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file))
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    if st.button("Convert RGB to HSV"):
        hsv_image = rgb_to_hsv(image)
        st.image(hsv_image, caption='HSV Image', use_column_width=True)

    if st.button("Calculate Histogram"):
        st.write("Histogram")
        calculate_histogram(image)

    brightness = st.slider('Brightness', 0, 100, 50)
    contrast = st.slider('Contrast', 0, 100, 50)

    if st.button("Apply Brightness & Contrast"):
        adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
        st.image(adjusted_image, caption='Adjusted Image', use_column_width=True)

    if st.button("Detect Contours"):
        contour_image = detect_contours(image)
        st.image(contour_image, caption='Contour Image', use_column_width=True)
