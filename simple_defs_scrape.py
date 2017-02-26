# -*- coding: utf-8 -*-
# getting complex definitions from wordreference
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

word = raw_input("Enter word: ")
# word = "hablar"

# some RegExp to fetch the sections I need
# specific sections have IDs like so: id='esen:18465'
regex = re.compile(r"esen:\d+")

def scrape(word):
  """Scrapes the definitions of a specified word from the wordreference website.

  :param word: word to be queried
  :type word: str
  :return: all definitions for the given word
  :rtype: list('unicode', 'unicode')
  """
  # the URL for the es-en WR dict is built in the format 'baseURL/translation.asp?=word'
  page_url = "http://www.wordreference.com/es/en/translation.asp?spen=" + word
  try:
    page = requests.get(page_url)
    #print page
    soup = BeautifulSoup(page.text, "html.parser")
    #print "#######################################"
    #print html
    # creating a bucket for the simple definitions
    def_list = list()

    ########## UNDERSTANDING THE DATA STRUCTURE ##########

    # the definitions are nested in a <div> id='articleWRD'
    # and its <table> class='WRD' elements, further nested like so:
    #
    # <tr class='wrtopsection'>
    #   <td colspan='3' title='Principal Translations'>
    #     <strong>Principal Translations</strong>
    #   </td>
    # </tr>
    # <tr class='langHeader' style='font-size: 13px;text-decoration: underline;font-weight:bold;'>
    #   <td class='FrWrd'>Spanish</td>
    #   <td></td>
    #   <td class='ToWrd'>English</td>
    # </tr>
    # <tr class='even' id='esen:18465'>
    #   <td class='FrWrd' >
    #     <strong>vamos</strong> <em class='tooltip POS2'>expr<span><i>expresión</i>: Expresiones idiomáticas, dichos, refranes y frases hechas de tres o más palabras ("Dios nos libre", "a lo hecho, pecho").</span></em>
    #   </td>
    #   <td> (para instar, urgir)</td>
    #   <td class='ToWrd' >
    #     let´s go, come on <em class='tooltip POS2'>interj<span><i>interjection</i>: Exclamation--for example, "Oh no!"  "Wow!"</span></em>
    #   </td>
    # </tr>
    # <tr class='even'>
    #   <td>&nbsp;</td>
    #   <td colspan='2' class='FrEx'>Vamos, hay que darse prisa que se nos hace tarde.</td>
    # </tr>

    ###### IMPORTANT SECTIONS ######

    # <tr class='wrtopsection'>
    #   <td title='Principal Translations'>
    #     <strong>________</strong>
    #   </td>
    # </tr>
    # <tr class='langHeader'>
    #   <td class='FrWrd'>Spanish</td>
    #   <td></td>
    #   <td class='ToWrd'>English</td>
    # </tr>
    # <tr id='esen:18465'>
    #   <td class='FrWrd' >
    #     <strong>vamos</strong>
    #     <em class='tooltip POS2'>expr
    #       <span>
    #         <i>expresión</i>:
    #           Expresiones idiomáticas, dichos, refranes y frases hechas
    #           de tres o más palabras ("Dios nos libre", "a lo hecho, pecho").
    #       </span>
    #     </em>
    #   </td>
    #   <td> (para instar, urgir)</td>
    #   <td class='ToWrd' >
    #     let´s go, come on
    #     <em class='tooltip POS2'>interj
    #       <span>
    #         <i>interjection</i>: Exclamation--for example, "Oh no!"  "Wow!"
    #       </span>
    #     </em>
    #   </td>
    # </tr>
    # <tr>
    #   <td></td>
    #   <td class='FrEx'>Vamos, hay que darse prisa que se nos hace tarde.</td>
    # </tr>

    # match all the sections with numbered word IDs
    all_defs = soup.findAll("tr", {"id" : regex})
    for d in all_defs:
      orig_word = d.find("td", {"class" : "FrWrd"}).find("strong").get_text()
      # getting rid of the '=>' arrow (that is some hidden unicode symbol)
      orig_word = re.sub("[^\w]+", "", orig_word)
      # the 'ToWrd' <td> contains information about translation and POS, all in a str
      transl_text = d.find("td", {"class" : "ToWrd"}).get_text()
      #pattern = re.compile(r"(?<='ToWrd' >\s).*") # trying to patternmatch the pieces

      # TODO: this is erroneous. if the translation consists of more than one word,
      #       it slices incorrectly!!!!!! needs a fix.

      # the definition is always the second entry <td> (see example HTML above)
      # it does NOT have a class or id associated, so I get it through slicing
      # it alsow starts with a whitespace char, which we don't need, so: lstrip()
      simple_def = d.findAll("td")[1].get_text().lstrip()
      if word == orig_word or word + "se" == orig_word: #reflexive form
        # add all info to a list of the following order:
        def_list.append([orig_word, simple_def, transl_text])
    return def_list
  except:
    error_msg = "No definitions found. Please double check the word you entered."
    return error_msg

def_list = scrape(word)

for i in def_list:
  print i
  print