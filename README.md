# Hydrocarbonator
An attempt at writing a parser for Single Chain Organic Compounds 

Motivation:
  IUPAC uses a really systematic form of nomenclature for organic compounds, I figured that this could be _**somewhat**_ implemented into a program.
  The reason for it being boiled all the way to single chain is because I still haven't thought of a way to make it able to detect and identify double cyclic or stacked compounds.
  Also I seriously needed to limit the scope for this if I wanted it to be finished by a certain deadline.
  
**NOTE** : Current Version **Only** detects and names single chain *Pure* Hydrocarbons (Not Dienes (;-;)) [Alkanes, Alkenes, Alkynes].
Reason being that the underlying code got too yucky before I could realistically build on it and the identification class is something to work on. As for now
the naming depends only element count data (identified from the chain) rather than pattern which is the end goal.

TODO:
+ A *better* parseResult object
+ *Simplify* Hydrogen counting
+ *Simplify* Node Making
+ Figure out hierarchy to get Cascading Unsaturation Naming
+ regex-ify this at some point. [100% sure this'll solve the entire issue in like 1 file lol]

Result:


![](https://media.discordapp.net/attachments/616572053994340364/845921881743425566/unknown.png)