from gpanel import *

raw_minutes = input("Bitte Anzahl der Minuten eingeben, die in Stunden und Minuten umgerechnet werden sollen.")

computed_days = raw_minutes//60//24
computed_hours = (raw_minutes//60) - (computed_days*24)
computed_minutes = raw_minutes%60

print(raw_minutes, "Minute(n) entsprechen",computed_days, "Tag(n),", computed_hours, "Stunde(n) und", computed_minutes, "Minute(n)")