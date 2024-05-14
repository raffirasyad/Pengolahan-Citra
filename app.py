import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import matplotlib.pyplot as plt

def rgb_to_hsv(image):
    return image.convert("HSV")

def calculate_histogram(image):
    image = np.array(image)
    color = ('r', 'g', 'b')
    plt.figure()
    for i, col in enumerate(color):
        histr, bin_edges = np.histogram(image[:, :, i], bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histr, color=col)
    plt.title('Histogram')
    plt.xlabel('Pixel value')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def adjust_brightness_contrast(image, brightness=1.0, contrast=1.0):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    return image

def detect_contours(image):
    gray = image.convert("L")
    blurred = gray.filter(ImageFilter.GaussianBlur(5))
    edges = blurred.filter(ImageFilter.FIND_EDGES)
    contour_img = image.copy()
    contour_img.paste(edges, mask=edges)
    return contour_img

st.title("Image Manipulation Web App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    if st.button("Convert RGB to HSV"):
        hsv_image = rgb_to_hsv(image)
        st.image(hsv_image, caption='HSV Image', use_column_width=True)

    if st.button("Calculate Histogram"):
        st.write("Histogram")
        calculate_histogram(image)

    brightness = st.slider('Brightness', 0.0, 2.0, 1.0)
    contrast = st.slider('Contrast', 0.0, 2.0, 1.0)

    if st.button("Apply Brightness & Contrast"):
        adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
        st.image(adjusted_image, caption='Adjusted Image', use_column_width=True)

    if st.button("Detect Contours"):
        contour_image = detect_contours(image)
        st.image(contour_image, caption='Contour Image', use_column_width=True)
