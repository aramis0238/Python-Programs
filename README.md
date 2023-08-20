# Negotiation-Calculator
This is a specially-made program, tailored to the business need of a law firm. 
This program has different entry boxes where a user can calculate a principal amount of money, settlement amount,
down payment (if any), amount of payments, and payment date. A custom monthly payment can also be added so that the number of payments 
will change according to how much the custom monthly payment is (note: custom monthly replaces need for number of payments entered, automatically handled).
Once the 'calculate' button is pressed, a table is populated that displays the first and last payment with all the monthly payments in between. 
It also displays all the payments according to their months (example: 1. 08/23/2023  $559.96
                                                                      2. 09/23/2023  $559.96)

There are drop-downs available so that the user may add extra information to this table. 
The purpose of the content in the table is to be copied into the information database.

All calculations are handled automatically as well as table information population.

Top libraries used: customtkinter, math, datetime. (see header documentation in "Negotiation-Calculator_20230714_v12.py"
