"""
This is a generic version of my jargon helper files. It reads an excel file (which keeps formatting so headers are in the same place, unlike .csv). 
The default headers are command, alternates, and description.
It begins with several settings, including variables that add things to the .gitignore automatically if you want.
Make sure the alternates in the spreadsheet are only separated by commas!
"""

import pandas as pd
# import os

### Generic setup
## Settings (modify these)
write_to_utterly_dir = False # likely better to keep this False, but up to you. If False, remember to copy yaml file to utterly voice
print_at_end = True # can print to terminal at end of program

file_private = False # adds output_file to .gitignore if True - code at end of this file
directory_private = False # adds this directory to .gitignore if True - code at end of this file

output_file_name = "test-output-file.yaml"
output_file_title = "output file" # this gets written to yaml. match it to the output_file_name
output_file_description = "This file contains example jargon."

this_file_dir = "helpers/" # this is where the output file will go if write_to_utterly_dir is false
jargon_data_file = this_file_dir + "jargon_example_data.xlsx"
### End settings to modify

# set output file location based on write_to_utterly_dir
if write_to_utterly_dir:
  output_dir = "utterlyvoice-1.09/config/modes/" + output_file_name
else:
  output_dir = this_file_dir + output_file_name


### Creating and adding data to output file
output_file = open(output_dir, "w") # overwrites the file every time you run this program
df = pd.read_excel(jargon_data_file)

# get data for yaml header
num_commands = len(df)

# add yaml header to file
file_header = """---
name: """+output_file_title+"""
description: >-
  """+output_file_description+""" Includes """+str(num_commands)+""" command(s) (barring errors in the jargon spreadsheet).
initiallyActive: false
exclusive: false
commands:"""
output_file.write(file_header)

skipped_commands_count = 0 # not in use
for index, row in df.iterrows():
    # check if common name exists. If not, skip this plant
    if not isinstance(row['command'], str):
        skipped_commands_count += 1
        continue
    # first need to setup a list of alternate names
    alt_names = row['alternates']
    alternates_string = ''
    if isinstance(alt_names,str):
        alternates_string = "\n    alternates: "
        alt_names = alt_names.split(',')
        for name in alt_names:
            alternates_string += '\n      - "'+str(name)+'"'
    # now we make the big string...
    big_string = '''
  - name: "'''+str(row['command'])+'''"
    description: >-
      '''+output_file_description+alternates_string+'''
    functions:
      - name: "type"
        fixedArguments:
          - "'''+str(row['command'])+'''"'''
    output_file.write(big_string)
output_file.close()

if print_at_end:
    f = open(output_dir, "r")
    print(f.read())
    f.close()

print("\n\nSkipped "+str(skipped_commands_count)+" command(s).")

## add to .gitignore if file_private and/or directory_private are True
gitignore_file_name = ".gitignore"

# check whether locations are already in .gitignore
# check if output_dir and directory are in .gitignore already
this_dir = "/"+this_file_dir[:-1] # need / at beginning and not end for directories in .gitignore.
with open(gitignore_file_name, "r") as fp:
  in_data_output_dir = False
  in_data_this_dir = False 
  # read all lines
  lines = fp.readlines()
  for row in lines:
      if row == output_dir:
        in_data_output_dir = True
      if row == this_dir:
        in_data_this_dir = True
 
print(output_dir + " in .gitignore already: "+str(in_data_output_dir)+" (file_private is set to "+str(file_private)+")")
print(this_dir + " in .gitignore already: "+str(in_data_this_dir)+" (directory_private is set to "+str(directory_private)+")")

if file_private and not in_data_output_dir:
  # add output_file to .gitignore if not there already
  with open(gitignore_file_name, "a") as filepath:
    filepath.write("\n" + output_dir)
    print("Wrote "+output_dir+" to "+gitignore_file_name)
if directory_private and not in_data_this_dir:
  with open(gitignore_file_name, "a") as filepath:
    filepath.write("\n" + this_dir)
    print("Wrote "+this_dir+" to "+gitignore_file_name)