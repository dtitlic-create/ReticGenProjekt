# Snake Genetics API & Arhiva

Ovaj projekt je backend sustav izgrađen pomoću **Python Flask** okvira za izračunavanje i pohranu genetike mrežastih pitona. Sustav omogućuje korisnicima da izračunaju vjerojatnost genotipa potomstva, trajno spreme te podatke u bazu podataka (SQLite) te upravljaju njima putem punog **CRUD** sustava.

## Tehnološki Stog
*   **Backend:** Python 3 + Flask
*   **Baza podataka:** SQLite + Pony ORM (Object-Relational Mapping)
*   **Genetska logika:** Prilagođeni algoritmi za izračun fenotipova i genotipova

## Funkcionalnosti (CRUD)

Aplikacija nije samo kalkulator, već i digitalna arhiva vaših legla:

*   **Create (Stvori):** `/izracunaj` (POST) – Izračunava genetiku i automatski sprema zapis u bazu.
*   **Read (Pročitaj):** 
    *   `/izracunaj/<id>` (GET) – Dohvaća specifično leglo putem jedinstvenog ključa.
    *   `/arhiva` (GET) – Izlistava sva spremljena legla iz baze podataka.
*   **Update (Ažuriraj):** `/azuriraj/<id>` (PUT) – Omogućuje izmjenu roditelja ili rezultata postojećeg zapisa.
*   **Delete (Obriši):** `/obrisi/<id>` (DELETE) – Trajno uklanja zapis iz povijesti.

