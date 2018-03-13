# implemented in Ruby
require 'open-uri'
require 'Nokogiri'

#word = input("Enter word: ")
word = "sombrero"

# define the language
language = "es"

# some RegExp to fetch the sections I need
# specific sections have IDs like so: id='esen:18465' (at least for Spanish)
regex = /#{language}en:\d+/

def scrape(word, language)
  """Gets the definitions of a specified word from the wordreference website.

  :param word: word to be queried
  :type word: str
  :return: all definitions for the given word
  :rtype: list([str, str, str], [str, str, str])
  """
  # the URL for the es-en WR dict is built in the format 'baseURL/translation.asp?=word'
  page_url = "http://www.wordreference.com/#{language}/en/translation.asp?spen=" + word
  begin
    page = Nokogiri::HTML(open(page_url, "User-Agent" => "Mozilla/5.0"))
    # creating a bucket for the simple definitions
    def_list = Array.new

    # we want to get stuff from all the sections with numbered word IDs
    page.xpath('//tr[starts-with(@id, "esen:")]').each do |definition|

      # the actual word returned by the query
      orig_word = definition.css("strong").text

      # the simple definition is always the second entry <td> (see example HTML structure in 'sample.md')
      # it does NOT have a class or id associated, so I get it through slicing
      # it also starts with a whitespace char, which we don't need, so: lstrip()
      simple_def = definition.css("td")[1].text.lstrip!

      # # the 'ToWrd' <td> contains information about translation and POS, all in a str
      # # for now I'm taking it all and we can later post-process
      transl_text = definition.css("td")[2].text

      # # add all info to a list of the following order:
      def_list.push([orig_word, simple_def, transl_text])
    end
    return def_list
  rescue
    error_msg = "No definitions found. Please double check the word you entered."
    return error_msg
  end
end

# call the function, get the stuff
def_list = scrape(word, language)

# checkup #1
puts def_list[0][1]

# checkup #2
def_list.each do |i|
  puts i
  puts
end
