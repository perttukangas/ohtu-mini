# ohtu-mini

## Definition of Done

- Testikattavuus vähintään `80%` ja testit menevät läpi
- Koodin Pylint arvosana vähintään `9,00`
- Ominaisuus on manuaalisesti testattu
- Koodissa dokumentointi suomeksi, ja koodi englanniksi
- Pull requstin on ainakin yksi toinen ohjelmoija katselmoinut
- CI-palvelun testit menee läpi

## Alustus

### Poetry riippuvuudet

```
poetry install
```

### Ympäristömuuttujat:

Luo juureen `.env` tiedosto, jonka sisältö on vastaava:

```
DB_USERNAME=ronituohino
DB_HOST=db.bit.io
DB_DATABASE=ronituohino/ohtuminidev
DB_PORT=5432
DB_PASSWORD=<kehitystietokannan salasana>
SECRET_KEY=<salainen avain>
```

Luo juureen `.env.test` tiedosto, jonka sisältö on vastaava:

```
DB_USERNAME=ronituohino
DB_HOST=db.bit.io
DB_DATABASE=ronituohino/ohtuminitest
DB_PORT=5432
DB_PASSWORD=<testaustietokannan salasana>
SECRET_KEY=<salainen avain>
```

## Komentorivitoiminnot

### Ohjelman suorittaminen kehitystilassa

Komento: `poetry run invoke dev`

### Testaus

Komento: `poetry run invoke test`

### Testikattavuus

Komento: `poetry run invoke coverage`

### Pylint

Komento: `poetry run invoke lint`

## Julkaiseminen

### Ohjelman suorittaminen tuotantotilassa

Komento: `poetry run invoke start`

### Docker -kuvan rakentaminen

Komento: `docker build .`

### Docker -kuvan suorittaminen

Komento: `docker run -p 8080 <image id>`
