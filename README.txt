Will McGinnis
WanderTechnologies.com
7/15/2012
Version 1.2.0

SerialReader desktop application
-Reads in serial data from Arduino devices
-If data is in CSV format, with time or count in column 1, real time plotting is enabled
    -Only supported for 4 channels at this time
    -Use slower updates to ensure reliabiltiy (1 line per second or so)

Built with QTdesigner, PyQT, PyQTGraph, and pySerial. Installer built with py2exe and innoIDE.  
Let me know if you want to py2exe an updated version for yourself, there is a good bit of trickery to get it to package PyQTGraph.

MIT License

Copyright (C) 7/5/2012 Wander Technologies, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.