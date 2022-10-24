from gpanel import *

year = input("Bitte geben Sie das Jahr an");

schaltjahr = False;


if (year % 4 == 0):
    schaltjahr = True;
    
    if (year % 100 == 0): 
        schaltjahr = False;
        if (year % 400 == 0):
            schaltjahr = True;

        


if (schaltjahr):
    print("Das angegebene Jahr ist ein Schaltjahr und hat 366 Tage");
else:
    print("Das angegebene Jahr ist KEIN Schaltjahr und hat 365 Tage");