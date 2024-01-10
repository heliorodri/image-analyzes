import webbrowser
from google.cloud import vision

import streamlit as st

GOOGLE_API_URL = 'https://maps.google.com/'

def main():
    st.title("Finding places around the world")

    image_url = st.text_input("Enter an image URL or upload a file:", "")
    
    if st.button("Submit") and (image_url is not None):    
        client = vision.ImageAnnotatorClient()

        response = client.annotate_image({
            'image': {'source': {'image_uri': image_url}},
            'features': [],
        })

        if response.landmark_annotations:
            landmark = response.landmark_annotations[0]
            st.info(f'This is: {landmark.description}')

            location = landmark.locations[0]
            lat = location.lat_lng.latitude
            lng = location.lat_lng.longitude
            url = f'{GOOGLE_API_URL}?q={lat},{lng}'

        elif response.web_detection:
            guessed_place = response.web_detection.best_guess_labels[0].label
            st.info(f'This is: {guessed_place}')
            url = f'{GOOGLE_API_URL}?q={guessed_place}'

        else:
            st.error('Sorry, I could not find anything related to this image')
            return

        st.success(f"Opening location on Google Maps: {url}")
        webbrowser.open(url)

if __name__ == "__main__":
    main()