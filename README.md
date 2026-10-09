# GIANT — Data Analysis in STEM

Ein klickbares, Quarto-basiertes Lernmodul für das GIANT-Projekt (Uni Köln &
IISc Bangalore). Problembasiertes Lernen mit Umweltdaten, begleitet von der
KI-Lernbegleitung *Acemate*.

Diese README ist für dich als absoluten Quarto-Einsteiger geschrieben. Für die
Praktikant:in, die die Lektionsinhalte ausgestaltet, gibt es zusätzlich
[`INTERN_GUIDE.md`](INTERN_GUIDE.md).

## Was hier schon steht

- **`index.qmd`** — die Startseite/Einleitung (Layer 1): Begrüßung, wie das Modul
  funktioniert, Selbsteinschätzung, Challenge-Auswahl, Anforderungen an die
  Abschlussarbeit (Dashboard + Bericht). Inhaltlich eng an eurem bestehenden
  `Layer_1.docx` orientiert.
- **`01-…qmd` bis `08-…qmd`** — die acht Kompetenzbereiche (Layer 2), jeweils mit
  Leitfrage, Erklärung, Übungen und einem gemeinsamen Übungsdatensatz. Kapitel 1
  basiert eng auf eurem bestehenden `COURSE_OUTLINE.docx`; Kapitel 2–4 nutzen denselben
  echten Datensatz und ziehen ihn konsequent durch; Kapitel 5–8 sind ein erster Entwurf
  (siehe `INTERN_GUIDE.md` für den Status jeder einzelnen Datei).
- **`resources.qmd`** — alle externen Lernressourcen (DataCamp, r4ds, OpenIntro,
  Bogners `environmental_stat`/`statistik_uebung` usw.), aus euren bisherigen
  Link-Sammlungen zusammengeführt.
- **`data/`** — der echte Übungsdatensatz für Kapitel 1–4: offizielle Klimadaten des
  Deutschen Wetterdienstes (DWD) für fünf Bundesländer plus Deutschland, 1991–2024,
  CC BY 4.0, mit ein paar bewusst eingebauten und vollständig offengelegten
  Formatierungsfehlern für die Übungen in Kapitel 1. Siehe `data/README.md` für Quelle,
  Lizenz und volle Offenlegung.
- **`_template-lesson.qmd`** — eine leere Lektions-Vorlage mit dem Design-System, zum
  Kopieren für neue Lektionen. Erscheint nicht auf der veröffentlichten Seite.
- **`_quarto.yml`** — die Projekt-Konfiguration: legt fest, welche Dateien in welcher
  Reihenfolge im Menü links erscheinen.

## Was ist Quarto, in einem Absatz

Quarto ist ein Werkzeug, das Textdateien mit der Endung `.qmd` (Markdown-Text + Code)
in fertige Webseiten, PDFs oder Bücher verwandelt. Ihr kennt das Prinzip evtl. schon
von R Markdown — Quarto ist dessen direkter Nachfolger, vom selben Team, und
sprachunabhängig (auch Python/Julia). Ein `.qmd`-Projekt vom Typ `book` (wie dieses
hier) erzeugt automatisch eine Webseite mit Seitenleiste, Vor/Zurück-Navigation und
Inhaltsverzeichnis — also genau das "Durchklicken durch Lektionen", das du dir
vorstellst.

## Einmalig einrichten

1. **R und RStudio** (oder [Positron](https://positron.posit.co/)) installieren, falls
   noch nicht vorhanden.
2. **Quarto CLI** installieren: [quarto.org/docs/get-started](https://quarto.org/docs/get-started/)
   — für Windows/Mac gibt es einen normalen Installer. (Aktuelle RStudio-Versionen
   bringen Quarto bereits mit.)
3. In RStudio/Positron benötigte R-Pakete installieren (Konsole):
   ```r
   install.packages(c("tidyverse", "broom", "infer", "moderndive", "plotly",
                      "shiny", "shinydashboard"))
   ```
   Diese Pakete sind für die *Beispiel-Codes* in den Lektionen nötig, nicht für das
   Rendern der Seite selbst — das Rendern funktioniert auch ohne R, da der Beispielcode
   aktuell nicht ausgeführt wird, sondern nur formatiert angezeigt wird (siehe unten,
   "Code ausführbar machen").

## Lokal ansehen

Im Projektordner (dort, wo `_quarto.yml` liegt):

```bash
quarto preview
```

Das öffnet automatisch einen Browser-Tab mit der Seite — inklusive Seitenleiste,
Klick-Navigation zwischen den Lektionen, und Live-Aktualisierung bei jeder
Speicherung. So siehst du sofort, wie sich Änderungen auswirken. Zum Beenden: `Ctrl+C`
im Terminal.

Einmalig (ohne Vorschau-Server) rendern:

```bash
quarto render
```

Das erzeugt die fertige Webseite im Ordner `docs/` (bewusst so konfiguriert, siehe
nächster Abschnitt).

## Code ausführbar machen (optional, für später)

Die R-Code-Blöcke in den Lektionen sind aktuell als reine ` ```r ` -Blöcke geschrieben
— sie werden nur farbig dargestellt, aber beim Rendern nicht ausgeführt. Das ist
Absicht: so kann jeder das Projekt ohne R-Installation rendern und die Struktur prüfen.

Sobald ihr wollt, dass Code-Ausgaben (Tabellen, Diagramme) direkt in der Seite
erscheinen, ändert ihr die Codeblock-Markierung von ` ```r ` zu ` ```{r} ` — das ist
Quartos Syntax für "diesen Block wirklich ausführen". Das lohnt sich vor allem für die
Beispiel-Diagramme; bei den Übungsaufgaben (die Studierende selbst ausführen sollen)
kann reiner Anzeige-Code auch bewusst so bleiben.

## Neue Lektion hinzufügen

1. `_template-lesson.qmd` kopieren, z. B. zu `09-neues-thema.qmd`.
2. Platzhalter ausfüllen (Anleitung steht als Kommentar oben in der Datei).
3. Dateinamen in `_quarto.yml` unter `chapters:` an der gewünschten Stelle eintragen —
   erst dann erscheint die Lektion in der Seitenleiste.



## Lizenz

CC BY 4.0, wie das übrige GIANT-Lehrmaterial (Open Educational Resource, Projektziel
OP1).
