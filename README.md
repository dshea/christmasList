# christmasList
Christmas gift exchange selector

This repository contains the Python code and data files used to select
Christmas gift exchange pairs.  Currently the Python code is in 2.7,
but I will update it to 3.x when that is delivered with most operating
systems.

# get a copy of the git repository

```
git clone https://github.com/dshea/christmasList.git
```

# run the program

```
cd christmasList
christmasList.py adult.csv
```

This will select new parings and add them to the end of the history(adult.csv)
file.

christmasList.py <history.csv> [numYears]

* history.csv - history file used to exclude recent pairings.
* numYears(optiona) - how many previous years to exclude.  Default is
  all years in the file.

# input files

## families.csv

This file is used to exclude pairings from immediate family units.
This file must be in the current working directory.

* one family on a line
* each member seperated by a comma

## history.csv

This file has the list of previous pairings. The first line is used as
the list of people to pair.  The following lines are the pairings from
previous years.  The program will append the new pairing to this file.
