# VI_A
Virtual Interface

=== TODO ===

• Reposition widgets to make the video feed larger

• Modularize code, fix bad code

• Try to break the program (and then fix it)

• Repackage as an executable/installer

• Handle no camera when starting program

• Handle unavailble/wrong port when starting

• Handle correct status message when file upload fails

• Handle when camera stops working while application is running

=== DONE ===

• Implement serial monitor control of program to assert certain pins.

• Create a working python program to control the Arduino via serial to assert/deassert pins

• Get a working live feed

• Integrate the feed and control program into a GUI

• Integrate the programmer via scripting - see altera reference

Note: As the Arduino UNO only has 12 pins this program will only implement KEY[0..3] and SW[0..7]. It would take 66 pins to implement all 4 keys, 10 switches, 10 ledr's and 6 7-segs.

Note: Actually, if I wrote an accompanying verilog top level module that students must use I could implement a custom read-write protocol. log(66)/log(2) = 7 bits to select which pin. 1 bit read. 1 bit write. 1 bit data. For a total of 10 bits which could actually work! Lets just stick with the video feed for now though...