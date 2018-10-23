import happybase
import  config
import  datetime
import uuid

def make_table(delete_table=False):
    connection = happybase.Connection(host=config.HBASE_HOST, port=9090)



    if delete_table:
        try:
            connection.delete_table(config.HBASE_TABLE, disable=True)

        except:
            pass
    connection.create_table(config.HBASE_TABLE, {
         'family': dict(max_versions=10),
         'family': dict(max_versions=1, block_cache_enabled=False),
         'family': dict(),
         'family': dict()}
                            )
    connection.close()
    return True


def write_row_hbase(dict_row):
    try:
        connection = happybase.Connection(host=config.HBASE_HOST, port=9090)
        table_name = 'infographis'
        table = connection.table(table_name)
        dict_row["family:date"]=bytes(datetime.date.today().strftime("%Y-%b-%d"), 'utf-8')
        #table.put(b'row-key', {b'family:date': b'2019-01-01',b'family:trending': b'trump',b'family:analized': b'bad'})
        table.put(uuid.uuid4().hex,dict_row)
        connection.close()
        return True
    except:
        pass
    return False
#print  ( write_row_hbase({b'family:date': b'2019-01-01',b'family:trending': b'trump',b'family:analized': b'bad'}) )