people = {"Emma": 1996,
          "Anna": 2002,
          "Toni": 1985,
          "Lena": 1967,
          "Jakob": 2001,
          "Oliver": 2007,
          "Selina": 1991,
          "Felix": 1970,
          "Luisa": 2003,
          "Moritz": 1956};

jungest = ("", 0);
sum = 0;


for key,value in people.items():
    if value > jungest[1]:
        jungest = (key, value);

    sum += 2022-value;

msgDlg("Von allen Personen, die ich kenne, ist " + jungest[0] + " mit " + str(2022 - jungest[1]) + " Jahren am jüngsten.");
msgDlg("Alle Personen, die ich kenne, sind zusammen " + str(sum) + " Jahre alt.");