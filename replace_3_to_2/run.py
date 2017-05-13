import MySQLdb

from DB import DB


# dbv2 = MySQLdb.connect(host="localhost",    # your host, usually localhost
#                      user="root",         # your username
#                      passwd="root",  # your password
#                      db="datatallyversion2")        # name of the data base

# dbv3 = MySQLdb.connect(host="localhost",    # your host, usually localhost
#                      user="root",         # your username
#                      passwd="root",  # your password
#                      db="datatally")        # name of the data base



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




# cursor_dbv2 = dbv2.cursor()
# cursor_dbv3 = dbv3.cursor()


# # field_names = [i[0] for i in cursor_dbv3.description]
# # print field_names

# dbv3_datatables_fieldnames = ['fld_Bldg_SID', 'fld_Bldg_DsgnStd', 'fld_Bldg_ID', 'fld_Bldg_UID', 'fld_Bldg_NM', 'fld_Bldg_HSFU', 'fld_Bldg_Oshp', 'fld_Bldg_YOC', 'fld_Bldg_GC', 'fld_Bldg_Typ', 'fld_Bldg_Use', 'fld_HI_ID', 'fld_HI_SID', 'fld_Bldg_FlrAr', 'fld_Bldg_Img0', 'fld_Bldg_Img1', 'fld_Bldg_Img2', 'fld_Bldg_Img3', 'fld_Bldg_Img4', 'fld_Bldg_Drw', 'fld_HI_Typ', 'fld_HI_Name', 'is_tallied', 'fld_Dist_NM', 'fld_Dist_ID', 'is_new', 'fld_Bldg_WPit', 'fld_Bldg_Plac', 'fld_Bldg_Inci']


# def main():
#   cursor_dbv3.execute("SELECT * FROM DataTable LIMIT 5")
#   for row in cursor_dbv3.fetchall():
#     print row[dbv3_datatables_fieldnames.index('fld_Bldg_SID')]
  

#   print "ok"


dbv3 = DB("datatally", ["DataTable"])
dbv2 = DB("datatallyversion2", ["tbl_bldg_web", "tbl_hi_web"])



def print_common_fields():
  a = dbv3.tables["DataTable"]["fields"]
  b = dbv2.tables["tbl_bldg_web"]["fields"]
  c = dbv2.tables["tbl_hi_web"]["fields"]


  # print a
  print list(set(a).intersection(b))
  # ['fld_Bldg_Inci', 'fld_Bldg_HSFU', 'fld_Bldg_YOC', 'fld_Bldg_Typ', 'fld_Bldg_UID', 'fld_HI_ID', 'fld_Bldg_NM', 'fld_Bldg_Oshp', 'fld_Bldg_DsgnStd', 'fld_Bldg_ID', 'fld_HI_Typ', 'fld_Bldg_Use', 'fld_HI_SID', 'fld_Bldg_WPit', 'fld_Bldg_GC', 'fld_Bldg_FlrAr', 'fld_Bldg_Img1', 'fld_Bldg_SID', 'fld_Bldg_Img3', 'fld_Bldg_Img2', 'fld_Bldg_Img4', 'fld_Bldg_Img0', 'fld_Bldg_Plac']
  print list(set(a).intersection(c))
  # ['fld_HI_Typ', 'fld_HI_SID', 'fld_Dist_ID', 'fld_HI_ID']


blgd_fields_to_replace = ['fld_Bldg_Inci', 'fld_Bldg_HSFU', 'fld_Bldg_YOC', 'fld_Bldg_Typ', 'fld_Bldg_UID', 'fld_HI_ID', 'fld_Bldg_NM', 'fld_Bldg_Oshp', 'fld_Bldg_DsgnStd', 'fld_HI_Typ', 'fld_Bldg_Use', 'fld_HI_SID', 'fld_Bldg_WPit', 'fld_Bldg_GC', 'fld_Bldg_FlrAr', 'fld_Bldg_Plac', 'fld_Bldg_SID']


