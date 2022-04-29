""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
"""
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path
import sqlite3
import os
import json
import ctypes
import requests

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dictt = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = apod_info_dictt[apod_date]
    image_msg = download_apod_image(image_url)
    image_sha256 = sha256(image_msg.content).hexdigest()
    image_size = len(image_msg.content)
    image_path = get_image_path(image_url, image_dir_path)

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
      
    #os.path checks that the directory exist
    dir_path= os.path.join('NASA Images')
   # makes a directory named image whether or not the image is downloaded.
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """ 
    apod_date = datetime.today().strftime('%Y-%m-%d')
     
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            apod_date = datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    image_path = get_image_dir_path["title"]+".png"
    
    return "TODO"

def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """   
    Image_url = ("https://api.nasa.gov/planetary/apod?api_key=yUk0bektwbRHmGt3rsaA023MSJ5yCddkKmcAFN1U")
    apod_info = requests.get(Image_url, params={"date":datetime.today().strftime('%Y-%m-%d')})
    if apod_info.status_code == 200:
        try: 
            print("Succesfull to get info...")
            body = apod_info.content
            body = json.loads(body)
            return body
        except:
            return None

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """ 
    print(image_url)
    print(image_path) 
    print(image_size + image_sha256)
     
    return #TODO

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    if os.path.isfile(path):
            return path

    resp_msg = requests.get(image_url)
    if resp_msg.status_code == 200:
        try:
            # getting response of image 
            img_data = resp_msg.content
            # here open returns an object of image path
            with open(path, 'wb') as fp:
                fp.write(img_data)
                return path
        except:
                return
       

    

def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    with open(image_path, 'wb') as fp:
        print("Save image")
        fp.write(image_msg)
    return #

def create_image_db(db_path):
    myConnection = sqlite3.connect('Image_Database.db')


    myCursor = myConnection.cursor()

#Let's define the SQL Query we will use to create our first table:
    createImageTable = """ CREATE TABLE IF NOT EXISTS people (
                          Date text NOT NULL,
                          Time text NOT NULL
                        
                        );"""

    myCursor.execute(createImageTable)


    myConnection.commit()


    myConnection.close()                     
    #return #TODO

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    myConnection = sqlite3.connect('Image_Database.db')


    myCursor = myConnection.cursor()

    db_Query = """INSERT INTO people ( 
                      Date, 
                      Time)
                      VALUES (?, ?)"""
    db = ("apod_data",
                      
          datetime.now(), 
            
          None)       
          
    myCursor.execute(db_Query, db)


    myCursor.execute("SELECT group_concat(name, ', ') FROM pragma_table_info('people')")
    print(myCursor.fetchone())


    myConnection.commit()


    myConnection.close()              
    return #TODO

    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """


def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    db_cxn = sqlite3.connect(db_path)
    db_cursor = db_cxn.cursor()

    db_cursor.execute("select if FROM Images")
    query_results = db_cursor.fetchall()
    db_cxn.close()


    if len(query_results) > 0:
        print("Image is already in cache")
        return True 
    else:
        print("New img not in cache")
        return False

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    except:
        print("Eroor setting dsktp bckgrnd img")


    return #TODO

main()