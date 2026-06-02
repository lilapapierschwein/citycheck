# Anforderungsanalyse

## Vorlage zum Projekt 1 - Datenanwendung mit Python

_Diese Vorlage hilft Ihnen, die wichtigsten Aspekte Ihres Projekts vor Beginn der Programmierung zu klären. Sie ist nicht starr. Wenn Ihnen ein Abschnitt für Ihr Vorhaben unpassend erscheint, ersetzen Sie ihn. Wenn Ihnen etwas fehlt, ergänzen Sie es. Die Anforderungsanalyse ist Ihr Arbeitsdokument - sie wächst und ändert sich mit Ihrem Projekt._

---

## 1. Projekt-Steckbrief

_Kompakter Überblick. Eine bis zwei Zeilen pro Eintrag genügen._

| **Projektname**          | citycheck                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Variante**             | [ ] A – Strompreis-Assistent<br>[X] B – Reise- und Städte-Dashboard                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Autorin / Autor**      | Kai Elsässer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Erstellt am**          | 02.06.2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Letzte Änderung**      | -                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Geplanter Tech-Stack** | **Backend:**<br> - _Python v.3.14.5_ (latest stable zu Projekbeginn) verwaltet via _uv_<br>- Datenbank: Sqlite3 (ORM Python-Bibiothek _sqlalchemy_)<br>- Datenvalidierung und -modellierung via Python-_Pydantic_<br> - Restful Api via _FastApi_<br> - Tests via _pytest_<br><br>**Frontend:**<br> - JavaScript, HTML<br>- stateful Application via _HATEOAS_ (Hypermedia as the Engine of Application State) unter Nutzung von der JS-library _htmx_<br><br>**Versionsverwaltung** via _git_ |

---

## 2. Projektziel

_Was soll Ihre Anwendung in einem Satz leisten? Zwei bis drei Sätze maximal._

> Ein:e Nutzer:in soll in der Lage sein, eine Liste an Lieblingsorten persistent zu speichern zu und editieren.
>
> Für jeden neu angelegten Ort werden die Wetterdaten und wichtige Faken (Sprache, Währung, etc.) abgerufen und ebenfalls gespeichert.
>
> Beim erneuten Aufruf werden die Daten für alle bereits hinterlegten Ort aktualisiert und zu Verfügung gestellt, auch eine manuelle Aktualisierung kann durch den:die Nutzerin angestoßen werden.
>
> Die Daten werden statistisch aufgebreitet visualisiert. (BONUS: Eine Möglichkeit zum Datenexport)

---

## 3. Funktionale Anforderungen

_Was soll die Anwendung können? Pro Punkt eine Funktion. Stichworte reichen. Versuchen Sie zu unterscheiden zwischen MUSS (Pflicht) und KANN (optional, falls Zeit bleibt)._

### Muss-Anforderungen

- Nutzerkonto anlegen und verwalten
- Orte suchen und speichern
- Wetter- und weitere Daten für Orte abrufen und speichern
- Daten statistisch aufbereiten und visualisieren

### Kann-Anforderungen (Kür)

- Möglichkeit für verschiedene Nutzerkonten per Login
- Datenexport

---

## 4. Nicht-funktionale Anforderungen

_Eigenschaften der Anwendung jenseits der reinen Funktion: Bedienbarkeit, Antwortzeit, Zuverlässigkeit, Datenschutz, Wartbarkeit. Pro Punkt ein Stichwort plus kurze Erläuterung._

| **Aspekt**      | **Anforderung in Ihrem Projekt** |
| --------------- | -------------------------------- |
| Bedienbarkeit   |                                  |
| Antwortzeit     |                                  |
| Zuverlässigkeit |                                  |
| Datenschutz     |                                  |
| Wartbarkeit     |                                  |

---

## 5. User Stories

_Beschreiben Sie typische Nutzungssituationen aus Nutzersicht. Format: "Als ... will ich ... damit ich ..." Drei bis fünf User Stories reichen._

| **Nr.** | **Als (Rolle)** | **will ich (Ziel)** | **damit ich (Nutzen)** |
| ------- | --------------- | ------------------- | ---------------------- |
| 1       |                 |                     |                        |
| 2       |                 |                     |                        |
| 3       |                 |                     |                        |
| 4       |                 |                     |                        |
| 5       |                 |                     |                        |

---

## 6. Abgrenzung

_Was wird die Anwendung explizit NICHT können? Diese Auflistung schützt Sie vor sich selbst - es ist die Erlaubnis, bestimmte Features bewusst NICHT zu bauen._

- ...
- ...
- ...

---

