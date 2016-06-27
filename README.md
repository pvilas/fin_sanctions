# fin_sanctions

Interface for query the lists of UN, EU and US persons, groups and entities subject to financial sanctions.

The project aims to compliment the EU regulations in the sense of detect similitudes between a given name and the lists.

We use the Levenshtein distance in order to detect matches. We can pass the distance on the *distance* parameter of the query.



## Lists
- [EU](http://eeas.europa.eu/cfsp/sanctions/consol-list/index_en.htm)
- [UN](https://www.un.org/sc/suborg/en/sanctions/un-sc-consolidated-list)
- [US](https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml)


## Installation

Clone fin_sanctions
```
git clone https://github.com/pvilas/fin_sanctions
```

Install and activate the python virtual environment
```
cd fin_sanctions
sudo pip install python-virtualenv
virtualenv venv
. venv/bin/activate 
```

Install required packages
```
pip install Flask
pip install Flask-admin
pip install Flask-SQLAlchemy
pip install Flask-security
```

> Optional: If you like to use Sublime Text editor, make link on the local directory
```
ln -s "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl" /usr/local/bin/sublime
sublime .
```

Now you can create the database, sqlite by default. Follow the script instructions.
Each time you run make_db the script tries to make a backup before to recreate the db,
so the first time will report an error, just ignore.
```
source make_db.sh
```

If none error happens, you would take a look at the database structure
```
sqlite3 fin_sanctions/list.db
.tables
.quit
```


Run the flask server
```
source run.sh
```





