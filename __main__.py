from print_notas import print_notas

"""
Fill the arguments below and run the script to print the grades
run 'python .' or 'python3 .' in the project root to run script
"""

# must be a String filepath
filename = "example.tsv"

# must be String
title = "Notas Example"

# must be Integer
top_percent_to_appear = 10

# whether to save or not in /results directory
save = True

if __name__ == "__main__":
    print_notas("formatted_data/" + filename, title, top_percent_to_appear, save)