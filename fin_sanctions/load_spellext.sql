.open ./list.db
.load ./spellfix1.so
create virtual table spell_whole_name using spellfix1;
create virtual table spell_passport using spellfix1;
.quit
