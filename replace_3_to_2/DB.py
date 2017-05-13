import MySQLdb


# class TBL(object):
#   """docstring for TBL"""
#   def __init__(self, table_name):
#     super(TBL, self).__init__()
#     self.table_name = table_name
    

class DB(object):
  """docstring for DB"""
  def __init__(self, db_name, tables):
    super(DB, self).__init__()
    self.db_name = db_name
    
    self.db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = "root",
                     db = db_name)
    self.cursor = self.db.cursor()

    self.tables = {}

    for table in tables:
      self.tables[table] = {
        "fields" : self.get_fields(table)
      }


  def get_fields(self, table):
    self.cursor.execute("SELECT * FROM %s LIMIT 1" %table)
    return [i[0] for i in self.cursor.description]
    


  def execute_read(self, query):
    self.cursor.execute(query)
    return [row for row in self.cursor.fetchall()]
      # print row[dbv3.tables["DataTable"]["fields"].index("fld_BldSID")]


  def get(self, table, row, field):
    return row[self.tables[table]["fields"].index(field)]


  def replace(self, table, replace_dict, where):
    # self.cursor.execute("SELECT * FROM %s LIMIT 1" %table)

    sql = "UPDATE " + table + " SET "  + ", ".join(["%s = '%s'" %(key, replace_dict[key]) for key in replace_dict]) + " WHERE " + where + ";"
    # print ["%s = %s," %(key, replace_dict[key]) for key in replace_dict]

    try:
       self.cursor.execute(sql)
       self.db.commit()
       print "success editing %s %s" %(table, where)
    except:
       self.db.rollback()
       print sql
       print "ERROR editing %s %s" %(table, where)


  def insert(self, table, insert_dict):
    # INSERT INTO table SET columnA = 'valueA', columnB = 'valueB'
    sql = "INSERT INTO " + table + " SET "  + ", ".join(["%s = '%s'" %(key, insert_dict[key]) for key in insert_dict]) + ";"
    # print ["%s = %s," %(key, replace_dict[key]) for key in replace_dict]

    try:
       self.cursor.execute(sql)
       self.db.commit()
       print "success entry %s" %(table)
    except:
       self.db.rollback()
       print sql
       print "ERROR entry %s" %(table)



  def __del__(self):
    self.db.close()

#     sql = "UPDATE " + table + SET  
# SET column1=value, column2=value2,...
# WHERE some_column=some_value 


#     print sql

'''

  # you must create a Cursor object. It will let
  #  you execute all the queries you need
  cur = db.cursor()

  # Use all the SQL you like
  cur.execute("SELECT * FROM tbl_hi_web LIMIT 4")

  # print all the first cell of all the rows
  for row in cur.fetchall():
    print row[0]

  db.close()
'''