# -*- coding: utf-8 -*-
# uses python 3
# getting complex definitions from wordreference
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

word = input("Enter word: ")

# some RegExp to fetch the sections I need
# specific sections have IDs like so: id='esen:18465'
regex = re.compile(r"esen:\d+")

def scrape(word):
  """Gets the definitions of a specified word from the wordreference website.

  :param word: word to be queried
  :type word: str
  :return: all definitions for the given word
  :rtype: list([str, str, str], [str, str, str])
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
      # getting rid of the '⇒' arrow (that is some hidden unicode symbol)
      if orig_word.find(u"⇒") != -1:
        orig_word = re.sub(r"[^\w]+", "", orig_word)

      # the simple definition is always the second entry <td> (see example HTML structure in 'sample.md')
      # it does NOT have a class or id associated, so I get it through slicing
      # it also starts with a whitespace char, which we don't need, so: lstrip()
      simple_def = d.findAll("td")[1].get_text().lstrip()

      # the 'ToWrd' <td> contains information about translation and POS, all in a str
      # for now I'm taking it all and we can later post-process
      transl_text = d.find("td", {"class" : "ToWrd"}).get_text()

      # add all info to a list of the following order:
      def_list.append([orig_word, simple_def, transl_text])
    return def_list
  except:
    error_msg = "No definitions found. Please double check the word you entered."
    return error_msg

def_list = scrape(word)

for i in def_list:
  pprint(i)
  print()
