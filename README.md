
# pollwizard
<p align="center">Web application for creating polls and voting.</p>

#### Libraries and frameworks used:
* FastAPI
* React.js
* Bootstrap
* SQLAlchemy

<br />

![App](https://i.imgur.com/tY9fCn4.png)

## Setup
#### Environment setup
* Install Python.
* Install Node.JS.
* Setup SQL database
* (optional) Create Python virtual environment.

#### Backend setup
* Add the following environmental variables to the ".env" file, replacing the placeholders with your specific values.
```ini
db_user = <your_database_username>
db_pass = <your_database_password>
db_host = <your_database_host>
db_port = <your_database_port>
db_name = <your_database_name>

jwt_secret = <your_256_bit_secret_key>
jwt_algorithm = HS256
jwt_access_token_time = 600
jwt_refresh_token_time = 86400
```

* Open your terminal and install python modules.
```
pip3 install -r requirements.txt
```
* Run the server.
```
uvicorn main:app --reload
```

* You can visit this URL to view auto-generated API documentation.
```
http://127.0.0.1:8000/docs
```

#### Frontend setup
* Open your terminal and install packages.
```
npm install
```

* Run the server.
```
npm run dev
```
