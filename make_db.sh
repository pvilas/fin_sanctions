echo "fin_sanctions. DB creation and population"
echo "-----------------------------------------"
read -p "Creating db backup. The old backup will be deleted!. Press Ctrl+C to abort or Enter to proceed."
echo "Deleting old backup"
rm fin_sanctions/list.db.old
echo "Creating new backup"
mv fin_sanctions/list.db fin_sanctions/list.db.old
echo "Creating new db"
python make_db.py