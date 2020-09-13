# SearchEngine_ElasticSearch_Transformer

Das Repo beinhaltet eine Suchmaschine, die auf ElasticSearch (ES) basiert. Darüber hinaus können Antworten auf Fragen(mithilfe eines Transformers auf Grundlage der Daten in ES extrahiert. Die GUI ist Browser-basiert und wurde mit Flask erstellt.

## Dieses Repo basiert in erster Linie auf folgenden Repos

- Haystack: https://github.com/deepset-ai/haystack
- Building-a-search-engine-using-Elasticsearch: https://github.com/dineshsonachalam/Building-a-search-engine-using-Elasticsearch
- 


## Nutzung

### Einrichtung

- conda env `flask` erstellen:
  *  erstelle conda env `flask` mit python=3.6
  * Install flask `conda install -c anaconda flask`
  * Klone haystack-Repo https://github.com/deepset-ai/haystack
  * Aktiviere conda env `flask`
  * Wechsle in das haystack-Repo und installiere das Repo über pip: `(flask) $ pip install --editable .`
  * Installiere watchdog in env `flask`: `pip install watchdog`
  * Installiere Tika in env `flask`: `pip install tika`

### Daten einlesen (einmalig)
1. ES mithilfe von Docker starten
'''
$ docker-compose -f docker-compose_dev.yml up
'''
2. Index in ES erstellen. Dabei wird ein Index `document` erstellt. Dafür das Skript `create_new_index.py` ausführen. In der Ausgabe sollte drinnen stehen, dass ein neuer Index erstellt wurde.
3. Daten einlesen (die Daten müssen als `.txt`-Datei vorliegen; pro Datei ein Artikel). Das Skript `Load_data_2_DB.py` ausführen. Zum Überpüfen, ob die Dokumente hochgeladen wurden kann auf der Kommandozeile folgender Befehl eingegeben werden:
```
$ curl -GET 'localhost:9200/_cat/indices'
```
als Output sollte man sowas in der Art erhalten:
```
yellow open document IAQUCD3IQGOC8pywOFU5_A 1 1 2811 0 3mb 3mb
```
Hierbei sind im Index `document` `2811` Einträge vorhanden.


### "Normale" Nutzung (*ohne* Daten einlesen
1. ES mithilfe von Docker starten
'''
$ docker-compose -f docker-compose_dev.yml up
'''
2. conda env `flask` starten und `(flask) $ python3 app.py` ausführen um den App-Server zu starten
3. Unter http://localhost:8005 kann auf die Suchmaschine zugegriffen werden.

## Nützliche Befehle
- Eintrag mit der doc_id "3f465bd5a1b454ddf51064502acea077" suchen:`curl -X GET "localhost:9200/document/_search?q=doc_id:3f465bd5a1b454ddf51064502acea077"`

# TODOs

- `done` Entfernung des Scrapers 
- `done`Daten einfügen: GoT-Daten von Haystack example
-  `done` flask auf GoT-Daten anpasssen
- `done` QA-Modell einbauen
- `done` deutsche Wikepedia Daten in ES schreiben
- dt. distillbert-Modell auf QA-trainieren
	6.1. Model nochmals komprimieren? --> https://snappishproductions.com/blog/2020/05/03/big-models-hate-this-one-weird-trick-quantization-t5-pytorch-1.4.html.html --> Komprimiert Model, aber kein Vorteil beim Inferenz.
- haystack-retriever in der index()-Functionen mit der bisherigen Variante refactoren
- `done` Eigenes Repo anlegen --> ``SearchEngine_ElasticSearch_Transformer
- Inferenzzeit reduzieren:
	* ONNX?
- Einlesen aller Dateien (pdf, Word, powerpoint) mithilfe von Tika und Ablegen der Extrahierten Daten in ES:
 * `done` pdf, word einlesen mit Tika in python
 * add ppt, word, excel?, txt files to tika
 * `done` ES hat Probleme mit / bei der Suche, daher versuchen den Pfad als Namen eindeutig in einen String zu konvertieren-hashen?** --> **https://www.geeksforgeeks.org/md5-hash-python/
 
 * `done` Extrahierte Texte in ES ablegen
 * `done` Watcher schreiben; er erkennt Dateiänderungen welcher Mechanismus?
  --> Anleitung: **http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/**
 * `done` Aktualisierung von Datei-dokumenten --> Realisierung? 2. Tabelle?
- `done` add logging: z.B. für watcher: datei erstellt, modififiziert; für tika: datei eingelesen
- Pip-requirements in txt-auslesen und abspeichern
- `done` Watcher erkennt nur Dateiänderungen ab dem Zeit seitdem er läuft --> Zu Beginn müssen der Watcher einmal durchlaufen und alle Dateien einlesen
- `done` Angenommen der Watcher läuft nicht die ganze Zeit, dann können die Datei-Änderungen nicht getracked und in ES upgedated werden. --> z.B. extra Feld mit "zuletzt gändert". Weiteren Ansatz ausdenken  
- `done`in watcher.py: für es client eine Klasse anlegen
- Watcher in allen Kombis testen wenn er _ausgeschalten_ war
    * `done` ob neue Dateien eingelesen werden
    * `done` alte Einträge aus DB gelöscht werden
    * `done` modifizierte Dateien geupdated werden
    * `done` rekursiv testen
- Watcher in allen Kombis testen wenn er _eingeschalten_ ist
    * `done`  ob neue Dateien eingelesen werden
    * `done` alte Einträge aus DB gelöscht werden
    * `done` modifizierte Dateien geupdated werden
    * `done` rekursiv testen
- `done` dev_read_data_with_tika in master mergen
- testen, ob mit farm finegetunete Modelle von Huggingface akzeptiert werden (z.B. Bert-Squad)
  * Falls ja, 1. Bert mit Huggingface finetunen (SquadGerman , eigener Datensatz) und prunen **https://github.com/huggingface/transformers/blob/master/examples/movement-pruning/README.md**
- **neuen dt. SQUAD-like Dataset erstellen (software erstellen, die dafür genutzt werden kann)**
- **hier weiter machen** Suchseite zu anpassen, dass neue Komponenten für einen Sucheintrag (z.B. Dateipfad) hinzugefügt werden können (--> html anpassen)
- Auf german squad fine-getunede Modelle einbinden
- alles in einen Docker-Container packen
- [optional] Ggf neuen Datensatz erstellen mit labelling Tool von haystack https://github.com/deepset-ai/haystack
- Labelling Tool für auf SQUADv2-Datensatz anpassen (plausible answers)




