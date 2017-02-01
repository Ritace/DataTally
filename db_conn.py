import pandas as pd
from sqlalchemy import *
engine = create_engine('mysql+pymysql://root:thapa@localhost/datatally?charset=utf8', pool_recycle=3600)

connection = engine.connect().connection
conn = engine.connect()
metadata= MetaData()

datatable = Table('DataTable', metadata,
									Column('fld_Bldg_SID',String(50),primary_key=True),									    
								    Column('fld_Bldg_DsgnStd',String(1000)),
								    Column('fld_Bldg_ID', String(50)),
									Column('fld_Bldg_UID',String(50)),
									Column('fld_Bldg_NM',String(100)),
									Column('fld_Bldg_HSFU',String(100)),
									Column('fld_Bldg_Oshp',String(100)),
									Column('fld_Bldg_YOC',String(100)),
									Column('fld_Bldg_GC',String(100)),
									Column('fld_Bldg_Typ',String(100)),
									Column('fld_Bldg_Use',String(100)),
									Column('fld_HI_ID',String(100)),
									Column('fld_HI_SID',String(100)),
									Column('fld_Bldg_FlrAr',String(100)),
									Column('fld_Bldg_Img0',String(100)),
									Column('fld_Bldg_Img1',String(100)),
									Column('fld_Bldg_Img2',String(100)),
									Column('fld_Bldg_Img3',String(100)),
									Column('fld_Bldg_Img4',String(100)),
									Column('fld_Bldg_Drw',String(100)),
									Column('fld_HI_Typ',String(100)),
									Column('fld_HI_Name',String(100)),
									Column('is_tallied',String(50)),
									Column('fld_Dist_NM',String(50)),
									Column('fld_Dist_ID',String(50)),
									mysql_engine = 'InnoDB',
									mysql_charset = "utf8")

metadata.create_all(engine)
