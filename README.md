# NFT LISTENER

Basic NFT Blockchain app, using Web3.py.

Listen and record transfer events for Bored Ape Yacht Club (BAYC) NFTs


### Following must be installed:

- Docker


### Steps to run:

1. Sign up for a free account at Infura.io.
2. Obtain your free API Key.
3. Clone the repo `git clone git@github.com:jonathantumulak/nft-listener.git`
4. Open terminal and cd into the directory
5. Create .env file and copy contents of env.example
6. Change value of `SECRET_KEY` to some random string if needed.
7. Change the value of `INFURA_API_KEY` to the API key you received from Infura.io
8. Run project with command `docker compose up --build -d`
9. Open `http://localhost:8000/` on a web browser to access the app
10. To run management command to fetch transfer events, use the command:

    `docker compose run --rm web ./manage.py fetchevents --start_block START_BLOCK --end_block END_BLOCK`
11. To run management command to listen for new transfer events, use the command:

    `docker compose run --rm web ./manage.py listenevents`
12. Once database has been filled with transfer events, 
open `http://localhost:8000/api/filter-transfer-events/<token_id>` to retrieve transfer events of a token id as a json list


Commands:

To run via docker:

```
docker compose up --build -d
```

To migrate database:

```
docker compose run --rm web ./manage.py migrate
```

To create superuser:

```
docker compose run --rm web ./manage.py createsuperuser
```

To fetch transfer events:

```
docker compose run --rm web ./manage.py fetchevents --start_block START_BLOCK --end_block END_BLOCK
```

To listen for new transfer events:

```
docker compose run --rm web ./manage.py listenevents
```

To stop containers:

```
docker compose down
```
