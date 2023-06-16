
# pollwizard
University group project: Web application for conducting surveys and voting.

![App](https://i.imgur.com/tY9fCn4.png)
## Setup
* Install Python3
* Install Node.JS
* Install MySQL
* Create database and app user 
* Clone this repository
```bash
git clone https://github.com/kreedyX/pollwizard
```
#### Backend setup
* In "backend" directory create ".env" file containing following variables:
```ini
# DB Config
db_user = <db_appuser>
db_pass = <db_password>
db_host = 127.0.0.1
db_port = 3306
db_name = <db_name>
# JWT Config
secret = 92fdc312748bb9b62df6a2ac76f68b248c3dedc79cbf5173797572813d16c47a
algorithm = HS256
```
* Open terminal in "backend" directory
* (optional) Create Python virtual environment and activate it
```bash
python3 -m venv env
env/Scripts/activate
```
* Install python modules
```bash
pip3 install -r requirements.txt
```
* Run backend server
```bash
uvicorn main:app --reload
```

#### Frontend setup
* Open terminal in "frontend" directory
* Install packages
```bash
npm install
```
* Run frontend server
```bash
npm run dev
```

