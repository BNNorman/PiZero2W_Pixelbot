# readme.md

The Pi Zero uses threading to achieve its functionality.

One thread is used to handle the HttpServer polling and a second is used to run the Python interpreter which uses exec() ro actually run the uploaded program. 

## HttpServer

This serves just one file from the folder **web pages**. The file is called **Editor.html** which presents the caller with options to download the current program or upload another. It also has a selection of example programs you can upload to the Pixelbot, if you wish. Editor.html is a variation on the web page used by Rob Miles' PICO_pixelbot code.

HttpServer passes uploaded programs to the interpreter.py program to be stored and executed by the Pi Zero.

## Interpreter

This program runs uploaded user programs using python exec() it provides access to the hardware using a globals dictionary which gives the user program access to the following classes:-

- motors - which provides control over the Pixelbot motors.
- neopixels - which proviudes control over the 12 neopixel ring
- speaker - which just plays notes
- mqtt  which enables message passing between Pixelbots or a controller
- distance() which returns the distance sensor reading (mm)
- myname() which returns the name of the Pixelbot (see Config.py)
