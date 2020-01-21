This a project that develops a portal for executing tapes and drivers using binary files and bash scripts.
The data in the company I am interning is stored in the form of cartridges instead of hard disks. A cardtrige
is a data storing device where data can be stored sequentially.The data is accessed through a pointer of a driver that traverses
the cartridge consisting of various tapes. User authentication has been implemented using LDAP.
By using pipes and subprocess feature in Python, the GUI(developed with tkinter) will show the live status of the command
being executed and the user can even interract with the binary file output in real time using pipes.
