# Raspberry-Pi-Python-3-TM1637-Clock

This is a merge between a few TM1637 python libraries I found on github.

## Requirements
Software:
* RPi.GPIO
* requests - in case you use an external api to feed the outside temp (eg https://openweathermap.org/) in file clock_dht11.py

Hardware:
* Raspberry PI 3 B (tested) - may work on other raspberry versions.
* TM1637 7 Segment display with clock dots.

## Connections

Raspberry PI  | 4 Digit Display
------------- | ---------------
GPIO23        | CLK
GPIO18        | DIO
3V3 (or 5V)   | VCC
G             | GND

I used these pins because GND is in the middle :)

### Setup

Start by simply downloading/copying the library and the test file into the same directory on your Pi. 
Once done, be sure to check line 17 in the clock.py file:
```
self.display = tm1637.TM1637(CLK=23, DIO=18, brightness=1.0)
```
Set the value of CLK and DIO to whichever Pi GPIO pins you have used. If you copy the hardware setup below, this will work as is.

### Running

Navigate into the directory where you have stored the files you just downloaded. You can then run the program with Python3. For those unfamiliar with Linux, the following command will do the trick: 
```
sudo python3 clock.py
```

# Seven Segment Font

They are called 7-segment displays as there are 7 LEDs for each digit (segment).
One byte (7 lower bits) for each segment. The 8th bit (MSB) is for the colon and only on the 2nd segment.

```
      A
     ---
  F |   | B   *
     -G-      H (on 2nd segment)
  E |   | C   *
     ---
      D

  HGFEDCBA
0b01101101 = 0x6D = 109 = show "5"
```

** HexDigit Index is the index of character in tm1637.py HexDigits list.

Display | Bin        | Hex  | Dec | HexDigit Index
------- | ---------- | ---- | --- | ------------
0       | 0b00111111 | 0x3F | 63  | 0
1       | 0b00000110 | 0x06 | 6   | 1
2       | 0b01011011 | 0x5B | 91  | 2
3       | 0b01001111 | 0x4F | 79  | 3
4       | 0b01100110 | 0x66 | 102 | 4
5       | 0b01101101 | 0x6D | 109 | 5
6       | 0b01111101 | 0x7D | 125 | 6
7       | 0b00000111 | 0x07 | 7   | 7
8       | 0b01111111 | 0x7F | 127 | 8
9       | 0b01101111 | 0x6F | 111 | 9
A       | 0b01110111 | 0x77 | 119 | 10
b       | 0b01111100 | 0x7C | 124 | 11
C       | 0b00111001 | 0x39 | 57  | 12
d       | 0b01011110 | 0x5E | 94  | 13
E       | 0b01111001 | 0x79 | 121 | 14
F       | 0b01110001 | 0x71 | 113 | 15
G       | 0b00111101 | 0x3D | 61  | 16
H       | 0b01110110 | 0x76 | 118 | 17
I       | 0b00000110 | 0x06 | 6   | 18
J       | 0b00011110 | 0x1E | 30  | 19
K       | 0b01110110 | 0x76 | 118 | 20
L       | 0b00111000 | 0x38 | 56  | 21
M       | 0b01010101 | 0x55 | 85  | 22
n       | 0b01010100 | 0x54 | 84  | 23
O       | 0b00111111 | 0x3F | 63  | 24
P       | 0b01110011 | 0x73 | 115 | 25
q       | 0b01100111 | 0x67 | 103 | 26
r       | 0b01010000 | 0x50 | 80  | 27
S       | 0b01101101 | 0x6D | 109 | 28
t       | 0b01111000 | 0x78 | 120 | 29
U       | 0b00111110 | 0x3E | 62  | 30
v       | 0b00011100 | 0x1C | 28  | 31
W       | 0b00101010 | 0x2A | 42  | 32
X       | 0b01110110 | 0x76 | 118 | 33
y       | 0b01101110 | 0x6E | 110 | 34
Z       | 0b01011011 | 0x5B | 91  | 35
blank   | 0b00000000 | 0x00 | 0   | 36
\-      | 0b01000000 | 0x40 | 64  | 37
\*      | 0b01100011 | 0x63 | 99  | 38



## Sources
* [tm1637 I started from](https://github.com/timwaizenegger/raspberrypi-examples/tree/master/actor-led-7segment-4numbers)
* [Another good version of TM1637 library](https://github.com/Michael-Kirkpatrick/tm1637-pi-python)
* [dht11](https://github.com/szazo/DHT11_Python)

## License

Licensed under the [MIT License](http://opensource.org/licenses/MIT).
