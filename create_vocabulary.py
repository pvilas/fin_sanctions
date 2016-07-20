import apsw
apsw_con=apsw.Connection('fin_sanctions/list.db')
apsw_con.enableloadextension(True)
apsw_con.loadextension('./fin_sanctions/spellfix1.so')
print('spellfix1 extension loaded')



def create_vocabulary():
    """ populates the vocabulary tables to do spellfix - Levenshtein """

    # import apsw type connection
    cursor=apsw_con.cursor()

    cursor2 = apsw_con.cursor()

    cursor3 = apsw_con.cursor()


    # for each name
    for w in cursor2.execute('select whole_name, id from names'):
        cursor.execute('insert into spell_whole_name(word) values(?)', 
                        (w[0].upper(),))
        # get rowid
        lr = apsw_con.last_insert_rowid()

        # update Name with the rowid
        cursor3.execute('update names set spell_ref=? where id=?',
            (lr, w[1]))
        

    # for each passport
    for w in  cursor2.execute('select number, id from passports'):
        cursor.execute('insert into spell_passport(word) values(?)', 
                        (w[0].upper(),))
        # get rowid
        lr = apsw_con.last_insert_rowid()
        # update passport with the rowid
        cursor3.execute('update passports set spell_ref=? where id=?',
            (lr, w[1]))
        

    # insert into spell_whole_name(word) select upper(whole_name) from names;
    # insert into spell_passport(word) select upper(number) from passports;     



print ("Creating vocabulary tables...")
cursor=apsw_con.cursor()
cursor.execute('create virtual table spell_whole_name using spellfix1;create virtual table spell_passport using spellfix1;')
print ("Created.")

print "Creating vocabulary, wait please..."
create_vocabulary()
print "Vocabulary created"

