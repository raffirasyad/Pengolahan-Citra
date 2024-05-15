
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

def rgb_to_hsv(image):
    hsv_image = image.convert("HSV")
    return hsv_image.convert("RGB")  # Convert back to RGB for display purposes

def calculate_histogram(image):
    image = np.array(image)
    hist_red, bins_red = np.histogram(image[:, :, 0], bins=256, range=(0, 256))
    hist_green, bins_green = np.histogram(image[:, :, 1], bins=256, range=(0, 256))
    hist_blue, bins_blue = np.histogram(image[:, :, 2], bins=256, range=(0, 256))

    hist_image = Image.new('RGB', (256, 100), (255, 255, 255))
    for x in range(256):
        r = int(hist_red[x] / hist_red.max() * 100)
        g = int(hist_green[x] / hist_green.max() * 100)
        b = int(hist_blue[x] / hist_blue.max() * 100)
        for y in range(r):
            hist_image.putpixel((x, 99 - y), (255, 0, 0))
        for y in range(g):
            hist_image.putpixel((x, 99 - y), (0, 255, 0))
        for y in range(b):
            hist_image.putpixel((x, 99 - y), (0, 0, 255))
    return hist_image

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
st.markdown("""
    <h3>Nama  : Muhammad Raffi Rasyad</h3>
    <h3>Nim   : 312210184</h3>
    <h3>Kelas : TI.22.B1</h3>
    """, unsafe_allow_html=True)

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
        hist_image = calculate_histogram(image)
        st.image(hist_image, caption='Histogram', use_column_width=True)

    brightness = st.slider('Brightness', 0.5, 2.0, 1.0)
    contrast = st.slider('Contrast', 0.5, 2.0, 1.0)

    if st.button("Apply Brightness & Contrast"):
        adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
        st.image(adjusted_image, caption='Adjusted Image', use_column_width=True)

    if st.button("Detect Contours"):
        contour_image = detect_contours(image)
        st.image(contour_image, caption='Contour Image', use_column_width=True)
