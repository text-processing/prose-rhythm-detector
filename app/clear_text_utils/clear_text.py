""""
ProseRhythmDetector - the tool for extraction of rhythm features and computation of stylometric features for texts.
    Copyright (C) 2020  Vladislav Larionov, Vladislav Petryakov, Anatoly Poletaev, Ksenia Lagutina, Alla Manakhova, Nadezhda Lagutina, Elena Boychuk.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    The corresponding author: Ksenia Lagutina, lagutinakv@mail.ru
"""

import sys
import getopt
import os
import re


def exit_with_error_message(message):
    """ Print the error message and exit. """
    print(message)
    print(HELP_TEXT)
    sys.exit(2)


def get_arguments():
    """ Extract values of command line arguments"""
    try:
        arguments = getopt.getopt(sys.argv[1:], "t:o:h", ["texts=", "output=", "help"])
    except getopt.GetoptError as err:
        exit_with_error_message(str(err))
    texts_path = None
    output_path = None
    for opt, arg in arguments[0]:
        if opt in ("-t", "--texts"):
            texts_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-h", "--help"):
            print(HELP_TEXT)
            sys.exit()
        else:
            assert False, "unhandled option"
    if texts_path is None:
        exit_with_error_message("Specify the path to texts.")
    if output_path is None:
        exit_with_error_message("Specify the output directory.")
    return texts_path, output_path


HELP_TEXT = """Usage: python3 clear_text.py -t TEXTS_PATH -o OUTPUT_PATH
-t TEXTS_PATH, --texts=TEXTS_PATH:
\tPath to a directory with texts to clear.
-o OUTPUT_PATH, --output=OUTPUT_PATH:
\tPath to the output directory with clean texts.
-h, --help:
\tPrints help of the script.
"""


def clear_line(line):
    trimmed_line = line.replace('*', '').strip()
    if not trimmed_line:
        return trimmed_line
    line_without_multi_spaces = ' '.join(trimmed_line.split())
    clean_line = line_without_multi_spaces.replace('"', '\'')
    clean_line = clean_line.replace(' ', ' ')
    clean_line = clean_line.replace('—', '-')
    clean_line = clean_line.replace('–', '-')
    clean_line = clean_line.replace('−', '-')
    clean_line = re.sub('-+', '-', clean_line)
    clean_line = clean_line.replace(' :', ':')
    clean_line = clean_line.replace('« ', '\'')
    clean_line = clean_line.replace(' »', '\'')
    clean_line = clean_line.replace('“', '\'')
    clean_line = clean_line.replace('”', '\'')
    clean_line = clean_line.replace(' ?', '?')
    clean_line = clean_line.replace(' ;', ';')
    clean_line = clean_line.replace(' !', '!')
    clean_line = clean_line.replace(' …', '…')
    clean_line = clean_line.replace('’', "'")
    clean_line = clean_line.replace('‘', "'")
    clean_line = clean_line.replace("-'", "'")
    clean_line = clean_line.replace("_", "")
    clean_line = re.sub(r'([.?!…]+)([\"\'])([ \n]?)', r'\2\1\3', clean_line)
    return clean_line


if __name__ == "__main__":
    TEXTS_DIR, OUTPUT_DIR = get_arguments()
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    for filename in os.listdir(TEXTS_DIR):
        full_path = os.path.join(TEXTS_DIR, filename)
        if os.path.isfile(full_path) and filename.endswith('txt'):
            print("Processing " + filename)
            clean_file = open(os.path.join(OUTPUT_DIR, filename), "w")
            with open(full_path) as fp:
                line = fp.readline()
                while line:
                    clean_line = clear_line(line)
                    clean_file.write(clean_line)
                    clean_file.write("\n")
                    line = fp.readline()
            clean_file.close()
