# ohtu-mini

## Definition of Done

* Testikattavuus vähintään `80%` ja testit menevät läpi
* Koodin Pylint arvosana vähintään `9,00`
* Ominaisuus on manuaalisesti testattu
* Koodissa dokumentointi suomeksi, ja koodi englanniksi
* Pull requstin on ainakin yksi toinen ohjelmoija katselmoinut
* CI-palvelun testit menee läpi

## Komentorivitoiminnot

### Riippuvuuksien asentaminen

Komento: `poetry install`

### Ohjelman suorittaminen kehitystilassa

Komento: `poetry run invoke dev`

### Testaus

Komento: `poetry run invoke test`

### Testikattavuus

Komento: `poetry run invoke coverage`

### Pylint

Komento: `poetry run invoke lint`

## Komentorivitoiminnot julkaisuun

### Ohjelman suorittaminen tuotantotilassa

Komento: `poetry run invoke start`

### Docker -kuvan rakentaminen

Komento: `docker build`

### Docker -kuvan suorittaminen

Komento: `docker run -p 8080 <image id>`
