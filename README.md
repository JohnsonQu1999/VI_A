# VI_A
Virtual Interface

=== TODO ===

• Get a working live feed

• Integrate the feed and control program into a GUI

• Integrate the programmer via scripting - see altera reference

• Implement serial monitor control of program to assert certain pins.

Note: As the Arduino UNO only has 12 pins this program will only implement KEY[0..3] and SW[0..7]. It would take 66 pins to implement all 4 keys, 10 switches, 10 ledr's and 6 7-segs.

Note: Actually, if I wrote an accompanying verilog top level module that students must use I could implement a custom read-write protocol. log(66)/log(2) = 7 bits to select which pin. 1 bit read. 1 bit write. 1 bit data. For a total of 10 bits which could actually work! Lets just stick with the video feed for now though because I don't think tkinter can update that fast...

=== DONE ===

• Create a working python program to control the Arduino via serial to assert/deassert pins
