# fin_sanctions

Web interface to consult the lists of UN, EU and US of people, groups and entities that are under financial sanctions.

The project aims to compliment the EU regulations in the sense of detect similitudes between a given name and the lists.

We use the Levenshtein distance in order to detect matches.

The project includes a Flask web server and a script that updates the local database with the sanction lists.

It includes *connectors* that translates the different lists (EU, UN, US) to a common database format. More lists can be added to the database only programming a suitable new connector.

You should have some web, python and linux/mac experience to install fin_sanctions. 



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

The apsw sqlite driver provides direct access to sqlite. We use it do get direct access to the fts and spellfix extensions. The [official](http://rogerbinns.github.io/apsw/index.html) documentation is extensive. We have installed the library without the *--user* parameter and be aware of the enable-all-extensions option. More information is on the [download](http://rogerbinns.github.io/apsw/download.html#easy-install-pip-pypi) page. Make sure you have the virtual environment activated before the installation.

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

### Building the spellfix sqlite extension on your system


On other directory, download sqlite's [source code](https://www.sqlite.org/download.html). 

At this moment the latest version is 3.13.0, so download and unzip it, download the spellfix1 extension and compile it

```
$ cd..
$ mkdir sqlite_src
$ cd sqlite_src
$ wget https://www.sqlite.org/2016/sqlite-amalgamation-3130000.zip
$ unzip sqlite-amalgamation-3130000.zip
$ cd sqlite-amalgamation-3130000
$ wget $ wget http://sqlite.org/cgi/src/raw/ext/misc/spellfix.c?name=b9065af7ab1f2597b505a8aa9892620866d502fc -O spellfix1.c
$ gcc -fPIC -shared spellfix.c -o spellfix1.so
```

You should have spellfix1.so in your current directory. Copy it to fin_sanctions/fin_sanctions directory.


### Make the database

Now you can download the lists and create the database. Return to the fin_sanctions directory and execute the creation script. You may read the script to understand what is happen.

```
source make_db.sh
```

If none error happened you would take a look at the database structure

```
sqlite3 fin_sanctions/list.db
.tables
sqlite> .load .fin_sanctions/spellfix1.so
sqlite> select word, distance from spell_whole_name where word match 'hussein';
.quit
```

The distance field is proportional to the number of inserts, deletes or substitutions to transform one word into other.

### Run the flask server

```
source run.sh
```

Navigate to [localhost](http://localhost:5000/) to query the database names with Levenshtein distance. 

You can query the raw database from the [admin](http://localhost:5000/admin/entity) interface.



## Update the lists

You must run the *make_db.sh* script one time a month to update the lists.


## Regulations

The [Casinos Association of Spain](www.asociaciondecasinos.org/), following EU regulations, recommends to use the edit or Levenshtein distance method to detect similarities between the lists and given passports numbers or whole names. 


## Id number normalization

On the database, the passport number is *normalized* before storing it. Each time we query for a passport the server normalizes it before perform the search. The exact normalization code is:

```python

def toS(cadena):
    return unicodedata.normalize('NFKD', unicode(cadena)).encode('ascii', 'ignore')

def normalize_passport(num):
    """ normalizes passport id """
    num=num.\
        upper().\
        strip().\
        replace("-", "").\
        replace(" ", "").\
        replace("\\", "").\
        replace("_", "").\
        replace("/", "")
    return toS(num)
```

## API

To be  continued...


## Useful links

- [EU European Union External Action](http://eeas.europa.eu/cfsp/sanctions/index_en.htm)
- [UNHCR - The UN Refug ee Agency](http://www.unhcr.org/)
- [FATF - Financial Action Task Force](http://www.fatf-gafi.org/home/)
- [ES Comisión de Prevención de Blanqueo de Capitales](http://www.sepblac.es/espanol/home_esp.htm)
- [CH State Secretariat for Economics Affairs](https://www.seco.admin.ch/seco/en/home/Aussenwirtschaftspolitik_Wirtschaftliche_Zusammenarbeit/Wirtschaftsbeziehungen/exportkontrollen-und-sanktionen/sanktionen-embargos.html)
- [UK Office of Financial Sanctions Implementation Lists](https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets)
- [US Office of Foreign Assets Control](https://sanctionssearch.ofac.treas.gov/)
- [US Department of the Treasury](https://www.treasury.gov/resource-center/sanctions/Pages/default.aspx)
- [CA current sanctions](http://www.international.gc.ca/sanctions/countries-pays/index.aspx?lang=eng)
- [AU current sanctions](http://dfat.gov.au/international-relations/security/sanctions/sanctions-regimes/pages/sanctions-regimes.aspx)
- [SG Monetary Authority of Singapore](http://www.mas.gov.sg/Regulations-and-Financial-Stability/Anti-Money-Laundering-Countering-The-Financing-Of-Terrorism-And-Targeted-Financial-Sanctions.aspx)
- [HK Monetary Authority](http://www.hkma.gov.hk/eng/index.shtml)
- [The Egmont Group](http://www.egmontgroup.org/)
- [Transparency International](http://www.transparency.org/)
- [Human Rights Watch](https://www.hrw.org/)
- [Sanctions wiki](http://www.sanctionswiki.org/Main_Page)

## License

The MIT License (MIT)
Copyright (c) 2016 Pere Vilás

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



