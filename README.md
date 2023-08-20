# Excel-Report-Creator
This program was developed to automate the creation of a daily report, both for the morning reports and the afternoon reports. 

AM: The program would read all Excel files (xlsx) in a directory selected by the user. Then remove certain rows based on programmed conditions. 
The remaining rows would be added to a new sheet and reorganized, adding a grand total row and creating a pivot table with this new information.

PM: The program would read all Excel files (xlsx) in a directory selected by the user. The first sheet was copied, then first sheet and copy were renamed.
Rows with programmed conditions would be dropped from the copy sheet then sheet would be sorted by first column. While getting information from another excel sheet, 
all names in one column would be checked, matched, and renamed in the copied sheet. A pivot table was then created to show info for two columns within the copied sheet,
highlighting specific information found in some rows. A grand total of how many rows were pulled would be added to the bottom row. Another pivot table would then be created
based on information within the copied sheet. The program would populate this pivot table with totals, amounts, calculations, and the companies that said information belonged to. 
A difference column was added to show the difference between totals, then the new "report" would be dumped into a newly created output folder with the new file name being the date 
in a corresponding column within the worksheet.

Top libraries used: Pandas, pywin32, openpyxl.
(See header documentation in "Afternoon_Process_20230612_v2.py")
