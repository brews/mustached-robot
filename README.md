mustached-robot
===============
2013-04-11
Copyright 2013, S. Brewster Malevich <malevich@email.arizona.edu>

A painfully simple program that expands monthly time series files.

What does this program do?
--------------------------
mustached-robot helps people reformat flat, time-series files of monthly climate data.

This was originally tailored to format input data so that it could be read into Dave Meko's "seascorr" MATLAB script, but I've heard that other people have found uses for this.

How do I use this?
-----------------------------------------------
This program is happy to run on Linux, Mac, or MS Windows. However, it is not yet tested on all of these platforms.

You need to go install a recent [copy of Python](http://www.python.org/download/) version 3.x. Python version 2.x will not work.

Once you have that installed, you can run the program by double clicking on the `mr.pyw` file. Google or ask around if you're having trouble.

What kind of files can I read into this program?
------------------------------------------------
Go take a look in the `data` folder that came with the program. You'll see a copy of a NCDC .csv file and a PRISM .txt file. Files that are formatted exactly in this way should work fine. You can see what the output of each of these files is 

What kind of files are produced by this program?
------------------------------------------------
Check out the `data` folder that came with the program. The .tsv (tab-separated) with "goal" in the name are examples of the reformatted NCDC and PRISM files which are also in the `data` folder.

Help! I have a problem!
-----------------------
If you've found a bug, please go ahead and file a bug report on [our bug tracker](https://github.com/brews/mustached-robot/issues). Include a detailed description of what you did and what went wrong.

If you have another issue or your uncomfortable with bug reports you can contact one of the developers (me). Depending on my work load, it may be a few days before I get back to you.

This is awesome! I want to contribute
-------------------------------------------------
This program is open source so feel free to share it, fork it, hack it. The source code is available [here](https://github.com/brews/mustached-robot). There are a few restrictions and these are outlined in the LICENSE file.
