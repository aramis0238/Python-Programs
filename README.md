# PA County Cleanup
This program was developed with time efficiency in mind. The user is prompted with a small menu, displaying two buttons. 
One button allows a user to enter a county name and a starting page number they'd like to create a new PDF file from.   
The other button starts the process that prompts a user for a directory, then reads through a 'county_list' text file which contains a county name and a page number. 
The program iterates through PDFs within a user-selected directory, matching any of the county names within the text file to the content in the pdf. 
If the county name is found, the program creates a new PDF file starting at the corresponding page number that was set to the county.
These new pdf files are output into an automatically created 'output_folder'.

(See header documentation in "PACountyCleanup_20230414_v4.py" libraries showcased)
