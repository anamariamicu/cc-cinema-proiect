Proiect CC - Serviciu pentru rezervarea biletelor la cinema

Membri echipa:
- Cornea Doru-Andrei - MTI
- Micu Ana-Maria - SSA
- Paduraru Razvan-Stefan - SSA

Tematica proiectului:
Proiectul presupune crearea unei aplicatii pentru rezervarea si cumpararea
de bilete la cinema. Implementarea va presupune formarea mai multor componente,
folosirea unor componente deja existente si legarea acestora folosind Docker.

Link-uri utile:
Proiectul poate fi gasit pe:
- GitHub: https://github.com/anamariamicu/cc-cinema-proiect
- DockerHub:
    - https://hub.docker.com/r/anamariamicu/cc-cinema-proiect-server
    - https://hub.docker.com/r/anamariamicu/cc-cinema-proiect-auth
    - https://hub.docker.com/r/anamariamicu/cc-cinema-proiect-admin
    - https://hub.docker.com/r/anamariamicu/cc-cinema-proiect-interface

Arhitectura proiectului:
Proiectul este alcatuit din mai multe componente ce vor comunica intre ele
prin intermediul mai multor retele. O schema a acestora si a relatiilor
dintre ele poate fi vizualizata in fisierul "diagram.png".

Descrierea serviciilor:
- auth: serviciu de autentificare pe baza de token; in cadrul aplicatiei
exista doua roluri: utilizator obisnuit si admin; endpoint-urile ce necesita
securizare vor fi create folosind un "decorator" care va verifica mai intai
utilizatorul are permisiunile necesare pentru a accesa acea functionalitate
- admin: pune la dispozitie endpoint-uri pentru admin (ex: adaugarea unei
sali de cinema, adaugarea unui film, adaugarea unei proiectii de film,
vizualizarea stadiului rezervarilor, etc.)
- server: pune la dispozitie endpoint-urile pentru client; acestea pot fi
accesate si de admin (ex: rezervarea unui bilet, vizualizarea tuturor
proiectiilor de film disponibile, vizualizarea propriilor rezervari, etc.)
- kong: API gateway ce expune endpoint-urile implementare in serviciul de
autentificare, in serviciul "server" si in serviciul "admin"
- bd: serviciu de stocare si persistenta pentru datele folosite
de toate celelalte servicii (MySQL); tabelele ce abstractizeaza logica
aplicatiei se pot gasi in diagrama "db.png"
- interface: expune o interfata in linie de comanda pentru a putea testa
orice endpoint definit in cadrul celorlalte servicii; apelarea lor se face
prin intermediul gateway-ului

Rularea proiectului:
Detalii despre modul in care poate fi rulat proiectul se gasesc in fisierul
"instructiuni.txt".