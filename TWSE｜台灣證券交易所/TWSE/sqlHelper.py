import MySQLdb
import datetime
import numpy as np
from TWSE.transformDate import TDate
import warnings


class sqlHelper:
    def __init__(self, user, pw, db, table, createTable=None):
        self.user = user
        self.pw = pw
        self.db = db
        self.table = table
        self.createTable = createTable
    
    def getResult(self, rType):
        conn=MySQLdb.connect(host="127.0.0.1",user=self.user, passwd=self.pw,charset='utf8')
        cursor=conn.cursor()
        cursor.execute(f'USE {self.db}')
        cursor.execute("SELECT `日期` FROM `{}` ORDER BY `日期` DESC limit 1".format(self.table))
        try:
            r = cursor.fetchone()[0]
            r = datetime.datetime(r.year, r.month, r.day)
            if rType == 'date':
                return r
            elif rType == 'string':
                return TDate.date.toStringwithDash(r)
        except:
            return self, None
    def inSql(self, df):
        newDate = TDate.str.toDate(df['日期'][0])
        rDate = self.getResult(rType='date')
        try:
            if newDate.year == rDate.year and newDate.month == rDate.month:
                return True
            else:
                return False
        except:
            return False
    def LocList(self, df):
        try:
            locList = np.where([TDate.str.toDate(d) > self.getResult(rType='date') for d in df['日期']])
            if len(locList[0]) != 0:
                return locList[0]
            else:
                warnings.warn("是空集合...")
                return None
        except TypeError:
            warnings.warn("是空集合...")
            return None