## 7. Datenmodell und Datenquellen

_Welche Daten verarbeitet Ihre Anwendung? Woher kommen sie? Wohin gehen sie?_

### Externe Datenquellen (APIs)

| **API-Name**  | **URL / Endpunkt**                                    | **Verwendete Felder** |
| ------------- | ----------------------------------------------------- | :-------------------: |
| Open-meteo    | https://api.open-meteo.com/v1/forecast                |          ...          |
| Open-meteo    | https://archive-api.open-meteo.com/v1/archive         |          ...          |
| Open-meteao   | https://seasonal-api.open-meteo.com/v1/seasonal       |          ...          |
| open-metao    | https://air-quality-api.open-meteo.com/v1/air-quality |          ...          |
| open-metao    | https://geocoding-api.open-meteo.com/v1/search        |          ...          |
| RestCountries | ...                                                   |          ...          |

### Eigene Datenhaltung (Datenbank / Excel)

Geplante Speicherform: **Datenbank (_sqlite_)**

Geplante Tabellen / Bereiche:

- users
  - user_id (PK)
  - username
  - email
  - home_location_id (FK)

- locations
  - location_id (PK)
  - name
  - alias_name
  - latitude
  - longitude
  - country_id (FK)
  - _is_capital_city_
  - timezone_id (FK)

- countries
  - country_id (PK)
  - country_code
  - name
  - alias_name
  - language_id (FK)
  - _capital_city_id_ (FK)
  - continent_id (FK)
  - currency_id (FK)

- languages
  - language_id (PK)
  - name

- continents
  - continent_id (PK)
  - name

- timezones
  - timezone_id (PK)
  - name
  - is_dst
  - utcoffset_seconds

- weather_statistics_daily
  - weather_statistic_id (PK)
  - location_id (FK)
  - date
  - temperature_celsius_max
  - temperature_celsius_min
  - temperature_celsius_mean
  - temperature_apparent_celsius_max
  - temperature_apparent_celsius_min
  - temperature_apparent_celsius_mean
  - sunrise_time
  - sunset_time
  - daylight_duration_seconds
  - sunshine_duratio_seconds
  - snowfall_cm
  - max_wind_speed_ms
  - cloud_cover_max_percent
  - cloud_cover_min_percent
  - cloud_cover_mean_percent

---

## 8. Datenschutz und Datensicherheit

_Welche Daten könnten potenziell schutzwürdig sein? Wie schützen Sie sie? Stichworte zu: Speicherort, API-Schlüssel, Eingabevalidierung, Datensparsamkeit._

| **Aspekt**                           | **Maßnahme in Ihrem Projekt** |
| ------------------------------------ | ----------------------------- |
| Welche schutzwürdigen Daten gibt es? | Personenbezogene              |
| Wo werden sie gespeichert?           |                               |
| Wie sind API-Schlüssel geschützt?    | -                             |
| Wie werden Eingaben validiert?       |                               |
| Werden Daten an Dritte übertragen?   |                               |

---

## 9. Risiken

_Was könnte schiefgehen? Technische Risiken, Zeitrisiken, fachliche Lücken. Pro Risiko: Was ist das Risiko? Wie wahrscheinlich ist es? Was tun Sie dagegen?_

| **Risiko** | **Wahrscheinlichkeit** | **Gegenmaßnahme** |
| ---------- | ---------------------- | ----------------- |
|            |                        |                   |
|            |                        |                   |

---

## 10. Architektur-Skizze (in Stichworten)

_Welche Module planen Sie? Welche Aufgabe hat jedes Modul? Wie wirken sie zusammen? Eine grobe Liste reicht - eine richtige Skizze als Bild können Sie später anhängen._

| **Modul** | **Aufgabe**                  |
| --------- | ---------------------------- |
| main.py   | Einstiegspunkt der Anwendung |
|           |                              |
|           |                              |
|           |                              |
|           |                              |

---

## 11. Reflexion am Projektende

_Diesen Abschnitt füllen Sie am letzten Tag aus - er ist die Grundlage für Ihre Präsentation. Vergleichen Sie ehrlich, was Sie geplant hatten und was tatsächlich entstanden ist._

### Was wurde umgesetzt?

---

### Was wurde nicht umgesetzt – und warum?

---

### Wichtigste Designentscheidungen mit Begründung

---

### Stärken des Ergebnisses

---

### Schwächen / Lehren für das nächste Mal

---

### Potenziale – was wäre der nächste sinnvolle Schritt?

---

_Diese Vorlage darf frei angepasst werden. Sie ist ein Hilfsmittel, kein Selbstzweck._
