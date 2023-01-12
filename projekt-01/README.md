# Prvi projekt - distsys

## M0 mikroservis

Fake E-ucenje API microservis (M0). Sastoji se od DB i jedne rute koja vraća github linkove na zadaće. Prilikom pokretanja servisa, provjerava se postoje li podaci u DB. Ukoliko ne postoje, pokreće se funkcija koja popunjava DB s testnim podacima (10000). Kad microservis zaprimi zahtjev za dohvaćanje linkova, uzima maksimalno 100 redataka podataka iz DB-a

Pokretanje servisa: python m0.py

## M1 mikroservis

Microservis asinkrono poziva e-učenje API (M1), te prosljeđuje podatke kao dictionary Worker tokenizer (WT) microservisu.

Pokretanje servisa: python m1.py

## WT1 mikroservis

WT microservis uzima dictionary. Uzima samo redove gdje username počinje na w i d. Prosljeđuje kod 4. microservisu.

Pokretanje servisa: python wt1.py

## M4 mikroservis

Sastoji se od rute (/gatherData) sprema se Python kod u listu. Ako ima više od 10 elemenata unutar liste asinkrono se kreiraju svi file-ovi iz liste.

Pokretanje servisa: python m4.py