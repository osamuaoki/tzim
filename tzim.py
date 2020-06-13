#!/usr/bin/python3
#################################################################################################
#                                                                                               #
# tzim.py - Simple conversion module to convert a Tomboy/Gnote notes to zim notes.              #
#                                                                                               #
#           _Usage_:                                                                            #
#           If not already executable,                                                          #
#           $ chmod a+x tzim.py                                                                 #
#           Run                                                                                 #
#           $ <dir-path to tzim.py>/tzim.py                                                     #
#           follow instructions. When conversed, open zim and add repository (i.e. target dir)  #
#                                                                                               #
#                                                                                               #
#           GPL statement:                                                                      #
#           This program is free software; you can redistribute it and/or modify                #
#           it under the terms of the GNU General Public License as published by                #
#           the Free Software Foundation; either version 3 of the License, or                   #
#           (at your option) any later version.                                                 #
#                                                                                               #
#           This program is distributed in the hope that it will be useful,                     #
#           but WITHOUT ANY WARRANTY; without even the implied warranty of                      #
#           MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       #
#           GNU General Public License for more details.                                        #
#                                                                                               #
#           You should have received a copy of the GNU General Public License                   #
#           along with this program.  If not, see <http://www.gnu.org/licenses/>.               #
#                                                                                               #
#           Copyright 2007,2008 Bengt J. Olsson                                                 #
#           Copyright 2020      Osamu Aoki                                                      #
#                                                                                               #
# Rev:      1.2.1-oa01                                                                          #
# Date:     2020-06-13  (OA)                                                                    #
# Changes:  Updated to python3 and adjust default behavior to modern path choices               #
#   (original from https://github.com/jaap-karssenberg/zim-wiki/wiki/Tomboy-import-script)      #
#   (original upstream URL http://blafs.com/diverse.html was unreachable)                       #
#                                                                                               #
# Rev:      1.2.1                                                                               #
# Date:     2008-03-25                                                                          #
# Changes:  Corrected typo in dialog. Translates tomboy's monospace to zim verbatim             #
# Rev:      1.2                                                                                 #
# Date:     2008-03-24                                                                          #
# Changes:  Much revised code. Should be more robust against Tomboy note format now. Also added #
#           support for the new "Notebooks" concept (i.e. two-level name-spaces)                #
# Rev:      1.1                                                                                 #
# Date:     2008-03-08                                                                          #
# Changes:  Fixed an issue when Create date on tomboy note does not exist. Now displays both    #
#           "Last changed" and "Create date" (if these exists) and conversion date. Fixed       #
#           various issues with that could hang the script. Added a few character subs.         #
# Filename: tzim.py                                                                             #
# Rev:      1.0                                                                                 #
# Date:     2007-07-28                                                                          #
# Changes:  First version                                                                       #
#################################################################################################
import os
import os.path
import sys
import glob
import re


