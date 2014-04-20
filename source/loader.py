 #! /usr/bin/env python
"""
Generates a data dictionary for the markov generator from a text file. The text file path is passed to the load function.
"""

import os

dictionary={"$start$":[]}

def load(path):
  """
  Load the text in the specified path into a dictionary.

  Each dictionary contains words in keys and possible next words in a list as a value. 
  """
  global dictionary

  with open (path,"r+") as data:
    lines=data.readlines()
    data.seek(0,0)

    for line in lines:
      #Change stupid american punctuation
      line=line.replace(".'","'.").replace('."','".')
      line=line.lstrip()

      #If a line does not end with a dot, remove the line break
      if not line.rstrip().endswith("."):
        line=line.rstrip()

      #If a line ends with a dash, remove the dash, remove the dash and the line break
      if line.rstrip().endswith("-"):
        line=line.rstrip().rstrip("-")

      #If the line is less than three words long, delete it
      if len(line.split())<=3:
        line=""

      #If a line is entirely in caps, delete it
      shout=1
      for i in line:
        if not i.isupper():
          if not i.isdigit():
            shout=0
      if shout==1:
        line=""

      #Write the modified line into the file
      data.write(line.lstrip())

    #Process the lines
    for line in data:

      #make the punctuation symbols a separate word and split the string
      line=line.strip().replace(","," ,").replace("-"," - ").replace(";"," ; ").replace(":"," : ").strip().split()

      #Process the line
      for i in range(len(line)):

        #Remove quotes
        line[i]=line[i].strip('"').strip("'")

        #If the line is empty, pass
        if line[i]=="" or line[i]==" ":
          pass

        #If the word is first in the line, add it to the possible start values
        if i==0:
          dictionary["$start$"].append(line[i])

        #If not, check if it's the last word
        else:

          #If it's not the last word, add it to the previous' word entry
          #Unless the previous word was the last one
          if line[i] not in ["!","?"] and "." not in line[i]:
            if line[i-1] not in ["!","?"] and "." not in line[i-1]:
              try:
                dictionary[line[i-1]].append(line[i])
              except KeyError:
                dictionary[line[i-1]]=[line[i]]

            else:
              if not line[i-1].partition('.')[0] in ["Mr","Mrs","Ms","St"]:
                dictionary["$start$"].append(line[i].strip('.'))
                try:
                  dictionary[line[i-1]].append("$end$")
                except KeyError:
                  dictionary[line[i-1]]=["$end$"]

            #Special case for abbreviations
            if line[i-1].partition('.')[0] in ["Mr","Mrs","Ms","St"]:
              try:
                dictionary[line[i-1]].append(line[i])
              except KeyError:
                dictionary[line[i-1]]=[line[i]]


          #If it's the last word, do the same and add the $end$ mark to the current word
          elif line[i] in ["!","?"] or "." in line[i]:

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

  return dictionary