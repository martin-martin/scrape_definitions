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
    soup = BeautifulSoup(page.text, "html.parser")
    # creating a bucket for the simple definitions
    def_list = list()

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

      # the definition is always the second entry <td> (see example HTML structure in 'sample.html')
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
