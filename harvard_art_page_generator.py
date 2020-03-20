# Imports
import requests
import os
import time
import random

# Get the necessary data to generate the HTML page
def create_art_page():
    '''
    Script to load a random image from the Harvard Art Museums in your browser
    and generate an HTML page
    '''
    # Set up
    # Load API key from environment
    # Request API key here: https://docs.google.com/forms/d/e/1FAIpQLSfkmEBqH76HLMMiCC-GPPnhcvHC9aJS86E32dOd0Z8MpY2rvQ/viewform
    key = os.environ['harvard_art_api_key']
    base_url = 'https://api.harvardartmuseums.org/image'

    # Parameters
    payload = {'apikey': key}

    # Get total pages to choose a random one to query
    r = requests.get(base_url, params=payload)
    pages = r.json()
    pages = pages['info']['pages']
    time.sleep(.5)

    # Choose a random page of results
    random_page = random.randint(1, pages)

    # Update payload parameters with random page number
    payload['page'] = random_page

    # Get images for that page
    images = requests.get(base_url, params=payload)
    images = images.json()
    images = images['records']

    # Choose random image from list of images
    chosen_image = random.choice(images)
    print(chosen_image)

    # Create the HTML

    html_string = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="twitter:card" content="summary"></meta>
        <meta name="twitter:creator" content="@andyschaul"></meta>
        <meta name="twitter:title" content="Harvard Art Museum Image"></meta>
        <meta name="twitter:image" content="{chosen_image['baseimageurl']}"></meta>
        <title>Harvard Art Images</title>
        <link rel="stylesheet" href="harvardart.css">
    </head>
    <body>
      <h1>Here is a random photo from the Harvard Art Museums Collection:</h1>
      <h2> This page will update daily with a new image</h2><br>
      <div>
          <p1>Today's Image:</p1>
          <h3>Copyright: {chosen_image['copyright']}</h3>
          <h3>Date: {chosen_image['date']}</h3>
          <h3>ImageID: {chosen_image['imageid']}</h3>
          <h3>Height: {chosen_image['height']}</h3>
          <h3>Width: {chosen_image['weight']}</h3>
          <h3>Format: {chosen_image['format']}</h3>
          <a href="{chosen_image['baseimageurl']}">
          <img src="{chosen_image['baseimageurl']}" alt="Harvard Art Museum Image" width=1024px height=400px>
          <br><br>
      </div>


    </body>
    </html>
    """

    with open('harvardartimages.html', "w") as f:
        f.write(html_string)

create_art_page()
