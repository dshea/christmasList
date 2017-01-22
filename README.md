# christmasList
Christmas gift exchange selector program

This repository contains the Python code and data files used to select
Christmas gift exchange pairs.  Currently the Python code is in 2.7,
but I will update it to 3.x when that is delivered with most operating
systems.

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
* numYears(optional) - how many previous years to consider.  Default is
  all years in the history file.

# Input files

## families.csv

This file is used to exclude pairings from immediate family members.
This file must be in the current working directory.

* one family on a line
* each member seperated by a comma

## history.csv

This file has the list of previous pairings. The first line is used as
the list of people to pair.  The following lines are the pairings from
previous years to exclude.  The program will append the new pairing to this file.

* the first line is the people in the gift exchange. You must have this
  line and the first column is ignored.
* the first column is the year
* the rest of the columns are the selections for the people in the
first row for that year

