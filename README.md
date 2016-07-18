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
pip install Distance
```

The apsw provides direct access to sqlite. We will use it do get the fts and spellfix extensions. It is possible to use it with the traditional db-api python driver. The [official](http://rogerbinns.github.io/apsw/index.html) documentation is extensive. The only issue is with virtualenv, we have installed the library without the *--user* parameter. Moreover, note the enable-all-extensions option.More information is on the [download](http://rogerbinns.github.io/apsw/download.html#easy-install-pip-pypi) page.

```
pip install https://github.com/rogerbinns/apsw/releases/download/3.13.0-r1/apsw-3.13.0-r1.zip \
--global-option=fetch --global-option=--version --global-option=3.13.0 --global-option=--all \
--global-option=build --global-option=--enable-all-extensions
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

## Use

Navigate to your [localhost](http://localhost:5000/) server to query the database names with Levenshtein distance. You can also query the raw database from the [admin](http://localhost:5000/admin/entity) interface.

## Build and load spellfix sqlite3 extension

SQLite comes with the [Levenshtein distance function](https://en.wikipedia.org/wiki/Levenshtein_distance) named as [spellfix](https://www.sqlite.org/spellfix1.html), but in the form of [loadable extension](https://www.sqlite.org/loadext.html). You must compile the library on your target system before to use it. 


### Building the spellfix extension on your system

Download sqlite's [source code](https://www.sqlite.org/download.html). Go to ext/misc and run

```
$ gcc -fPIC -shared spellfix.c -o spellfix1.so
```

You should have spellfix1.so in your current directory. Copy it to fin_sanctions/fin_sanctions directory, that is, the same directory than ```list.db```.


### sqlite

https://github.com/ghaering/pysqlite
http://stackoverflow.com/questions/1545479/force-python-to-forego-native-sqlite3-and-use-the-installed-latest-sqlite3-ver


### Loading the spellfix extension on sqlite3

On the extension is loaded, the script creates the virtual table and then you can query form matches.

```
$sqlite3 list.db
sqlite> .load ./spellfix1.so
sqlite> create virtual table spell_whole_name using spellfix1;
sqlite> insert into spell_whole_name(word) select whole_name from names;
sqlite> select word, distance from spell_whole_name where word match 'hussein';
```

The distance field indicates the number of inserts, deletes or substitutions to transform one word into other.

## REST

To be  continued...

## TODO

- Format rules to save a passport number




## License

The MIT License (MIT)
Copyright (c) 2016 Pere Vilás

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



