.open ./list.db
.load ./spellfix1.so
create virtual table whole_name using spellfix1;
insert into whole_name(word) select upper(whole_name) from names;
.quit
