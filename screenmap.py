"""
@name : screenmap.py
@author: Marco Iannella (altair1016)
Module used to convert HTML to PNG
"""
import os
import time
from selenium import webdriver
from file_check import dir_exists


def html2png(filename, png_path):
    """
    Function to convert html to png. Folium output can only be a html file.
    This function, opens the html file in a browser and makes a screenshot of the displayed browser
    :param filename: html file
    :param png_path: destination path
    :return: the name of the created png file
    """

    # Save the map as an HTML file
    delay = 5
    print(filename)
    fn = filename
    output_dir = png_path
    tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
    path = r'{path}/{mapfile}'.format(path=os.getcwd(), mapfile="geckodriver")
    print(path)

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


