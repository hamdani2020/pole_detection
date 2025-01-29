import logging
import os
from io import BytesIO
from pathlib import Path

import cv2
import folium
import numpy as np
import piexif
import streamlit as st
from PIL import ExifTags, Image
from streamlit_folium import st_folium
from ultralytics import YOLO

from sample_utils.download import download_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Pole Detection App",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load logo
logo = "./imgs/logo.jpg"
st.sidebar.image(logo)

# Paths to models
HERE = Path(__file__).parent
ROOT = HERE.parent
MODEL_URL = (
    "https://raw.githubusercontent.com/Jubilio/pole_detection/main/models/best.pt"
)
MODEL_LOCAL_PATH = ROOT / "models" / "pole.pt"

# Ensure the models directory exists
os.makedirs(ROOT / "models", exist_ok=True)


# Download file with logging
def download_file_with_logging(url, local_path, expected_size):
    logger.info(f"Downloading file from {url} to {local_path}")
    download_file(url, local_path, expected_size)
    logger.info(f"Download complete. File saved to {local_path}")


# Load model with caching
@st.cache_resource()
def load_model():
    logger.info("Entering load_model function")
    if not MODEL_LOCAL_PATH.exists():
        logger.info(f"Model not found at {MODEL_LOCAL_PATH}. Downloading...")
        download_file_with_logging(MODEL_URL, MODEL_LOCAL_PATH, expected_size=89569358)
    else:
        logger.info(f"Model found at {MODEL_LOCAL_PATH}")
    logger.info("Loading YOLO model")
    model = YOLO(MODEL_LOCAL_PATH)
    logger.info("YOLO model loaded successfully")
    return model


# Load the model
logger.info("About to load the model")
net = load_model()
logger.info("Model loading complete")

# Tension Classes
CLASSES = ["low_tension", "medium_tension", "high_tension"]

# Title and introduction
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>Pole Detection App</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style='text-align: center;'>
        Upload an image to detect Pole Tension and view their location on a map.
    </div>
