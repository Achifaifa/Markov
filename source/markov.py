#! /usr/bin/env python
"""
Generates random strings from a given dictionary.

The dictionary contains data generated from a text file by the loader module.
"""
import os, random
import loader

dictionary={"$start$":[]}
path="../data/sherlock"

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

dictionary=loader.load(path)
print "Ready \n",("="*10)
while 1:
  print talk()
  raw_input()