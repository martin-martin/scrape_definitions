# getting complex definitions from wordreference
import requests
from bs4 import BeautifulSoup
from pprint import pprint

word = raw_input("Enter word: ")
#word = "escuchar"

def scrape(word):
  """Scrapes the definitions of a specified word from the wordreference website.

  :param word: word to be queried
  :type word: str
  :return: all definitions for the given word
  :rtype: list('unicode', 'unicode')
  """
  # the URL is built in the format 'baseURL/word'
  page_url = "http://www.wordreference.com/definicion/" + word
  try:
    page = requests.get(page_url)
    #print page
    soup = BeautifulSoup(page.text, "html.parser")
    #print "#######################################"
    #print html
    # creating a bucket for the definitions
    def_list = list()
    # the definitions are nested in an <ol> class='entry' and its <li> elements
    all_definitions = soup.find("ol", {"class" : "entry"})
    for d in all_definitions.findAll("li"):
      definition = d.get_text()
      def_list.append(definition)
    return def_list
  except:
    error_msg = "No definitions found. Please double check the word you entered."
    return error_msg

def_list = scrape(word)

for i in def_list:
  print i
  print