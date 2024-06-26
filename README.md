# Hydrocarbonator
An attempt at writing a parser for Single Chain Organic Compounds 

> Motivation:
  IUPAC uses a really systematic form of nomenclature for organic compounds, I figured that this could be _**somewhat**_ implemented into a program.
  The reason for it being boiled all the way to single chain is because I still haven't thought of a way to make it able to detect and identify double cyclic or stacked compounds.
  Also I seriously needed to limit the scope for this if I wanted it to be finished by a certain deadline.



**NOTE** : Current Version (SCV3) **Only** detects and names pure hydrocarbons and not any functional groups.

## Update: 28/12

I just found out that I accidentally recreated a formatting called [SMILES](https://archive.epa.gov/med/med_archive_03/web/html/smiles.html) 
Welp ig I now know that Im going to be recreating a fully SMILE compatible formatter in the near future :D


## Running it: 

For Setup/Install

```
git clone https://github.com/ShanTen/Hydrocarbonator/
cd Hydrocarbonator
init.bat 
```
use init.sh for non windows.

To Run it

```
python nm.py
```


## Additional Features:

+ Customizable terminal interface
+ debug logger
+ Caching 

## TODO:

+ ~~A *better* parseResult object~~
+ ~~*Simplify* Hydrogen counting~~
+ ~~*Simplify* Node Making~~
+ ~~Figure out hierarchy to get Cascading Unsaturation Naming~~
+ ~~regex-ify~~ 
+ ~~BUG [Critical]: Fix priority issues~~
+ ~~Add Caching~~ (used bin file instead of db)
+ ~~Add Massive List of Examples~~

## Result:

Some screenshots from the application

![](https://raw.githubusercontent.com/ShanTen/staticHaver/master/nmSS01.png)

![](https://raw.githubusercontent.com/ShanTen/staticHaver/master/nmSS02.png)
