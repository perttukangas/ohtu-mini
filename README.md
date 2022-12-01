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

### Ympäristömuuttujat

Luo juureen `.env` tiedosto, jonka sisältö on vastaava:

```
DB_USERNAME=postgres
DB_HOST=localhost
DB_DATABASE=ohtuminidev
DB_PORT=5432
DB_PASSWORD=supersalainensalasana
DB_SSL_CONTEXT=None
SECRET_KEY=topsekretdev
```

Luo juureen `.env.test` tiedosto, jonka sisältö on vastaava:

```
DB_USERNAME=postgres
DB_HOST=localhost
DB_DATABASE=ohtuminitest
DB_PORT=5432
DB_PASSWORD=supersalainensalasana
DB_SSL_CONTEXT=None
SECRET_KEY=topsekrettest
```

### Paikalliset tietokannat

#### Tietokantapalvelimen asennus

Varmista, että sinulla on asennettuna postgresql koneella. Vastauksena pitäisi
tulla jotain tietoa palvelusta, ja tiedoissa pitäisi lukea
`Active: active (exited)`

```
sudo systemctl status postgresql
```

postgresql:n pystyy asentamaan komennolla:

```
sudo apt-get -y install postgresql
```

Jos yllä oleva ei toimi, katso lisää tietoa:
https://www.postgresql.org/download/

#### Tietokantojen alustus

Mene tietokantapalvelimeen komennolla

```
sudo -u postgres psql
```

Luo testitietokanta komennolla

```
CREATE DATABASE ohtuminitest;
```

Luo kehitystietokanta komennolla

```
CREATE DATABASE ohtuminidev;
```

Vaihda tietokantapalvelimen salasana komennolla

```
ALTER ROLE postgres WITH PASSWORD 'supersalainensalasana';
```

Poistu tietokannasta komennolla

```
\q
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
