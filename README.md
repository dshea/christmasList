# christmasList
Christmas gift exchange selector program

This repository contains the Python code and data files used to select
Christmas gift exchange pairs.  I finally updated the Python code to Python 3.

## Rules

* give to a different person than the last numYears
* partners can't be nuclear family members
* can't choose yourself
* participants give one gift only
* participants receive one gift only


# Get a copy of the git repository

```
git clone https://github.com/dshea/christmasList.git
```

This will get all of the files for the program and put them in the
directory "christmasList"

# Run the program

```
cd christmasList
./christmasList.py adult.csv
```

This will select new parings and add them to the end of the history(adult.csv)
file.

`usage: christmasList.py <history.csv> [numYears]`

* history.csv - history file used to exclude recent pairings.
* numYears(optional) - how many previous years to consider.  Default is 20
  years in the history file and the program ratchets down the years automatically.

# Input files

## families.csv

This file is used to exclude pairings from immediate family members.
This file must be in the current working directory.

* one family on a line
* each member seperated by a comma (no spaces)

## history.csv

This file has the list of previous pairings. The first line is used as
the list of people to pair.  The following lines are the pairings from the
previous years.  The program will append the new pairing to end of this file.

* the first line is the people in the gift exchange. You must have this
  line.  The first column is ignored.
* the first column is the year
* the rest of the columns are the selections for the people in the
first row for that year.  Look at adults.csv as an example.
