from PIL import Image
import streamlit as st

import json
import re
import webbrowser
from google.cloud import vision

GOOGLE_API_URL = 'https://maps.google.com/'

def build_request_body(image_url, file):
  if image_url is not None: 
    return {
      'image': {'source': {'image_uri': image_url}},
      'features': [{'type_': vision.Feature.Type.LANDMARK_DETECTION}],
    }
  else:
    return {
      'image': {'source': {'image_uri': image_url}},
      'features': [{'type_': vision.Feature.Type.LANDMARK_DETECTION}],
    }
    

def main():
  st.title("Finding places around the world")

  image_url = st.text_input("Enter an image URL or upload a file:", "")
  uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
  
  if st.button("Submit") and (image_url is not None):    
      # content =  uploaded_file.read()
      # print(f'content: {content}')
      
      client = vision.ImageAnnotatorClient()
      response = client.annotate_image({
        'image': {'source': {'image_uri': image_url}},
        'features': [
          # {'type_': vision.Feature.Type.LANDMARK_DETECTION}, 
          # {'type_': vision.Feature.Type.TYPE_UNSPECIFIED}
        ],
      })

      print('-------')
      print(response)

      print(f'response.landmark_annotations: {response.landmark_annotations}')
      
      if response.landmark_annotations:
        print('passando na landmark')
        landmark = response.landmark_annotations[0]
        st.info(f'this is: {landmark.description}')

        location = landmark.locations[0]
        lat = location.lat_lng.latitude
        lng = location.lat_lng.longitude
        
        url = f'{GOOGLE_API_URL}?q={lat},{lng}'
        
      elif response.web_detection:
        print('passando no guessed place')
        guessed_place = response.web_detection.best_guess_labels[0].label
        st.info(f'this is: {guessed_place}')
        url = f'{GOOGLE_API_URL}?q={guessed_place}'
        
      else:
        st.error('Sorry, I could not find anything related to this image')
        return

      webbrowser.open(url)
      

      

if __name__ == "__main__":
    main()