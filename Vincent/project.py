import streamlit as st
import cv2
import numpy as np

import funEdit


uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

def save_image_as_png(image): # Ngolah citra untuk di download
    _, buffer = cv2.imencode('.png', img=image)
    return buffer.tobytes()



if uploaded_file is not None:
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

    col1, col2 = st.columns(2)

    # Foto Original
    with col1:
        st.image(image, caption="Original Photo", use_column_width=True, channels="BGR")

    edited_image = image.copy()

    # Tombol reset
    if st.button('Reset'):
        st.session_state.brightness_contrast = False
        st.session_state.grayscale = False
        st.session_state.negative = False
        st.session_state.blur = False
        st.session_state.sharpen = False
        st.session_state.mosaic = False
        edited_image = image.copy()

    # Buttons Efek
    if st.checkbox('Brightness/Contrast', key='brightness_contrast'):
        brightness = st.slider("Brightness", -100, 100, 0, key="brightness")
        contrast = st.slider("Contrast", -100, 100, 0, key="contrast")
        edited_image = funEdit.adjust_brightness_contrast(edited_image, brightness, contrast)

    if st.checkbox('Grayscale', key='grayscale'):
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_BGR2GRAY)
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_GRAY2BGR)
    
    # Pilih yang dibawah

    if st.checkbox('Negative Effect', key='negative'):
        st.write(edited_image)
        edited_image = 255 - edited_image
        st.write(edited_image)

    if st.checkbox('Blur (Gaussian)', key='blur'):
        kernel = st.slider('Kernel', min_value=1, max_value=35, step=2, value=15, key='blur_kernel')
        sigma = st.slider('Sigma', min_value=0, max_value=15, step=1, value=7, key='blur_sigma')
        edited_image = cv2.GaussianBlur(edited_image, (kernel, kernel), sigmaX=sigma, sigmaY=sigma)

    if st.checkbox('Sharpen', key='sharpen'):
        ksize = st.slider('ksize', min_value=1, max_value=25, step=2, value=1, key='sharpen_ksize')
        sigma = st.slider('sigma', min_value=5, max_value=15, step=5, value=5, key='sharpen_sigma')
        b_image = cv2.GaussianBlur(edited_image, ksize=(ksize, ksize), sigmaX=sigma, sigmaY=sigma)
        effect = st.radio('Effect', options=['Strong', 'Normal', 'Low'], key='sharpen_effect')
        if effect == 'Strong':
            edited_image = cv2.addWeighted(src1=edited_image, alpha=2.5, src2=b_image, beta=-1.5, gamma=0)
        elif effect == 'Normal':
            edited_image = cv2.addWeighted(src1=edited_image, alpha=2, src2=b_image, beta=-1, gamma=0)
        elif effect == 'Low':
            edited_image = cv2.addWeighted(src1=edited_image, alpha=1.5, src2=b_image, beta=-0.5, gamma=0)

    if st.checkbox('Mosaic Effect', key='mosaic'):
        level = st.slider('Level', min_value=1, max_value=35, step=2, value=15, key='mosaic_level')
        h = int(edited_image.shape[0] / level)
        w = int(edited_image.shape[1] / level)
        edited_image = cv2.resize(edited_image, (w, h), interpolation=cv2.INTER_LINEAR)
        edited_image = cv2.resize(edited_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Foto after
    with col2:
        st.image(edited_image, caption="Result", use_column_width=True, channels="BGR")


    download_button = st.download_button(
        label='Download Result',
        data=save_image_as_png(image=edited_image),
        file_name='image.png',
        key='download'
    )


    