# Quaderno 4

- [Obiettivo](#obiettivo)
- [Fase preliminare](#fase-preliminare)
- [Descrizione del database](#descrizione-del-database)
- [Esercizi](#esercizi)
- [Installazione](#installazione)

## Sviluppo di un'applicazione web con Streamlit e MySQL

## Obiettivo

Creare un'applicazione web in Python (Streamlit) in grado di interagire con un database MySQL in modo da eseguire interrogazioni in base alle interazioni dell'utente.

## Fase preliminare

- Avviare MySQL tramite Docker o XAMPP (vedi materiale Live Coding e Laboratorio 6)
- Importare il database
- Creare e avviare il progetto Streamlit (nuovo progetto o dal branch base del repository)
- Verificare la connessione al db attraverso le credenziali
- Suggerimento: usare st.write() per investigare i risultati ottenuti

## Descrizione del database

La base di dati si chiama PALESTRA e riguarda le attività di una palestra. Essa è caratterizzata dal seguente schema logico (le chiavi primarie sono sottolineate):

ISTRUTTORE (<u>CodFisc</u>, Nome, Cognome, DataNascita, Email, Telefono*)

CORSI (<u>CodC</u>, Nome, Tipo, Livello)

PROGRAMMA (<u>CodFisc</u>, <u>Giorno</u>, <u>OraInizio</u>, Durata, CodC, Sala)

Utilizzare l’interfaccia di phpMyAdmin per importare lo script e verificare che sia andato a buon fine. Usare l’interfaccia per esplorare la base di dati, le tabelle disponibili e i dati salvati.

## Esercizi

Creare un’applicazione multi-pagina per visualizzare le principali informazioni contenute nel database e permettere all’utente di aggiungerne di nuove. In particolare:

1. Creazione di un Homepage personalizzata che sfrutti la sintassi base del markdown (o gli elementi Streamlit) per introdurre il laboratorio/quaderno, l’obiettivo e lo studente. Sotto, riportare due grafici riguardanti le lezioni programmate: un Bar Chart che riporti il numero di lezioni per ogni slot di tempo e un Area Chart che riporti il numero di lezioni programmate in base al giorno della settimana.

2. Creazione di una pagina per la visualizzazione e filtraggio dei corsi disponibili. La pagina deve essere supportata da due metric per mostrare il numero di corsi e di tipi distinti disponibili. I widget di input devono essere creati in modo da proporre come opzioni le informazioni contenute già a database. L’utente deve poter visualizzare le informazioni sui corsi filtrando per più categorie (i.e., Tipo) e deve poter specificare il range di livello a cui è interessato. In un expander separato, visualizzare i programmi delle lezioni per i corsi selezionati e nome e cognome dell’istruttore corrispondente. In caso di risultati vuoti, bisogna stampare un errore/warning associato.

3. Creazione di una pagina per la visualizzazione degli istruttori disponibili. L’utente deve avere la possibilità di filtrare digitando il cognome dell’istruttore e utilizzando un date range per scegliere in base alla data di nascita (hint: usare datetime.date() per impostare il date_input e passare la data come stringa nell’interrogazione). La visualizzazione non deve essere una tabella complessiva, ma divisa elemento per elemento (creare un dataframe e usare df.iterrows per stampare una row alla volta, vedi Lab 6). Aggiungere un’icona per ogni risultato. In caso di risultati vuoti, bisogna visualizzare un messaggio associato.

4. Creazione di una pagina per l’inserimento di nuovi istruttori attraverso un form adatto. Usare un form d’inserimento che richiede tutti i dati necessari all’inserimento di un nuovo istruttore nella base di dati (CodFisc, Nome, Cognome, DataNascita, Email, Telefono). L’applicazione deve verificare che tutti i campi siano valorizzati tranne il Telefono in quanto opzionale (hint: convertire la data in stringa). In caso di dati mancanti, chiave duplicata o altri errori, l’applicazione deve generare un messaggio d’errore. Se invece i dati inseriti sono corretti e l’operazione d’inserimento va a buon fine, si deve visualizzare un messaggio di corretto inserimento.

5. Creazione di un form per l’inserimento di una nuova lezione settimanale nella tabella PROGRAMMA. Il form deve permettere di inserire tutti i campi necessari (CodFisc, Giorno, OrarioInizio, Durata, CodC, Sala) relativi alla programmazione di una nuova lezione. La selezione dell’istruttore deve avvenire tramite un menù a tendina contenente il codice fiscale dei possibili istruttori generato dal contenuto della tabella della base di dati. In modo analogo, anche la selezione del corso deve avvenire tramite un menù a tendina popolato dalla base di dati. Gli altri campi sono invece campi popolati manualmente dall’utente, utilizzando i widget più adatti (e.g., slider per OraInizio e Durata) o quelli testuali. L’applicazione delle verificare che l’utente non cerchi di inserire nel programma lezioni che durino più di 60 minuti e che il giorno indicato sia un giorno compreso tra Lunedì e Venerdì. L’inserimento di una nuova lezione in programma deve essere consentito ed eseguito se e solo se non sono in programma altre lezioni per lo stesso corso nello stesso giorno della settimana (hint: utilizzare i valori di input per effettuare l’interrogazione e verificare che non ci siano record). Se la richiesta di inserimento rispetta i vincoli indicati e l’inserimento termina correttamente, si deve visualizzare un messaggio di corretto inserimento, altrimenti si deve notificare un messaggio d’errore (il messaggio d’errore deve riportare il tipo di problema che ha comportato l’errore).

Tutte le pagine devono essere personalizzate con elementi di testo (utilizzando markdown o i widget pre-impostati di Streamlit) in modo da avere titoli, sottotitoli e paragrafi che evidenzino cosa viene rappresentato. Oltre a generare le interrogazioni corrette, per rendere la visione e l’interfaccia più intuitiva e organizzata, devono essere utilizzati i principali elementi di layout: expander, colonne, tab.

## Installazione

```pwsh
git clone https://github.com/66Bunz/BD-Streamlit.git
```

```pwsh
git checkout quaderno
```

Si suggerisce di creare un virtual environment (e.g., venv, pipenv).

```pwsh
pip install --user pipenv
```

Avviare il virtual env:

```pwsh
pipenv shell
```

Installare i moduli Python necessari:

```pwsh
pip install -r requirements.txt
```

Avviare l'applicazione:

```pwsh
python -m streamlit run 📒_Home.py
```

<br>
<br>
<br>
<br>
<br>

# Streamlit Tutorial: Live Coding

## Installazione completa su Windows

Vai [qui](readme_windows.md) per una guida completa all'installazione su Windows

## Installazione generica

Creazione di un'applicazione web multi-page in Streamlit interagendo con un database MySQL per visualizzare e aggiungere dati.

```pwsh
git clone https://github.com/66Bunz/BD-Streamlit.git
```

## Warm up

- Branch *live_coding* è il punto di partenza, branch *live_coding_complete* è l'applicazione finale, branch *base* come starting point per un nuovo progetto generico.

- Per ulteriori informazioni riguardo al database far riferimento a <https://www.mysqltutorial.org/mysql-sample-database.aspx>.

- Per la guida passo-passo sulla creazione dell'applicazione, dar riferimento a *guide.md*

- Per aggiungere emojii utilizzare <https://emojifinder.com> con copia-incolla.

## Environment

### Per ulteriori informazioni riguardo ai diversi OS e Streamlit: <https://docs.streamlit.io/library/get-started/installation>

#### 1. Installare l'environment MySQL (con Docker e Docker-compose <https://github.com/AndreaAvignone/mysql-docker.git>)

#### 2. Creare un nuovo virtual environment Python (e.g. *pipenv*)

Installare pipenv:

```
pip install pipenv
```

Avviare il virtual env:

```
pipenv shell
```

Installare le dependencies:

```
pip install -r requirements.txt

```

#### 3. Verificare l'installazione di streamlit

```
streamlit hello
```

Per fermare:

`Ctrl + C`

#### 4. Lanciare l'applicazione

```pwsh
python -m streamlit run 01_🏠_Home.py
```

O direttamente con il comando *streamlit*:

```pwsh
streamlit run 01_🏠_Home.py
```

Per evitare che si apri in automatico il browser:

```pwsh
streamlit run 01_🏠_Home.py --server.headless true
```
