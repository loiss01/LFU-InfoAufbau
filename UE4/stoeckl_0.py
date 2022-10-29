bag = list()

while True:
    gegenstand = inputString("Du packst ein...", False)

    if gegenstand == None:
        break
    elif gegenstand > 0:
        bag.append(gegenstand)

if (len(bag) < 3):
    msgDlg("Im gepackten Koffer befinden sich " + str(len(bag)) + " Gegenstände!")
else:
    msgDlg( "Es wurden (unter anderem)\n *) " + bag[0] + ",\n *) " + bag[1] + ",\n *) ...,\n *) " + bag[-1] +"\n eingepackt.")
