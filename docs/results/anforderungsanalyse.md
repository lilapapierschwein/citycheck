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
| **Erstellt am**          | 02.06.2026 13:12                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Letzte Änderung**      | 03.06.2026 09:41                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
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

- Datenexport
- Möglichkeit für verschiedene Nutzerkonten per Login

---

## 4. Nicht-funktionale Anforderungen

_Eigenschaften der Anwendung jenseits der reinen Funktion: Bedienbarkeit, Antwortzeit, Zuverlässigkeit, Datenschutz, Wartbarkeit. Pro Punkt ein Stichwort plus kurze Erläuterung._

| **Aspekt**      | **Anforderung in Ihrem Projekt**                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| Bedienbarkeit   | - intuitive Bedienbarkeit durch Best-Practices im UI/UX-Design und die Umsetzung von Barrierfreieheit   |
| Antwortzeit     | - die Antwortzeit soll möglichst gering sein                                                            |
| Zuverlässigkeit | - die Anwendung soll zuverlässig laufen und Fehler dürfen nicht zum Absturz führen                      |
| Datenschutz     | - Umsetzung der Anforderungen der DSGVO                                                                 |
| Wartbarkeit     | - Wartbarkeit ist durch die Umsetzung von Best-Practices (OOP, Loose Coupling, Clean Code) zu erreichen |

---

## 5. User Stories

_Beschreiben Sie typische Nutzungssituationen aus Nutzersicht. Format: "Als ... will ich ... damit ich ..." Drei bis fünf User Stories reichen._

| **Nr.** | **Als (Rolle)** | **will ich (Ziel)**                                 | **damit ich (Nutzen)**                    |
| ------- | --------------- | --------------------------------------------------- | ----------------------------------------- |
| 1       | Nutzer:in       | eine Konto anlegen                                  | die Anwendung nutzen kann.                |
| 2       | Nutzer:in       | meine Stammdaten ändern oder löschen                | ???                                       |
| 3       | Nutzer:in       | nach Orten suchen und sie speichern                 | sie in meinen Favoriten habe.             |
| 4       | Nutzer:in       | Orte löschen                                        | uninteressante Orte nicht weiterhin sehe. |
| 5       | Nutzer:in       | die Daten (Wetter und weitere) zu einem Ort ansehen | Vergleiche anstellen kann.                |

---

## 6. Abgrenzung

_Was wird die Anwendung explizit NICHT können? Diese Auflistung schützt Sie vor sich selbst - es ist die Erlaubnis, bestimmte Features bewusst NICHT zu bauen._

- Suche nach Reise-Möglichekiten (Flüge, Zugverbindungen etc.)
- Suche nach lokalen Events zu gespeicherten Orten

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

Geplante Speicherform: **Datenbank (_sqlite3_)**

Geplante Tabellen / Bereiche:

- users
  - (PK) user_id
  - username
  - email
  - (FK) home_location_id

- locations
  - (PK) location_id
  - name
  - alias_name
  - latitude
  - longitude
  - (FK) country_id
  - (FK) timezone_id

- user_locations
  - (PK) user_location_id
  - (FK) user_id
  - (FK) location_id
  - saved_at

- countries
  - (PK) country_id
  - country_code
  - official_name
  - common_name
  - cca2
  - cca3
  - (FK) region_id
  - (FK) subregion_id
  - area_sqkm
  - tld
  - flag
  - googlemaps
  - openstreetmaps
  - population

- countries_continents
  - (FK) country_id
  - (FK) continent_id

- countries_currencies
  - (FK) country_id
  - (FK) currency_id

- capital_cities
  - (PK) capital_city_id
  - (FK) location_id
  - (FK) country_id

- countries_languages
  - (FK) country_id
  - (FK) language_id

- countries_timezones
  - (FK) country_id
  - (FK) timezone_id

- languages
  - (PK) language_id
  - name
  - iso_code
  - locale

- continents
  - (PK) continent_id
  - name
  - iso_code

- regions
  - (PK) region_id
  - name

- subregions
  - (PK) subregion_id
  - (FK) region_id
  - name

- timezones
  - (PK) timezone_id
  - name

- currencies
  - currency_id (PK)
  - code
  - name
  - symbol

- weather_statistics_daily (unique: location_id,stat_date)
  - (PK) weather_statistic_id
  - (FK) location_id
  - stat_date
  - saved_at
  - temperature_celsius_max
  - temperature_celsius_min
  - temperature_celsius_mean
  - temperature_apparent_celsius_max
  - temperature_apparent_celsius_min
  - temperature_apparent_celsius_mean
  - sunrise_time
  - sunset_time
  - daylight_duration_seconds
  - sunshine_duration_seconds
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
| Welche schutzwürdigen Daten gibt es? | E-Mail Adresse, Wohnort       |
| Wo werden sie gespeichert?           | Datenbank; Tablle _users_     |
| Wie sind API-Schlüssel geschützt?    | -                             |
| Wie werden Eingaben validiert?       |                               |
| Werden Daten an Dritte übertragen?   | nein                          |

---

## 9. Risiken

_Was könnte schiefgehen? Technische Risiken, Zeitrisiken, fachliche Lücken. Pro Risiko: Was ist das Risiko? Wie wahrscheinlich ist es? Was tun Sie dagegen?_

| **Risiko**                                  | **Wahrscheinlichkeit** | **Gegenmaßnahme**                                                                                                            |
| ------------------------------------------- | :--------------------: | ---------------------------------------------------------------------------------------------------------------------------- |
| unvollständige Implementierung (Zeitrisiko) |         mittel         | zunächst Begrenzung auf minimale Implementierung (Muss-Anforderungen)<br>Kann-Anforderungen erst anschließend implementieren |

---

## 10. Architektur-Skizze (in Stichworten)

_Welche Module planen Sie? Welche Aufgabe hat jedes Modul? Wie wirken sie zusammen? Eine grobe Liste reicht - eine richtige Skizze als Bild können Sie später anhängen._

| **Modul**    | **Aufgabe**                  |
| ------------ | ---------------------------- |
| **main.py**  | Einstiegspunkt der Anwendung |
| **core**     | Kern-Logik                   |
| **db**       | Datenbank-Verwaltung (ORM)   |
| **api**      | Bereitstellung von Daten     |
| **frontend** | Client Logik                 |

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
