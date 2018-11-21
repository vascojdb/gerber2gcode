# gerber2gcode
 
* [Intro](#id1)
* [Software](#id2)
* [Hardware](#id3)
* [Donate](#id10)


## Intro <a name="id1"></a>
gerber2gcode is an application written in Python with the single purpose of converting a Gerber SMD solder mask file into a g-code file that can be read by common 3D printers.


The 3D printer will then extrude the correct amount of solder past in the correct pads of the PCB using any method available.
In my case I have an air solder paste dispenser with a syringe and a pedal.

## Software <a name="id2"></a>
The application is written in **Python 3.7.1**. Most libraries are included with Python default installation, the only dependency that you need to install with pip is **Matplotlib 3.0.2** or later.

You can install **Matplotlib 3.0.2** by running:  
`python -m pip install -U pip`  
`python -m pip install -U matplotlib`

The current version (v0.3) only accepts RS274X Gerber ZIP files created in Labcenter Electronics Proteus.  
But hopefully I will have time to adapt the code to other software like Eagle, etc.


<a href="http://www.youtube.com/watch?feature=player_embedded&v=GD7z5hcu2xU
" target="_blank"><img src="http://img.youtube.com/vi/GD7z5hcu2xU/0.jpg" 
alt="SmartiXX R&D #1 - gerber2gcode v0.3" width="240" height="180" border="10" /></a>


| Version | Features | Supported Gerber |
|:-------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| 0.1 | Initial version<br>Basic ZIP operations<br>Gerber file parsing | RS274X Gerber (Labcenter Electronics Proteus) |
| 0.2 | Image generation of pads | RS274X Gerber (Labcenter Electronics Proteus) |
| 0.3 | Image of pads now has sizes according to pad area<br>Image of pads has vectors for 3D printer movement<br>G-Code generation for Marlin-based printers<br>Code optimization, comment optimization | RS274X Gerber (Labcenter Electronics Proteus) |


| Future features and TODO's | Date proposed |
|--------------------------------------------------------|---------------|
| Add support to Eagle Gerber files | 2018/11/21 |
| Use the correct g-code for dispensing the solder paste | 2018/11/21 |


If you feel like helping the project, **feel free to contribute**!

## Hardware <a name="id3"></a>
For this project you will need the following (or similar) equipment:
* Tronxy X1 3D printer (modified: head removed and replaced with an adapter for the syringe)
* YDL-983A solder paste dispenser

**NOTE:** Currently I did not have time yet to assembly and complete the hardware build. But it is planned for my next free time slots.

## Donate <a name="id10"></a>

If you like this project, help us make it even better by donating!

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/vascojdb)