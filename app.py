import streamlit as st
import cv2
import numpy as np


st.title("Pengolahan Citra Digital")

uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

def save_image_as_png(image):
    _, buffer = cv2.imencode('.png', img=image)
    return buffer.tobytes()

if uploaded_file is not None:
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

    # Create two columns
    col1, col2 = st.columns(2)
    kol1, kol2, kol3 = st.columns(3)

    # Show original image in the first column
    with col1:
        st.image(image, caption="Before (Original)", use_column_width=True, channels="BGR")

    edited_image = image.copy()

    # Tombol reset
    if st.button('Reset'):
        st.session_state.brightness_contrast = False
        st.session_state.grayscale = False
        st.session_state.negative = False
        st.session_state.blur = False
        st.session_state.sharpen = False
        st.session_state.letter = False
        edited_image = image.copy()

    if st.checkbox('Brightness/Contrast', key='brightness_contrast'):
        brightness = st.slider("Brightness", -100, 100, 0, key="brightness")
        contrast = st.slider("Contrast", -100, 100, 0, key="contrast")
        edited_image = cv2.convertScaleAbs(edited_image, alpha=(contrast/127.0 + 1), beta=brightness)
        # rumus 
        # dst(i,j)=saturate_cast<uchar>(α⋅src(i,j)+β)

    if st.checkbox('Black-White Effect', key = 'grayscale'):
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_BGR2GRAY)
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_GRAY2BGR)

    if st.checkbox('Negative Effect', key='negative'):
        edited_image = 255 - edited_image

    if st.checkbox('Blur (Gaussian)', key='blur'):
        kernel = st.slider('Kernel', min_value=1, max_value=35, step=2, value=15, key='blur_kernel')
        sigma = st.slider('Sigma', min_value=0, max_value=15, step=1, value=7, key='blur_sigma')
        edited_image = cv2.GaussianBlur(edited_image, (kernel, kernel), sigmaX=sigma, sigmaY=sigma)
    

    if st.checkbox('Pixelate Image'):
        pixel_size = st.slider('Pixelation Level', 1, 50, 10)
        h, w = edited_image.shape[:2]
        temp = cv2.resize(edited_image, (51-pixel_size, 51-pixel_size), interpolation=cv2.INTER_LINEAR)
        edited_image = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        # with kol1:
        #     st.write(image)
        # with kol2:  
        #     st.write(temp)
        # with kol3:
        #     st.write(edited_image)
        # st.write(50-pixel_size)
        # st.write(edited_image.shape)
        # st.write(h)
        # st.write(w)


    # Show edited image in the second column
    with col2:
        st.image(edited_image, caption="After", use_column_width=True, channels="BGR")

    download_button = st.download_button(
        label='Download your image.',
        data=save_image_as_png(image=edited_image),
        file_name='image.png',
        key='download'
    )
