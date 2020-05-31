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
 * pdf, word einlesen mit Tika in python
 * Extrahierte Texte in ES ablegen
 * `done` Watcher schreiben; er erkennt Dateiänderungen welcher Mechanismus?
  --> Anleitung: **http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/**
 * Aktualisierung von Datei-dokumenten --> Realisierung? 2. Tabelle?
 * add logging: z.B. für watcher: datei erstellt, modififiziert; für tika: datei eingelesen
 * Pip-requirements in txt-auslesen und abspeichern

