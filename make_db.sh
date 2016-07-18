echo "fin_sanctions. DB creation and population"
echo "-----------------------------------------"
read -p "Creating db backup. The old backup will be deleted!. Press Ctrl+C to abort or Enter to proceed."
echo "Deleting old backup"
rm fin_sanctions/list.db.old
echo "Creating new backup"
mv fin_sanctions/list.db fin_sanctions/list.db.old
echo "Loading spellfix extension and creating indexes"
cd fin_sanctions
sqlite3 list.db < load_spellext.sql
cd ..
echo "Creating new (empty) db"
python make_db.py
echo "Downloading lists"
cd fin_sanctions/lists
echo "EU list"
wget -N http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml
echo "UN list"
wget -N https://www.un.org/sc/suborg/sites/www.un.org.sc.suborg/files/consolidated.xml
cd ../..
echo "Populating new db with EU list"
python parse_list_eu.py
echo "Populating new db with UN list"
python parse_list_un.py
echo "Vocabulary"
python create_vocabulary.py
echo "Terminated. Please look for errors."