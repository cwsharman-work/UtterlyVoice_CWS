"""
This script outputs the file data-entry-plants.yaml, which makes a list of plants in data entry format from the list provided in plant_names.csv.

Due to some lazy programming...
Make sure the csv of plant names has the headings 'alternate names' 'common name' 'scientific name' and 'invasive'
Make sure the alternate names are only separated by a comma (no space)
"""

import pandas as pd

write_to_utterly_dir = True # likely better to keep this False, but up to you. If False, remember to copy yaml file to utterly voice
print_at_end = False # can print to terminal at end of program

list_of_plants_file = "helpers/plant_formatting/plant_names.csv"
df = pd.read_csv(list_of_plants_file)

# set output file location
if write_to_utterly_dir:
    output_dir = "utterlyvoice-1.09/config/modes/data-entry-plants.yaml"
else:
    output_dir = "helpers/plant_formatting/data-entry-plants.yaml"

output_file = open(output_dir, "w") #"w" overwrites the file every time you run this program

# get data for yaml header
num_plants = len(df)

# add yaml header to file
file_header = """---
name: "data entry plants"
description: >-
  Used to type plants in data entry format. Includes """+str(num_plants)+""" plants (barring errors in the csv).
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
          - "'''+str(row['common name'])+"\\t"+str(row['scientific name'])+'''"
    spaceLeft: true
    spaceRight: true'''
    output_file.write(plant_string)

# output_file.write("\n\nSkipped "+str(skipped_plant_count)+" plant(s). Remember to copy this list into data-entry.yaml")
output_file.close()

if print_at_end:
    f = open(output_dir, "r")
    print(f.read())
    f.close()