""",
    unsafe_allow_html=True,
)
# Sidebar settings
st.sidebar.title("Settings")
st.sidebar.markdown("Upload images and adjust the confidence threshold below.")
uploaded_files = st.sidebar.file_uploader(
    "Upload Images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True
)
score_threshold = st.sidebar.slider(
    "Confidence Threshold", min_value=0.0, max_value=1.0, value=0.1, step=0.05
)

# Reset button
if st.sidebar.button("Reset App"):
    st.session_state.clear()
    st.rerun()


# Function to correct image orientation
def correct_image_orientation(image):
    try:
        exif = image._getexif()
        if exif is not None:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif_orientation = exif.get(orientation)
            if exif_orientation == 3:
                image = image.rotate(180, expand=True)
            elif exif_orientation == 6:
                image = image.rotate(270, expand=True)
            elif exif_orientation == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        logger.error(f"Error correcting image orientation: {e}")
    return image


# Extract GPS info
def extract_gps_info(image_file):
    try:
        image = Image.open(image_file)
        if "exif" in image.info:
            exif_data = piexif.load(image.info["exif"])
            gps_data = exif_data.get("GPS", {})
            if (
                piexif.GPSIFD.GPSLatitude in gps_data
                and piexif.GPSIFD.GPSLongitude in gps_data
            ):
                lat = gps_data[piexif.GPSIFD.GPSLatitude]
                lat_ref = gps_data[piexif.GPSIFD.GPSLatitudeRef]
                long = gps_data[piexif.GPSIFD.GPSLongitude]
                long_ref = gps_data[piexif.GPSIFD.GPSLongitudeRef]

                # Convert latitude to decimal degree
                lat_dec = (
                    float(lat[0][0]) / float(lat[0][1])
                    + (float(lat[1][0]) / float(lat[1][1])) / 60
                    + (float(lat[2][0]) / float(lat[2][1])) / 3600
                )
                if lat_ref == b"S":
                    lat_dec = -lat_dec

                # Convert longitude to decimal degree
                long_dec = (
                    float(long[0][0]) / float(long[0][1])
                    + (float(long[1][0]) / float(long[1][1])) / 60
                    + (float(long[2][0]) / float(long[2][1])) / 3600
                )
                if long_ref == b"W":
                    long_dec = -long_dec

                return lat_dec, long_dec
            else:
                logger.warning(f"No GPS information found in image: {image_file.name}")
                return None, None
        else:
            logger.warning(f"No EXIF data found in image: {image_file.name}")
            return None, None
    except Exception as e:
        logger.error(f"Error extracting GPS info from {image_file.name}: {str(e)}")
        return None, None


# Process image
def process_image(image_file):
    logger.info(f"Processing image: {image_file.name}")
    image = Image.open(image_file)
    image = correct_image_orientation(image)

    # Extract GPS coordinates
    lat, lon = extract_gps_info(image_file)

    _image = np.array(image)
    h_ori, w_ori = _image.shape[:2]
    image_resized = cv2.resize(_image, (720, 640), interpolation=cv2.INTER_AREA)

    results = net.predict(image_resized, conf=score_threshold)
    annotated_frame = results[0].plot()
    image_pred = cv2.resize(
        annotated_frame, (w_ori, h_ori), interpolation=cv2.INTER_AREA
    )

    return _image, image_pred, lat, lon


# Create map with detected poles
def create_map(coordinates):
    m = folium.Map(location=[0, 0], zoom_start=2)

    for i, (lat, lon) in enumerate(coordinates):
        if lat is not None and lon is not None:
            icon = folium.Icon(color="red", icon="tower", prefix="fa")
            folium.Marker([lat, lon], popup=f"Pole {i+1}", icon=icon).add_to(m)

    return m


# Welcome message
if not uploaded_files:
    st.write("## Welcome to the Pole Detection App!")
    st.write("""
    This app detects poles in images and displays their locations on a map. 
    To get started:
    1. Upload one or more images using the file uploader in the sidebar.
    2. Adjust the confidence threshold if needed.
    3. View the results and download the predicted images.
    """)

# Process images and display results
if uploaded_files:
    progress_bar = st.progress(0)
    total_files = len(uploaded_files)
    all_coordinates = []

    for i, image_file in enumerate(uploaded_files):
        st.write(f"### Processing: {image_file.name}")
        original_image, predicted_image, lat, lon = process_image(image_file)
        all_coordinates.append((lat, lon))

        # Update progress bar
        progress_bar.progress((i + 1) / total_files)

        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Original Image")
            st.image(original_image)
        with col2:
            st.write("#### Predictions")
            st.image(predicted_image)

        # Download button
        buffer = BytesIO()
        download_image = Image.fromarray(predicted_image)
        download_image.save(buffer, format="PNG")
        download_image_byte = buffer.getvalue()
        st.download_button(
            label="Download Predicted Image",
            data=download_image_byte,
            file_name=f"Predicted_{image_file.name}",
            mime="image/png",
        )

        # Correct class selection
        correct_class = st.selectbox(
            "Correct Class (if wrong)",
            CLASSES + ["No Change"],
            index=3,
            key=f"class_{i}",
        )

        if correct_class != "No Change":
            save_corrected_data(
                Image.fromarray(predicted_image), correct_class, image_file
            )
            st.write(f"Saved corrected image as {correct_class}")

        if lat is not None and lon is not None:
            st.write(f"GPS Coordinates: Latitude {lat:.6f}, Longitude {lon:.6f}")
        else:
            st.write("No GPS coordinates found in the image metadata.")

    # Map display with toggle
    st.write("### Map of Detected Poles")
    show_map = st.checkbox("Show Map", value=True)
    if show_map:
        map = create_map(all_coordinates)
        st_folium(map, width=1200, height=600)

# Footer
st.markdown("---")
st.markdown("""
    **Pole Detection App**  
    Built with Streamlit, YOLO, and Folium.  
    Developed by DATA4MOZ 
""")

