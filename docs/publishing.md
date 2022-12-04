# Ohjelman julkaiseminen

Ohjelman hostataan [Fly.io](https://fly.io/) palvelussa. Ohjelmalle on
määritelty automaattinen julkaisu
[GitHub Actionsien](../.github/workflows/pipeline.yml) avulla, mutta se on
mahdollista julkaista myös manuaalisesti.

Ohjelma suoritetaan [Docker](https://www.docker.com/) kontissa, jonka sisällä
sovellus käynnistyy [gunicorn](https://gunicorn.org/) palvelimella.

## Tuotantotilan testaaminen

Varmista, että sinulla on [Docker](https://www.docker.com/) asennettuna.

### Ohjelman suorittaminen tuotantotilassa

Tämä käynnistää sovelluksen [gunicorn](https://gunicorn.org/) palvelimella (vrt.
Flask kehityspalvelin)

Tämä käyttää paikallisia `.env` -määrittelyjä, joten tämä voi ihan hyvin ottaa
yhteyden kehitystietokantaan.

```
poetry run invoke start
```

### Docker -kuvan rakentaminen

Tämä rakentaa sovelluksen Docker kuvan.

```
docker build .
```

### Docker -kuvan suorittaminen

Tämä ajaa rakennetun Docker kuvan. Tämä on siis se asia, joka ajetaan
tuotantopalvelimella.

```
docker run -p 8080 <image id>
```

## Julkaisu tuotantoon

Varmista, että sinulla on [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
asennettuna.

Varmista, että ympäristömuttujat on konffattu oikein hostauspalvelussa.

```
flyctl deploy
```
