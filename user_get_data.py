"""
@name : user_get_data.py
@author: Marco Iannella (altair1016)
Module to help user getting data
"""

import logging
import urllib.request
import json
import matplotlib.pyplot as plt
import region_district_check as rdc
import file_check as fc

NOTIN_LABEL = ('stato', 'lat', 'long', 'note_it', 'note_en')

class UserGetData:
    """
    Get and prepare data for final user
    """
    def __init__(self):
        self.actual_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/" \
                          "dati-json/dpc-covid19-ita-andamento-nazionale.json"
        self.actual_region_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/" \
                                 "dati-json/dpc-covid19-ita-regioni-latest.json"
        self.actual_district_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/" \
                                   "dati-json/dpc-covid19-ita-province-latest.json"

        with urllib.request.urlopen(self.actual_url) as url:
            self.result_json = json.loads(url.read().decode())
        with urllib.request.urlopen(self.actual_region_url) as url2:
            self.result_region_json = json.loads(url2.read().decode())
        with urllib.request.urlopen(self.actual_district_url) as url3:
            self.result_district_json = json.loads(url3.read().decode())

        self.figure_path = "figures/"

        self.logger = logging.getLogger('covid_application.UserGetDataClass')
        self.logger.info('creating an instance of UserGetDataClass')

    def get_user_get_data_path(self):
        """
        Getter method for files path
        :return: path
        """
        return self.figure_path

    def get_today_bulletin(self):
        """
        Get today's bulletin and makes data human-readable
        :return: string containing output message details
        """

        today_dic = self.result_json[-1]
        out_message = ""
        for key in today_dic.keys():
            if str(key).lower() == 'data':
                out_message += str.capitalize((key)) + ": " + \
                               str(today_dic[key]).replace("_", " ")[0:10] + "\n"
            elif str(key).lower() != 'stato':
                out_message += str.capitalize((key)).replace("_", " ") + ": "+ \
                               str(today_dic[key]) + "\n"
        return "\n" + out_message


    def get_whole_bulletin_perc_trend(self):
        """
        Get today's bulletin and makes trend (style1) with data
        :return: name of the generated file
        """
        path = self.figure_path + "whole_bulletin_perc_trend"
        fname = fc.file_naming_rules(path, self.result_json[-1]["data"])
        try:
            returned_value = fc.file_exists(path)
            if returned_value[0:8] in fname:
                raise FileExistsError

            self.logger.info('creating a whole_bulletin_perc_trend plot')
            days = []
            results = []

            for elt in self.result_json:
                days.append(elt["data"][5:10])
                values = (elt["totale_casi"] / elt["tamponi"]) * 100
                results.append(values)
            plt.clf()
            plt.plot(days, results, 'b-+', label="Casi Positivi")
            plt.title('Trend Espansione COVID-19 in Italia')
            plt.xlabel('Giorni')
            plt.xticks(days, days, rotation='vertical')
            plt.ylabel('Casi positivi %')
            plt.grid(color='gray', linestyle='-', linewidth=0.2)
            plt.legend()
            plt.savefig(fname, dpi=None, edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1)
        except FileExistsError:
            self.logger.warning('whole_bulletin_perc_trend plot already exists')
            return path + "/" + returned_value

        return fname


    def get_whole_bulletin_trend(self):
        """
        Get today's bulletin and makes trend style(2) with data
        :return: name of the generated file
        """
        path = self.figure_path+"whole_bulletin_trend"
        fname = fc.file_naming_rules(path, self.result_json[-1]["data"])
        try:
            returned_value = fc.file_exists(path)
            if returned_value[0:8] in fname:
                raise FileExistsError
            self.logger.info('creating a whole_bulletin_trend plot')
            days = []
            results_positivi = []
            results_guariti = []
            results_new_positivi = []
            results_deceduti = []


            for elt in self.result_json:
                days.append(elt["data"][5:10])
                results_positivi.append(elt["totale_positivi"])
                results_new_positivi.append(elt["nuovi_positivi"])
                results_deceduti.append(elt["deceduti"])
                results_guariti.append(elt["dimessi_guariti"])

            plt.clf()
            plt.plot(days, results_positivi, 'b-+', label="Casi Positivi")
            plt.plot(days, results_new_positivi, 'y-+', label="Nuovi casi positivi")
            plt.plot(days, results_deceduti, 'r-+', label="Decessi")
            plt.plot(days, results_guariti, 'g-+', label="Guarigioni")
            plt.grid(color='gray', linestyle='-', linewidth=0.2)
            plt.title('Trend globale COVID-19 in Italia')
            plt.xlabel('Giorni')
            plt.xticks(days, days, rotation='vertical')
            plt.ylabel('Casi')
            plt.legend()
            plt.savefig(fname, dpi=None, edgecolor='w', orientation='portrait',
                        papertype=None, format=None, transparent=False,
                        bbox_inches=None, pad_inches=0.1)
        except FileExistsError:
            self.logger.warning('whole_bulletin_trend plot already exists')
            return path + "/" + returned_value

        return fname

    def get_generic_bulletin_trend(self, flag, json_label, legend_label, color):
        """
        Get whole bulletin and makes trend (style1) with data
        :return: name of the generated file
        """
        path = self.figure_path + json_label+"_bulletin_trend"
        fname = fc.file_naming_rules(path, self.result_json[-1]["data"])
        try:
            returned_value = fc.file_exists(path)
            if returned_value[0:8] in fname:
                raise FileExistsError

            self.logger.info('creating a ' + legend_label + '_bulletin_trend plot')
            days = []
            results = []
            previous = 0

            for elt in self.result_json:

                days.append(elt["data"][5:10])
                if flag == 'diff':
                    values = elt[json_label] - previous
                else:
                    values = elt[json_label]
                results.append(values)
                previous = elt[json_label]
            print(results)
            plt.clf()
            plt.plot(days, results, color + '-+', label=legend_label)
            plt.title('Trend '+legend_label+' COVID-19 in Italia')
            plt.xlabel('Giorni')
            plt.xticks(days, days, rotation='vertical')
            plt.ylabel('Casi')
            plt.grid(color='gray', linestyle='-', linewidth=0.2)
            plt.legend()
            plt.savefig(fname, dpi=200, figsize=(10, 10), edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1)
        except FileExistsError:
            self.logger.warning(json_label+'_bulletin_trend plot already exists')
            return path + "/" + returned_value

        return fname

    def get_regional_today_bulletin(self, region):
        """
        Get regional bulletin and makes trend (style1) with data
        :return: name of the generated file
        """
        flag = True
        regions = [elt["denominazione_regione"].lower() for elt in self.result_region_json]
        region = rdc.check_value(region, regions)
        element = [elt for elt in self.result_region_json
                   if region in elt["denominazione_regione"].lower()]
        out_message = ""
        out_message += "Ecco alcuni dettagli per la regione richiesta ["\
                       + str.capitalize(region) + "]:\n\n"
        try:
            if region == "NULL":
                raise IndexError
            for key in element[0].keys():
                if str(key).lower() == 'data':
                    out_message += str.capitalize(key) + ": " + \
                                   str(element[0][key]).replace("_", " ")[0:10] + "\n"
                elif  str(key).lower() not in NOTIN_LABEL:
                    out_message += str.capitalize(key).replace("_", " ") + ": " + \
                                   str(element[0][key]) + "\n"
        except IndexError:
            out_message = "Nome regione/provincia Errato!"
            flag = False
        return "\n" + out_message, flag


    def get_district_today_bulletin(self, district):
        """
        Get district bulletin and makes trend (style1) with data
        :return: name of the generated file
        """
        flag = True
        label = ""
        if len(district) <= 3:
            label = "sigla_provincia"
            all_districts = [elt[label].lower() for elt in self.result_district_json]
        else:
            label = "denominazione_provincia"
            all_districts = [elt[label].lower() for elt in self.result_district_json]

        district = rdc.check_value(district, all_districts)
        element = [elt for elt in self.result_district_json
                   if district.lower() in elt[label].lower()]
        out_message = ""
        out_message += "Ecco alcuni dettagli per la provincia richiesta ["\
                       + str.upper(district) + "]:\n\n"
        try:
            if district == "NULL":
                raise IndexError
            for key in element[0].keys():
                if str(key).lower() == 'data':
                    out_message += str.capitalize(key) + ": " + \
                                   str(element[0][key]).replace("_", " ")[0:10] + "\n"
                elif str(key).lower() not in NOTIN_LABEL:
                    out_message += str.capitalize(key).replace("_", " ") +\
                                   ": " + str(element[0][key]) + "\n"
        except IndexError:
            out_message = "Nome provincia/regione Errato!"
            flag = False
        return "\n" + out_message, flag

    def get_data_voice(self, text):
        """
        From User text , this method parses keyword to return the correct dataset
        :param text: speech text
        :return: output message
        """
        text = text.split(" ")
        # check for region
        for elt in text:
            values = self.get_regional_today_bulletin(elt)
            if values[1]:
                return values
        # check for district
        for elt in text:
            values = self.get_district_today_bulletin(elt)
            if values[1]:
                return values
        return list(text), False

