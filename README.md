# GUI__VISUALISATION_SDSOC
Minimal GGUI for real-time visualisation of outputs generated from Hardware connected to a host machine. Part of B-tech project.  

Requirements
  1. Host machine with python (>=3.6 with matplotlib,numpy,PIL, tkinter)
  2. 7 series board compatible of running linux (use ZC706 if you want to test with the given baord files )

Steps to run the GUI  
Board setup : Connect board to a host machine via Ethernet and UART. 
  1. Set an ip to the board by  doing "ifconfig eth0 192.168.0.10" (This can be done by booting linux on the board and sending the command through UART)
  2. Check if you can ping the board at this IP from your host machine's cmd.
  3. The code is written for a windows host machine. For a linux machine, replacing 'pscp' to 'scp' in the mod_display.py should work.  
  
Board Side
1. Make sure the board can linux running on it. (tested config : ZC706 with petalinux)
2. Copy the files in the "Board Files" folder to an sd-card.ALong with that, add the weights file, and the Dataset(Set-1 or Set-2) to the sd_card. Plug the sd-card and start.
3. Set ip to the board "ifconfig eth0 192.168.0.10"
4. cd /mnt
5. ./preprocess.elf  
Host side  
6. Open cmd and run 'python mod_display.py'
7. Press Start to start collecting data.

Dataset to copy to sd-card for testing + trained weights can be found in :

https://drive.google.com/drive/folders/1flzs1jIbuw9Pihx-LV9laus2SOMgN1Br?usp=sharing



You can modify this code to visualize whatever type of data you want while keeping the overall framework intact.
