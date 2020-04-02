"""
@name : screenmap_nodisplay.py
@author: Marco Iannella (altair1016)
Module used to convert HTML to PNG
"""

import os
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from file_check import dir_exists

def html2png(filename, png_path):
    """
    Function to html to png. Folium output can only be a html file.
    This function, opens the html file in a browser and makes a screenshot of the displayed browser
    The function has to run on server without a physical display.
    For that reason a virtual display has to be created, to make screenshot possible
    :param filename: html file
    :param png_path: destination path
    :return: the name of the created png file
    """
    # Save the map as an HTML file

    delay = 5
    fn = filename
    output_dir = png_path
    tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
    path = r'{path}/{mapfile}'.format(path=os.getcwd(), mapfile="geckodriver")
    print(path)

    display = Display(visible=0, size=(1366, 768))
    display.start()
    # Open a browser window...
    browser = webdriver.Firefox(executable_path=path)
    # ..that displays the map...
    browser.get(tmpurl)
    # Give the map tiles some time to load
    time.sleep(delay)
    # Grab the screenshot
    dir_exists(output_dir)
    fn = fn.split("/")[-1]
    output_name = output_dir + fn.split(".")[0]+'.png'
    browser.save_screenshot(output_name)
    os.chmod(output_name, 777)
    # Close the browser
    browser.quit()

    return output_name


