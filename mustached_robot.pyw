#! /usr/bin/env python3
# 2011-09-05
# v0.20
#
#   Copyright 2011 S. Brewster Malevich <malevich@email.arizona.edu>
#
#   pydendro is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
This is a quick and dirty module to convert NCDC CSV files and data from the
PRISM website to a tab-delimited file which can be read by seascorr for data
analysis.

The fuction ncdc2seascorr and prism2seascorr can be used as a module in a script or program, although not yet through Bash shell. There is also a very simple tkinter GUI at the end of this file.

This should run on Linux, Mac and Windows with Python 3.
"""

import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename  # Hack to get around a bug.
from tkinter.filedialog import asksaveasfilename  # Hack to get around a bug.

def ncdc2seascorr(infile, outfile):
    """Converts a NCDC CSV file to a tab-delimited file seperated by months.

    Input:
        infile: The full path to the NCDC CSV file you wish to convert.
        outfile: The full path of file you want the tab-delimited format saved
        to.

    Return:
        No value is returned. Output is sent to outfile.

    At the moment it is assumed that the first line in infile is a line
    listing the source of the data. The second line is headings and the data
    begins on the third line. Data columns are as follows: 'State_id', 'YEAR',
    'Month', 'PRECIP (in)'. It is also assumed that each year in the data is
    is complete with no missing months. By this I mean that all months are
    present in the record, but if the record is missing, this is designated
    by a 'NA', 'None', etc...

    Note that this code isn't very bright. The only error catching, is if
    infile does not exist.

    Hopefully, this code will be improved and expanded in future versions.
    """
    if not os.path.isfile(infile):
        raise IOError()  # Want to build custom error for this eventually.
    # Might consider stream-lining this whole thing so that it's just in and
    # out without loading the file into Python.
    unparsed = []
    parsed = []
    with open(infile, 'r') as rawfile:  # Read the csv into python.
        for line in rawfile.readlines()[2:]: # Strips the heading.
            unparsed.append(line.rstrip())
    columns = ['YEAR(S)', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
               'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    with open(outfile, 'w') as outbox:
        for head in columns:  # Column heading for our new files.
            outbox.write('%s \t' % head)
        outbox.write('\n')
        year = None
        for line in unparsed:  # Parse the unparsed file data.
            line = line.split(',')
            if year is None:
                year = line[1]
                # TODO: Brush up on string formatting so that these two lines
                # can be merged into one, same with those below.
                outbox.write('%s \t' % year)
                outbox.write('%s \t' % line[3])
            elif line[1] == year:
                outbox.write('%s \t' % line[3])
            elif line[1] != year:
                outbox.write('\n')
                year = line[1]
                outbox.write('%s \t' % line[1])
                outbox.write('%s \t' % line[3])

def prism2seascorr(infile, outfile):
    """Converts PRISM copy-n-paste to a tabdelimited file seperated by months.

    Input:
        infile: The full path to the PRISM file you wish to convert. This file
        should be cut-n-paste from the web "PRISM explorer" into a simple .txt
        file.
        outfile: The full path of file you want the tab-delimited format saved
        to.

    Return:
        No value is returned. Output is sent to outfile.

    Note that this code isn't very bright. The only error catching, is if
    infile does not exist.

    Hopefully, this code will be improved and expanded in future versions.
    """
    if not os.path.isfile(infile):
        raise IOError()  # Want to build custom error for this eventually.
    # Might consider stream-lining this whole thing so that it's just in and
    # out without loading the file into Python.
    unparsed = []
    parsed = []
    with open(infile, 'r') as rawfile:  # Read the csv into python.
        for line in rawfile.readlines()[1:]: # Strips the heading.
            unparsed.append(line.rstrip())
    columns = ['YEAR(S)', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
               'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    with open(outfile, 'w') as outbox:
        for head in columns:  # Column heading for our new files.
            outbox.write('%s \t' % head)
        outbox.write('\n')
        year = None
        for line in unparsed:  # Parse the unparsed file data.
            line = line.split('\t')
            if year is None:
                year = line[0].strip()
                # TODO: Brush up on string formatting so that these two lines
                # can be merged into one, same with those below.
                outbox.write('%s \t' % year)
                outbox.write('%s \t' % line[2].strip())
            elif line[0].strip() == year:
                outbox.write('%s \t' % line[2].strip())
            elif line[0].strip() != year:
                outbox.write('\n')
                year = line[0].strip()
                outbox.write('%s \t' % line[0].strip())
                outbox.write('%s \t' % line[2].strip())

# Begin Tkinter GUI code.
root = Tk()
root.title("Madness-to-SEASCORR")
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)

filein = StringVar()
fileout = StringVar()
statusmsg = StringVar()

def startconvert():
    # This is rather convoluted.
    statusmsg.set("Working...")
    rawfile = filein.get()
    fl = open(rawfile, 'r')
    testline = fl.readline()
    fl.close()
    if testline == 'Year\tMonth\tValue\n':
        prism2seascorr(infile = rawfile, outfile = fileout.get())
        statusmsg.set("Your file is ready!") 
    elif testline == 'Source: MJ Menne CN Williams Jr. RS Vose NOAA National Climatic Data Center Asheville, NC\n':
        ncdc2seascorr(infile = rawfile, outfile = fileout.get())
        statusmsg.set("Your file is ready!")
    else:
        statusmsg.set("There appears to be a problem with the file format.")

def selectfilein():
    filein.set(askopenfilename(filetypes = [('all files', '.*'), ('comma-separated values', '.csv')]))
    statusmsg.set("Please select your files and press 'Convert'...")

def selectfileout():
    fileout.set(asksaveasfilename(defaultextension = '.tsv'))
    statusmsg.set("Please select your files and press 'Convert'...")

filein_entry = ttk.Entry(mainframe, text = filein, width = 50,
                         textvariable = filein)
filein_entry.grid(column = 0, row = 1, sticky = (E, W))
fileout_entry = ttk.Entry(mainframe, text = fileout, width = 50,
                          textvariable = fileout)
fileout_entry.grid(column = 0, row = 3, sticky = (E, W))
ttk.Label(mainframe, textvariable = statusmsg).grid(column = 0, row = 4,
                                                    sticky = W)
ttk.Label(mainframe, text = "Input:").grid(column = 0, row = 0, sticky = W)
ttk.Label(mainframe, text = "Destination:").grid(column = 0, row = 2,
          sticky = W)
ttk.Button(mainframe, text = 'Convert',
           command = startconvert).grid(column = 1, row = 4, sticky = E)
ttk.Button(mainframe, text = "Select...",
           command = selectfilein).grid(column = 1, row = 1, sticky = E)
ttk.Button(mainframe, text = "Select...",
           command = selectfileout).grid(column = 1, row = 3, sticky = E)

statusmsg.set("Please select your files and press 'Convert'...")
for child in mainframe.winfo_children():
    print(child)
    child.grid_configure(padx = 2, pady = 2)
root.bind('<Return>', startconvert)
filein_entry.focus()

root.mainloop()