def main():
    home = os.path.expanduser("~")
    tomboynotes = input("Path to gnote/tomboy notes directory (blank for default path): ")
    tomboynotes = tomboynotes.rstrip()
    if tomboynotes == "":
        if os.path.exists(home + "/.local/share/gnote"):
            # modern choice for gnote
            tomboynotes = home + "/.local/share/gnote"
        elif os.path.exists(home + "/.local/share/tomboy"):
            # modern choice for tomboy
            tomboynotes = home + "/.local/share/tomboy"
        elif os.path.exists(home + "/.tomboy"):
            # historic for tomboy
            tomboynotes = home + "/.tomboy"
        else:
            # current
            tomboynotes = "."
    tomboynotes = os.path.realpath(os.path.expanduser(tomboynotes))
    if not tomboynotes[-1] == "/":
        tomboynotes += "/"
    print("***** Reading gnote/tomboy notes from: ", tomboynotes, " *****")
    files = glob.glob(tomboynotes + "*.note")  # Read tomboy notes file names
    if len(files) == 0:
        print("No note files.")  # Exit if no note files in directory
        sys.exit()
    zimnotes = input("Path to zim notes directory (blank for current directory): ")
    zimnotes = zimnotes.rstrip()
    if zimnotes == "":
        # current
        zimnotes = "."
    zimnotes = os.path.realpath(os.path.expanduser(zimnotes))
    if not zimnotes[-1] == "/":
        zimnotes += "/"
    if zimnotes == tomboynotes:
        # avoid overlapping directory
        zimnotes += "zim/"
    print("***** Writing zim notes to: ", zimnotes, " *****")
    if not os.path.exists(zimnotes):
        os.mkdirs(zimnotes)
    elif os.listdir(zimnotes):
        print(" ---- some files exist in ", zimnotes, " ----")
    answer = input("Continue [Yes/no]? ").lower()
    if answer != "" and answer[0] != "y":
        sys.exit()
    curdir = os.getcwd()
    os.chdir(zimnotes)
    for fil in files:
        infile = open(fil, "r")
        longline = infile.read()
        infile.close()

        # --- Match note title --------------------------------------------------------
        match = re.search(r".*<title>(.*)</title>", longline, re.S)
        if match:
            title = format(match.group(1))
            print("***** Converting:", title, "*****")
        else:
            print("Title: note title could not be found")

        # --- Match tomboy note format versions ---------------------------------------
        match = re.search(r'.*<note version="(\d+\.\d+)"', longline, re.S)
        if match:
            if match.group(1) not in ["0.2", "0.3"]:
                print("Version: only tested with Tomboy note version 0.2 and 0.3")
        else:
            print("Version: Tomboy note version could not be found")

        # --- Match note text ---------------------------------------------------------
        match = re.search(
            r".*<note-content.*?>.*?\n(.*)</note-content>", longline, re.S
        )
        # ^^^^ to avoid title repeat itself
        if match:
            text = format(match.group(1))
        else:
            print("Text: note text could not be found")
            text = "*** No text found in tomboy note ***"

        # --- Match last-change text --------------------------------------------------
        match = re.search(
            r".*<last-change-date>(\d\d\d\d-\d\d-\d\d).*</last-change-date>",
            longline,
            re.S,
        )
        if match:
            last_change_date = match.group(1)
        else:
            last_change_date = "Not found"
            print("last-change-date: could not be found")

        # --- Match create-change text ------------------------------------------------
        match = re.search(
            r".*<create-date>(\d\d\d\d-\d\d-\d\d).*</create-date>", longline, re.S
        )
        if match:
            create_date = match.group(1)
        else:
            create_date = "Not found"
            print("create-date: could not be found")

        # --- Match folder (tomboy version > 0.3) -------------------------------------
        # 2018-07-28: vrubiolo: non-greedy modifier for '+' is here to support nested tags
        # (too much is matched otherwise and the potential mkdir() below for folder creation fails)
        match = re.search(r".*<tag>system:notebook:(.+?)</tag>", longline, re.S)
        if match:
            folder = match.group(1)
        else:
            folder = ""

        # --- Put together zim note ---------------------------------------------------
        outname = title
        outname = re.sub("[/&<>:; ]", "_", outname)  # removing "dangerous" chars
        outname += ".txt"  # zim file name for note
        if folder != "":
            if not os.path.exists(folder):
                os.mkdir(folder)
            outname = folder + "/" + outname
        outfile = open(outname, "w")
        line = "====== " + title + " ======" + "\n"
        line += text + "\n"
        line += "\n" + "Last changed (in Tomboy/Gnote): " + last_change_date + "\n"
        line += "Note created (in Tomboy/Gnote): " + create_date + "\n"
        outfile.write(line)
        outfile.close()
    print("\n" + "Conversion OK!")
    os.chdir(curdir)


# ------------------------------------------------------------------------------


def format(line):  # various format substitutions of lines
    line = re.sub("</?bold>", "**", line)
    line = re.sub("</?italic>", "//", line)
    line = re.sub("</?strikethrough>", "~~", line)
    line = re.sub("</?highlight>", "__", line)
    line = re.sub("</?size:(small|large|huge)>", "", line)  # Can't handle tomboy sizes
    line = re.sub("</?monospace>", "''", line)
    line = re.sub("<link:(internal|broken)>", "[[", line)
    line = re.sub("</link:(internal|broken)>", "]]", line)
    line = re.sub("<link:(url)>", "", line)
    line = re.sub("</link:(url)>", "", line)
    line = re.sub(
        '<list-item dir="ltr">', "* ", line
    )  # List handling in tomboy to complexfor this
    line = re.sub(
        "(</?list>|</list-item>)", "", line
    )  # this simple converter; generating a one-level
    line = re.sub("&gt;", ">", line)  # list only
    line = re.sub("&lt;", "<", line)
    line = re.sub("&amp;", "&", line)
    return line


main()
