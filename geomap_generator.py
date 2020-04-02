"""
@name : geomap_generator.py
@author: Marco Iannella (altair1016)
Module for map drawing
"""
import urllib.request
import datetime
import sys
import json
import folium as fl
import screenmap as sm
from file_check import dir_exists, file_exists



FILE = 'geojson_data/ita_geo.geojson'
DATE = (str(datetime.datetime.now())[0:10].replace("-", ""))
FILE_OUT = [str(DATE) + "_heatmap_global", str(DATE)+"_heatmap_district"]
#COLOR: [Line, fill]
COLOR = {"red":["#AF0000", "#F55D3D"],
         "orange": ["#FF9300", "#FDBA5F"],
         "yellow": ["#FFE421", "#FFF18A"]}


def draw_circle(map, flag='NULL'):
    """
    Function to draw circles on the whole map.
    Each circle stand for the contamination
    number for each district
    :param map: whole map
    :param flag: flag for region / district
    :return: updated map
    """
    if flag == 'd':
        actual_region_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19" \
                          "/master/dati-json/dpc-covid19-ita-province-latest.json"
        CONSTANT = 430 * 1.5
    else:
        actual_region_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19" \
                            "/master/dati-json/dpc-covid19-ita-regioni-latest.json"
        CONSTANT = 300

    actual_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19" \
                 "/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"

    with urllib.request.urlopen(actual_url) as url:
        result_json = json.loads(url.read().decode())
    with urllib.request.urlopen(actual_region_url) as url2:
        result_region_json = json.loads(url2.read().decode())

    total = result_json[-1]["totale_positivi"] - \
            result_json[-1]["dimessi_guariti"] - \
            result_json[-1]["deceduti"]
    for elt in result_region_json:
        if flag == 'd':
            partial = elt["totale_casi"]
        else:
            partial = elt["totale_positivi"] - elt["dimessi_guariti"] - elt["deceduti"]

        circle_radius = (partial / total) * CONSTANT
        if circle_radius > 0 and circle_radius <= CONSTANT/20:
            color = COLOR["yellow"]
        elif circle_radius > CONSTANT/20 and circle_radius <= CONSTANT/9:
            color = COLOR["orange"]
        elif circle_radius > CONSTANT/9:
            color = COLOR["red"]

        fl.CircleMarker(
            location=[elt["lat"], elt["long"]],
            radius=circle_radius,
            popup=elt['denominazione_regione'],
            color=color[0],
            fill=True,
            fill_color=color[1]
        ).add_to(map)
    return map

def map_generator(flag='NULL'):
    """
    Function that generates the final map.
    :param flag: "d" for district, null for region
    :return: name of the final png file
    """

    dest_path = "figures/heatmap/html/"
    png_path = "figures/heatmap/png/global/"
    if flag == "d":
        png_path = "figures/heatmap/png/district/"
    new_fileout = "TEST"
    dir_exists(dest_path)
    dir_exists(png_path)
    try:

        if flag == 'd':
            file = file_exists(png_path)
            if file != "None":
                return png_path + FILE_OUT[1]+".png"
            raise FileNotFoundError
        elif flag == 'NULL':
            file = file_exists(png_path)
            if file != "None":
                return png_path + FILE_OUT[0] + ".png"
            raise FileNotFoundError

    except FileNotFoundError:
        with open(FILE) as data_file:
            data = json.load(data_file)
        map = fl.Map([41.6252978589571, 12.34580993652344], zoom_start=6, control_scale=True)
        fl.GeoJson(data).add_to(map)
        map = draw_circle(map, flag)
        fileout = dest_path + FILE_OUT[0] + ".html"
        if flag == 'd':
            fileout = dest_path + FILE_OUT[1]+".html"
        map.save(fileout)
        print(fileout, png_path)
        new_fileout = sm.html2png(fileout, png_path)
    return new_fileout

if __name__ == '__main__':
    """
    This script cannot be used inside the flask app, 
    due to a conflict between flask and folium modules.
    For that reason has to be executed in a separated session.
    """
    # did that because folium was in conflict with python flask module
    INPUT_VAL = sys.argv
    if len(INPUT_VAL) > 1:
        map_generator(INPUT_VAL[1])
    else:
        map_generator()
