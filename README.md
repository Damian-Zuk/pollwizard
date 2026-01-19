
# pollwizard
Web application for creating single-question polls and voting.

#### Technologies used:
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Redis
* React.js
* Bootstrap

<br />

![App](https://i.imgur.com/tY9fCn4.png)

# Setup

Create `.env` file with following content:
```ini
db_host = postgres
db_user = <db_user>
db_pass = <db_pass> 
db_port = 5432
db_name = pollwizard

redis_host = redis
redis_port = 6379
redis_pass = <redis_pass>

jwt_secret = <256 bit secret key>
jwt_algorithm = HS256
jwt_access_token_time = 300
jwt_refresh_token_time = 600
jwt_redis_index = 0

rate_limiter_redis_index = 1
```


## Docker setup

### Backend setup
```
docker compose up --build
```

### Frontend setup
```
docker build -t react-app .
docker run -p 5173:5173 react-app
```

## Manual setup
### Environment setup
* Install Python
* Install Node.JS
* Setup PostgreSQL database
* Setup Redis server
* Create Python virtual environment (`backend` directory):
```
python -m venv venv
./venv/Scripts/activate
```

### Backend setup
* Install python modules:
```
pip3 install -r requirements.txt
```

* Run the server:
```
uvicorn main:app --reload
```

* You can visit URL below to view Swagger generated API documentation:
```
http://127.0.0.1:8000/docs
```

#### Frontend setup
* Install packages:
```
npm install
```

* Run the server:
```
npm run dev
```
