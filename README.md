Program to easily copy RFID data from an SD card to an appropriate directory.

<img class=" size-full wp-image-1101 aligncenter" src="https://jevansbio.files.wordpress.com/2017/11/picture1.png" alt="Picture1" width="536" height="450" />

How to use:
<ul>
	<li>Place a text file with the name "RFIDID" (no file extension) on your SD card</li>
	<li>In that file place the following (Three columns seperated by tabs, with a header):</li>
</ul>

TYPE	SITE	ID
1	YOURSITENAME	AN_ID

<ul>
	<li>When the program is running it'll check for the presence of this file on any SD card plugged into the computer.</li>
	<li>If it detects this file and data in the form of a .DAT file, you can hit enter of click the button to automatically move that data file(so the original is removed from the SD card) to YOURFILEDIR/YOURSITENAME/AN_ID/STARTDATETIME_ENDDATETIME/</li>
</ul>

NOTES:
<ul>
	<li>Installer currently windows only. I can create a Mac version if there is interest and I can persuade a Mac owning friend to let me compile apps on their machine.</li>
	<li>Currently assumes RFID data is in a .DAT file, will not find other file formats. This could be genericised. Similarly, the first column is assumed to be the date time</li>
	<li>The "TYPE" column does nothing in the published version (in my lab it is used to distinguish between two different types of board producing two different output files, reading them differently and placing them in different locations). Once again this could be genericised in future versions if people would find this feature useful. Potentially this could also be modified to work with non RFID data/multiple files.</li>
</ul>
Please let me know if there are any issues or if you have any suggestions.
