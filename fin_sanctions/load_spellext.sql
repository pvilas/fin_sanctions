.open ./list.db
.load ./spellfix1.so
create virtual table spell_whole_name using spellfix1;
insert into spell_whole_name(word) select upper(whole_name) from names;
create virtual table spell_passport using spellfix1;
insert into spell_passport(word) select upper(number) from passports;     
.quit