# dbv3.tables["DataTable"]["fields"][dbv3.tables["DataTable"]["fields"].index("fld_Dist_NM")] = "fld_Dist_Nm"
# print dbv3.tables["DataTable"]["fields"].index("fld_Dist_Nm")

def main():
  rows_dbv3 = dbv3.execute_read("SELECT * FROM DataTable LIMIT 5000 OFFSET 4000")


  for row in rows_dbv3:
    if dbv3.get("DataTable", row, "is_tallied") == "0": continue

    bldg_sid = dbv3.get("DataTable", row, "fld_Bldg_SID")
    hi_sid = dbv3.get("DataTable", row, "fld_HI_SID")

    print bldg_sid, hi_sid

    if bldg_sid == "" or hi_sid == "":
      continue


    r = {}
    w = {}
    for field in dbv3.tables["DataTable"]["fields"]:
      r[field] = dbv3.get("DataTable", row, field)
      if field in blgd_fields_to_replace:
        w[field] = r[field]

    if w["fld_HI_Typ"] == "":
      w["fld_HI_Typ"] = '0'

    if w['fld_Bldg_Oshp'] == "":
      w["fld_Bldg_Oshp"] = '0'

    if w['fld_Bldg_DsgnStd'] == "":
      w["fld_Bldg_DsgnStd"] = '0'
    
    if w['fld_Bldg_HSFU'] == "":
      w["fld_Bldg_HSFU"] = '0'

    if w['fld_Bldg_Use'] == "":
      w["fld_Bldg_Use"] = '0'

    if w['fld_HI_ID'] == "":
      w["fld_HI_ID"] = '0'

    if w['fld_HI_ID'] == "":
      w["fld_HI_ID"] = '0'

    if w['fld_Bldg_YOC'] == "":
      w["fld_Bldg_YOC"] = '0'

    if r["fld_HI_Typ"] == "":
      r["fld_HI_Typ"] = '0'

    #### is_updated value = 1 -> updated
    ####            value = 2 -> updated + new
    ####            value = 0 -> not touched
    # return

    row_dbv2_bldg = dbv2.execute_read("SELECT * FROM tbl_bldg_web WHERE fld_Bldg_SID = '%s'" %bldg_sid)
    if len(row_dbv2_bldg) == 0:
      # CREATE NEW HERE>>
      w["is_updated"] = "2"

      dbv2.insert("tbl_bldg_web", w)

      row_dbv2_hi = dbv2.execute_read("SELECT * FROM tbl_hi_web WHERE fld_HI_SID = '%s'" %hi_sid)

      if len(row_dbv2_hi) == 0:
        # CREATE NEW HI
        dbv2.insert("tbl_hi_web", {"fld_HI_Typ": r["fld_HI_Typ"], "fld_HI_SID": r["fld_HI_SID"], "fld_Dist_ID": r["fld_Dist_ID"], "fld_Dist_Nm": r["fld_Dist_NM"], "fld_HI_ID": r["fld_HI_ID"], "is_updated": "2"})

      else:
        # REPLACE HI
        dbv2.replace("tbl_hi_web", {"fld_Dist_Nm": r["fld_Dist_NM"], "fld_Dist_ID": r["fld_Dist_ID"], "is_updated": "1"}, "fld_HI_SID = '%s'" %hi_sid)

    else:
      # REplace here.
      w["is_updated"] = "1"

      dbv2.replace("tbl_bldg_web", w, "fld_Bldg_SID = '%s'" %bldg_sid)
      dbv2.replace("tbl_hi_web", {"fld_Dist_Nm": r["fld_Dist_NM"], "fld_Dist_ID": r["fld_Dist_ID"], "is_updated": "1"}, "fld_HI_SID = '%s'" %hi_sid)
      pass


    # print row_dbv3_hi
    # dbv2.replace("tbl_bldg_web", {"is_updated": "0", "fld_Bldg_NM": "office"}, "fld_Bldg_SID = '%s'" %bldg_sid)

    # print type(bldg_sid)
  # print rows

  # print dbv2.tables


if __name__ == '__main__':
  # print_common_fields()
  main()