# EM---calculator
Calcualtor for solving EM equations and problems.

## Supported Calculation
You can use this calculator to calculate problem given below:
1. Transmited and reflected wave perpendicular to surface for multiple interface
2. Transmited and reflected wave at any angle. Only for two medium. Support for general boundary plane(__not just in z = 0, y = 0, or x = 0__)
<br></br>
__Notes__: For detailed explaination on implemented calculation and mode, refer to docs. (For now the docs is incomplete)

# Installation
To install, just clone this repository
```
git clone https://github.com/AdityaP1502/EM---calculator
```
__No extra packages are needed__, unless you want to run experimental features. For experimental features, numpy is needed. 
# Run
to run the program, go to EM--calculator dir and run
```
python start.py
```
__Notes__ : Tested on python 3.10.2. It seemed there are error on type alias when using python 3.8.10. So probably won't work for any older version too. 
# Further Works
1. Complete the documentation
2. Support for a much more genereal surface, not just plane, will be added in experimental mode. (Side)
3. Mode for section 7 calculation : Transmission Lines. (Main)
