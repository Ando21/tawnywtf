import os
import boto3
import requests
import os
import time
import random

#Functions

######################################################################################
######################################################################################
######################################################################################

def update_html_pages():
    '''Function to update html files on www.tawny.wtf s3 bucket'''
    print('-------------------------------------------')
    print('Updating html files:')
    print('-------------------------------------------')
    # Access S3
    s3 = boto3.client('s3', region_name='us-east-1',
                         aws_access_key_id=os.environ['aws_access_key'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'])
    # Set directory
    os.chdir('/Users/andyschaul/Dropbox/tawny.wtf')

    # Upload html files only
    for file in ['about.html', 'photos.html', 'blog.html', 'harvardartimages.html', 'index.html']:
        #if file[-4:] == 'html':
        print('Uploading:', file)
        s3.upload_file(Filename=file,
                      Bucket='www.tawny.wtf',
                      Key=file,
                      ExtraArgs={'ContentType': 'text/html'})

######################################################################################
######################################################################################
######################################################################################

def update_image_files():
    '''Function to upload image to s3 images folder'''
    print('-------------------------------------------')
    print('Updating image files:')
    print('-------------------------------------------')
    # Access S3
    s3 = boto3.client('s3', region_name='us-east-1',
                         aws_access_key_id=os.environ['aws_access_key'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'])

    # Set directory
    os.chdir('/Users/andyschaul/Dropbox/tawny.wtf/images')

    # upload jpegs or pngs
    for file in os.listdir():
        print('Uploading:', file)
        # assign correct content type
        if file[-4:] == 'jpeg':
            content_type = 'image/jpeg'
        elif file[-3:] == 'png':
            content_type = 'image/png'
        else:
            content_type = 'image'
        # upload to s3 location
        s3.upload_file(Filename=file,
                       Bucket="www.tawny.wtf",
                       Key="images" + "/" + file,
                       ExtraArgs={'ContentType': content_type})

######################################################################################
######################################################################################
######################################################################################

def update_css_files():
    '''Function to upload css files to s3'''
    print('-------------------------------------------')
    print('Updating CSS files:')
    print('-------------------------------------------')
    # Access S3
    s3 = boto3.client('s3', region_name='us-east-1',
                         aws_access_key_id=os.environ['aws_access_key'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'])

    # Set directory
    os.chdir('/Users/andyschaul/Dropbox/tawny.wtf/styles')

    # Upload html files only
    for file in os.listdir():
        if file[-3:] == 'css':
            print('Uploading:', file)
            s3.upload_file(Filename=file,
                           Bucket="www.tawny.wtf",
                           Key="styles" + "/" + file,
                           ExtraArgs={'ContentType': "text/css"})

######################################################################################
######################################################################################
######################################################################################

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
        <link rel="stylesheet" href="styles/harvardart.css">
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
          <h3>Width: {chosen_image['width']}</h3>
          <h3>Format: {chosen_image['format']}</h3>
          <a href="{chosen_image['baseimageurl']}">
          <img src="{chosen_image['baseimageurl']}" alt="Harvard Art Museum Image" width=chosen_image['width']px height={chosen_image['height']}px>
          <br><br>
      </div>


    </body>
    </html>
    """

    with open('harvardartimages.html', "w") as f:
        f.write(html_string)

######################################################################################
######################################################################################
######################################################################################

def update_s3_website():
    '''Function to upload html, images, and css files to s3'''
    print('-------------------------------------------')
    print('Creating Harvard Art Page')
    print('-------------------------------------------')
    print('Updating html, css, and images on tawny.wtf:')
    print('-------------------------------------------')
    # Create Art pages
    create_art_page()
    # update images files
    update_image_files()
    # update css files
    update_css_files()
    # update html files
    update_html_pages()
