# JSON-Editor
Has a qt interface, generates json from a template. It is also possible to upload files to text lists of their names. 

# How to use
Example of input:'''
{
"~~~soundname1 soundname2 soundname3~~~": {
    "category": "player",
    "sounds": [["~~~soundname11~~~", "soundname12", "soundname13", "soundname14"], ["soundname21", "soundname22", "soundname23", "soundname24", "soundname25", "soundname26"], ["soundname34", "soundname35", "soundname36", "soundname37", "soundname38"]]
  }
}'''

At the out.json it will turn out :
'''
{
  "soundname1": {
    "category": "player",
    "sounds": [
      "soundname11",
      "soundname12",
      "soundname13",
      "soundname14"
    ]
  },
  "soundname2": {
    "category": "player",
    "sounds": [
      "soundname21",
      "soundname22",
      "soundname23",
      "soundname24",
      "soundname25",
      "soundname26"
    ]
  },
  "soundname3": {
    "category": "player",
    "sounds": [
      "soundname34",
      "soundname35",
      "soundname36",
      "soundname37",
      "soundname38"
    ]
  }
}
'''
Functional:
"File extension" A checkbox that shows whether the filenames will be added with or without extension.
"Add File Names" Adds and writes a list of filenames.
"Add File Names Arrays" Adds and writes a list of arrays of filenames (not for headers)
"Convert" Generates a json file and dumps it to out.json in the same directory where the script is located. 
