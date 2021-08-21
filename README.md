# Hydrocarbonator
An attempt at writing a parser for Single Chain Organic Compounds 

Motivation:
  IUPAC uses a really systematic form of nomenclature for organic compounds, I figured that this could be _**somewhat**_ implemented into a program.
  The reason for it being boiled all the way to single chain is because I still haven't thought of a way to make it able to detect and identify double cyclic or stacked compounds.
  Also I seriously needed to limit the scope for this if I wanted it to be finished by a certain deadline.
  
**NOTE** : Current Version (SCV3) **Only** detects and names pure hydrocarbons and not any functional groups.
TODO:
+ ~~A *better* parseResult object~~
+ ~~*Simplify* Hydrogen counting~~
+ ~~*Simplify* Node Making~~
+ ~~Figure out hierarchy to get Cascading Unsaturation Naming~~
+ ~~regex-ify~~ 
+ Add Caching with a db
+ Add Massive List of Examples

Result:


![](https://media.discordapp.net/attachments/864011471565619280/878394699986124840/unknown.png?width=1256&height=600)