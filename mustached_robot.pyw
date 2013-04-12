#! /usr/bin/env python3
# 2013-03-11
#
#   Copyright 2013 S. Brewster Malevich <malevich@email.arizona.edu>
#
#   mustached-robot is free software: you can redistribute it and/or modify
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

The fuction ncdc2seascorr and prism2seascorr can be used as a module in a
script or program, although not yet through Bash shell. There is also a very
simple tkinter GUI at the end of this file.

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


class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        parent.title("mustached-robot")
        self.mainFrame = ttk.Frame(root, padding = "3 3 12 12")
        self.mainFrame.grid(column = 0, row = 0, sticky = (N, W, E, S))
        self.mainFrame.columnconfigure(0, weight = 1)
        self.mainFrame.rowconfigure(0, weight = 1)

        self.inFileString = StringVar()
        self.outFileString = StringVar()
        self.statusString = StringVar()

        filein_entry = ttk.Entry(self.mainFrame, text = self.inFileString, width = 50,
                                 textvariable = self.inFileString)
        filein_entry.grid(column = 0, row = 1, sticky = (E, W))
        fileout_entry = ttk.Entry(self.mainFrame, text = self.outFileString, width = 50,
                                  textvariable = self.outFileString)
        fileout_entry.grid(column = 0, row = 3, sticky = (E, W))
        ttk.Label(self.mainFrame, textvariable = self.statusString).grid(column = 0, row = 4,
                                                            sticky = W)
        ttk.Label(self.mainFrame, text = "Input:").grid(column = 0, row = 0, sticky = W)
        ttk.Label(self.mainFrame, text = "Destination:").grid(column = 0, row = 2,
                  sticky = W)
        self.selectinButton = ttk.Button(self.mainFrame, text = "Select...",
                                         command = self.selectinfile)
        self.selectoutButton = ttk.Button(self.mainFrame, text = "Select...",
                                          command = self.selectoutfile)
        self.convertButton = ttk.Button(self.mainFrame, text = 'Convert',
                                        command = self.startconvert,
                                        state = DISABLED)
        self.selectinButton.grid(column = 1, row = 1, sticky = E)
        self.selectoutButton.grid(column = 1, row = 3, sticky = E)
        self.convertButton.grid(column = 1, row = 4, sticky = E)

        self.statusString.set("Please select your files.")
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx = 2, pady = 2)
        filein_entry.focus()

    def selectinfile(self):
        """Input file selection dialog"""
        self.inFileString.set(askopenfilename(filetypes = [('all files', '.*'),
                        ('comma-separated values', '.csv')]))
        self.statusString.set("Please select your files")
        self.checkfilestrings()

    def selectoutfile(self):
        """Output file selection dialog"""
        self.outFileString.set(asksaveasfilename(defaultextension = '.tsv'))
        self.statusString.set("Please select your files")
        self.checkfilestrings()

    def startconvert(self):
        """Detects formatting and converts input file to output file"""
        # This is rather convoluted.
        self.statusString.set("Working...")
        rawfile = self.inFileString.get()
        fl = open(rawfile, 'r')
        testline = fl.readline()
        fl.close()
        if testline == 'Year\tMonth\tValue\n':
            prism2seascorr(infile = rawfile, outfile = self.outFileString.get())
            self.statusString.set("Your file is ready!") 
        elif testline == 'Source: MJ Menne CN Williams Jr. RS Vose NOAA National Climatic Data Center Asheville, NC\n':
            ncdc2seascorr(infile = rawfile, outfile = self.outFileString.get())
            self.statusString.set("Your reformatted file is ready")
        else:
            self.statusString.set("There appears to be a problem with the file format.")

    def checkfilestrings(self):
        """If inFileString and outFileString then enable convertButton"""
        if (len(self.inFileString.get()) > 0) and (len(self.outFileString.get()) > 0):
            self.convertButton.config(state = NORMAL)
        self.statusString.set("Select convert when you're ready")


if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
