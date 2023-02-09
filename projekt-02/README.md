# Drugi projekt - distsys

## Master wprker architecture

## Klijent

Generira se lista od 10 000 klijenata. (client ids) Ucitava dataset i uzima stupac koji sadrzi python kod. Dataset se podijeli ravnomjerno klijentima. (dict klijenata i njihov python kod) Klijenti salju zahtjeve za obradu koda. Ispisuje u konzolu za svakog klijenta prosjecan broj slova koji sadrzi sav njihov python kod.

Pokretanje servisa: python client.py

## Master servis

Pokrece na random 5-10 workera. (ovo je number of workers = N) Po pokretanju workera dodjeljuje im se id. (spremaju se u dict, potrebno da se zna koji worker je obavio sto). Servis prati broj primljenih i obavljenih zadataka. Logira se timestamp slanja i primanja taska. Salje svakom workeru po 1000 redaka.[ovo je sample size = M, task za workera] Nakon sto dobije rezultate od workera, salje sljedece redke.

Pokretanje servisa: python masterService.py

## Worker servisi

Posto se radi na lokalnoj masini potrebno je “simulirati” delay mreze. Kad worker dobije i vraca obavljeni task na random ceka 0.1 - 0.3 sekunde. Worker racuna broj rijeci u python “fileu” . (ala “word counter”)

Pokretanje servisa: python worker1.py, python worker2.py...