"""
This script outputs the file scientific-plants.yaml, which makes a list of plants in Common name (scientific name) format from the list provided in plant_names.csv.

Due to some lazy programming...
Make sure the csv of plant names has the headings 'alternate names' 'common name' 'scientific name' and 'invasive'
Make sure the alternate names are only separated by a comma (no space)

TODO:
fix excel error (sigh)
"""

import pandas as pd

write_to_utterly_dir = True # likely better to keep this False, but up to you. If False, remember to copy yaml file to utterly voice
print_at_end = False # can print to terminal at end of program

list_of_plants_file = "helpers/plant_formatting/plant_names.xlsx"
df = pd.read_excel(list_of_plants_file)

output_file_name = "plants-scientific.yaml"

# set output file location
if write_to_utterly_dir:
    output_dir = "utterlyvoice-1.09/config/modes/" + output_file_name
else:
    output_dir = "helpers/plant_formatting/" + output_file_name

output_file = open(output_dir, "w") #"w" overwrites the file every time you run this program

# get data for yaml header
num_plants = len(df)

# add yaml header to file
file_header = """---
name: "plants scientific"
alternates:
  - "plant scientific"
description: >-
  Used to type plants in Common name (scientific name) format. Includes """+str(num_plants)+""" plants (barring errors in the csv).
initiallyActive: false
exclusive: false
commands:"""
output_file.write(file_header)

skipped_plant_count = 0 # not in use
for index, row in df.iterrows():
    # check if common name exists. If not, skip this plant
    if not isinstance(row['common name'], str):
        skipped_plant_count += 1
        continue
    # first need to setup a list of alternate names
    alt_names = row['alternate names']
    alternates_string = ''
    if isinstance(alt_names,str):
        alternates_string = "\n    alternates: "
        alt_names = alt_names.split(',')
        for name in alt_names:
            alternates_string += '\n      - "'+str(name)+'"'
    # now we make the big string...
    plant_string = '''
  - name: "'''+str(row['common name'])+'''"
    description: >-
      '''+str(row['scientific name'])+alternates_string+'''
    functions:
      - name: "type"
        fixedArguments:
          - "'''+str(row['common name'])+" ("'''"'''
    italics_string = '''
      - name: "keyPress"
        fixedArguments:
          - "control"
          - "i"'''
    scientific_plant_string = '''
      - name: "type"
        fixedArguments:
          - "'''+str(row['scientific name'])+'''"'''
    end_parenthesis_string = '''
      - name: "type"
        fixedArguments:
          - ")"'''
    combined_string = plant_string+italics_string+scientific_plant_string+italics_string+end_parenthesis_string
    output_file.write(combined_string)

# output_file.write("\n\nSkipped "+str(skipped_plant_count)+" plant(s). Remember to copy this list into data-entry.yaml")
output_file.close()

if print_at_end:
    f = open(output_dir, "r")
    print(f.read())
    f.close()