#! /usr/bin/env python
import os, random

dictionary={"$start$":[]}
path="./data/text"

def formatf():
  """
  Formats a file removing anything that is not a sentence and would screw the loader up
  """

  with open (path,"r+") as file:
    whole=file.readlines()
    for line in whole:
      line=line.replace("?"," ? ").replace("!"," ! ").replace(","," , ").replace(";"," ; ").replace(":"," : ").replace('"',"")
      if len(line.split())<2:
        line=""


    file.seek(0,0)
    for line in whole:
      file.write(line)


def load():
  """
  Load the text in ./data/text into a dictionary.

  Each dictionary contains words in keys and possible next words in a list as a value. 
  """
  global dictionary

  formatf()

  with open (path,"r") as data:

    for line in data:
      line=line.strip().replace(","," ,").replace("-"," - ").replace(";"," ; ").replace(":"," : ").strip(".").strip().split()

      #Process a line
      for i in range(len(line)):
        line[i]=line[i].strip('"')
        #If the line is empty, pass
        if line[i]=="" or line[i]==" ":
          pass

        #If the word it's first in the line, add it to the possible start values
        if i==0:
          dictionary["$start$"].append(line[i])

        #If not, check if it's the last word
        else:

          #If it's not the last word, add it to the previous' word entry
          #Unless the previous word was the last one
          if "." not in line[i] and "?" not in line[i] and "!" not in line[i]:
            if "." not in line[i-1] and not line[i-1] in ["!","?"]:
              try:
                dictionary[line[i-1]].append(line[i])
              except KeyError:
                dictionary[line[i-1]]=[line[i]]
            elif "." in line[i-1]:
              if not line[i-1].partition('.')[0] in ["Mr","Mrs","Ms","St"]:
                dictionary["$start$"].append(line[i].strip('.'))

            #Special case for abbreviations
            if line[i-1].partition('.')[0] in ["Mr","Mrs","Ms","St"]:
              try:
                dictionary[line[i-1]].append(line[i])
              except KeyError:
                dictionary[line[i-1]]=[line[i]]


          #If it's the last word, do the same and add the $end$ mark to the current word
          elif "." in line[i]:
            #Check if the word with a dot is an abbreviation
            #If it is, add the word with the dot as previously done
            if line[i].partition('.')[0] in ["Mr","Mrs","Ms","St"]:
              if "." not in line[i-1]:
                try:
                  dictionary[line[i-1]].append(line[i])
                except KeyError:
                  dictionary[line[i-1]]=[line[i]]
              elif "." in line[i-1]:
                dictionary["$start$"].append(line[i])

            #If it's not, process the end of the sentence
            else:
              try:
                dictionary[line[i-1]].append(line[i].strip('.').strip())
              except KeyError:
                dictionary[line[i-1]]=[line[i].strip('.').strip()]
              try:
                dictionary[line[i].strip('.').strip()].append("$end$")
              except KeyError:
                dictionary[line[i].strip('.').strip()]=["$end$"]


def format(string):
  """
  Formats the output string
  """

  return string.replace(" ,",",").replace(" - ","-").replace(" ;",";").replace(" :",":").strip(".").strip("'").strip()+"."

def talk():
  """
  Generates a string fror a dictionary containing references
  """

  chain=""
  word="$start$"

  try:
    while 1:
      word=random.choice(dictionary[word])
      if word in ["$end$","."]:
        break
      else:
        chain=chain+" "+word
    return format(chain)

  except KeyError:
    return "Key Error: "+word

load()
# print dictionary["$start$"]
print "Ready \n",("="*10)
while 1:
  print talk()
  raw_input()