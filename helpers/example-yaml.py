"""
This script outputs a yaml file with string setup for common functions.
"""

import pandas as pd

write_to_utterly_dir = False # likely better to keep this False, but up to you. If False, remember to copy yaml file to utterly voice
print_at_end = False # can print to terminal at end of program

output_file_name = "output-yaml.yaml"

# set output file location
if write_to_utterly_dir:
    output_dir = "utterlyvoice-1.09/config/modes/" + output_file_name
else:
    output_dir = "helpers/" + output_file_name

output_file = open(output_dir, "w") #"w" overwrites the file every time you run this program

# add yaml header to file
file_header = """---
name: "output yaml"
description: >-
  This is the result of a python file that creates examples of common functions in yaml format.
initiallyActive: false
exclusive: false
commands:"""
output_file.write(file_header)

# junk variable
junk = "junk"

## common functions
# these use ''' to contain "" which the yaml file needs
# the simple versions are straightforward
# the complex versions have a basic setup for when you want to add variables to the strings
type_function_simple = '''
  - name: "name"
    description: >-
      Description here
    alternates: 
      - "alternate here"
    functions:
      - name: "type"
        fixedArguments:
          - "text here"
    spaceLeft: true
    spaceRight: true'''

type_function_complex = '''
  - name: "'''+junk+'''"
    description: >-
      '''+junk+'''
    alternates:
      - "'''+junk+'''"
    functions:
      - name: "type"
        fixedArguments:
          - "'''+junk+'''"
    spaceLeft: true
    spaceRight: true'''

keypress_function_simple = '''
  - name: "keypress example"
    description: >-
      Description of keypress example
    functions:
      - name: "keyPress"
        fixedArguments:
          - "control"
          - "i"'''

#write to output file
output_file.write(type_function_simple)
output_file.write(type_function_complex)
output_file.write(keypress_function_simple)

#close output file
output_file.close()