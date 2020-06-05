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


# pylint: disable=E0401

"""
Contains functions that are common for statistical utiltes.

exit_with_error_message
prints the error message, the text about the utility, and exit.

get_arguments
returns the input file and output file/path from command line arguments.

save_plot
saves a plot as png.
"""

import sys
import getopt
import os
import matplotlib.pyplot as plt


def exit_with_error_message(message, help_text):
    """ Print the error message and exit. """
    print(message)
    print(help_text)
    sys.exit(2)


def get_arguments(help_text):
    """ Extract values of command line arguments"""
    try:
        arguments = getopt.getopt(sys.argv[1:], "f:o:h", ["features=", "output=", "help"])
    except getopt.GetoptError as err:
        exit_with_error_message(str(err), help_text)
    features_path = None
    output_path = 'pictures/'
    for opt, arg in arguments[0]:
        if opt in ("-f", "--features"):
            features_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-h", "--help"):
            print(help_text)
            sys.exit()
        else:
            assert False, "unhandled option"
    if features_path is None:
        exit_with_error_message("Specify the path to features.", help_text)
    return features_path, output_path


def save_plot(name, path):
    """ Save the plot as png by path with name """
    fmt = 'png'
    pwd = os.getcwd()
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    plt.savefig(name + '.' + fmt, fmt='png')
    os.chdir(pwd)
