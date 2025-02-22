# emeraldRoll
source code for my RickRoll pokemon Emerald save file

## Release
	If you just want the .sav file check under releases!

## Build
	To build the .sav file from source you need to install gvasm https://github.com/velipso/gvasm
	You will also need to be able to run python scripts, and the following python packages:
		- Numpy https://numpy.org/install/
		- Python Image Library https://pillow.readthedocs.io/en/stable/installation/basic-installation.html
		- hitherdither https://github.com/hbldh/hitherdither
		- PyNLZSS https://github.com/DorkmasterFlek/python-nlzss

	Then run makeVidData.py to generate the Data/ImageData.bin and Data/FlagData.bin
	compile the bootstrap bin with gvasm: `gvasm make bootstrap.gvasm -o build/bootstrap.bin`
	compile the payload bin 	`gvasm make payload.gvasm -o build/payload.bin`
	
	Then run SaveFileInject.py to inject all the bin files into a copy of Data/FreshSave.sav to Out/EmeraldRoll.sav
