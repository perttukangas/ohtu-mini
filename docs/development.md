# Kehitysympäristön setuppaaminen

Varmista, että sinulla on asennettuna [Python (>=3.8)](https://www.python.org/),
[Poetry](https://python-poetry.org/), ja
[postgresql (lisää ohjeita alla)](https://www.postgresql.org/)

## Poetry riippuvuudet

Mene projektin juureen, ja asenna kehitysriippuvuudet komennolla

```
poetry install
```

## Ympäristömuuttujat

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

## Paikalliset tietokannat

### Tietokantapalvelimen asennus

Tarkista, onko sinulla asennettuna postgresql.

```
sudo systemctl status postgresql
```

Vastauksena pitäisi tulla jotain tietoa palvelusta, ja tiedoissa pitäisi lukea
`Active: active (exited)`

postgresql:n pystyy asentamaan komennolla:

```
sudo apt-get -y install postgresql
```

Jos yllä oleva ei toimi, katso lisää tietoa:
https://www.postgresql.org/download/

### Tietokantojen alustus

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

### Ohjelman suorittaminen kehitystilassa

Käynnistä kehitystila komennolla

```
poetry run invoke dev
```

Ohjelman pystyy avamaan selaimella osoitteessa http://127.0.0.1:5000
