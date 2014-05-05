Team Scoot-N-Shoot Senior Design Project University of Delaware
https://sites.google.com/a/udel.edu/scootnshoot/

Scoot-N-Shoot is an open-surfing WiFi project that focuses on finding and tracking the best available WiFi network and uploading as much data securely as quickly as possible.

In this repository you will find the code responsible for signal tracking. Materials needed include:

Yagi antenna
two servos
tripod
two servos
Alpha usb dongle
Arduino Uno

The application runs as follows:
1)performs scans on all available wifi network
2)connects to strongest network
3)performs a 360 degree scan on current network, sampling signal strength as it goes
4)finds the direction of greatest signal strength after calculating a rolling average on sampled data
5)orients antenna in most optimal direction

