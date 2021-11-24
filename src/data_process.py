import csv
import sys
import sqlite3

def sqlite_escape(keyword):
    keyword = keyword.replace("/", "//");  
    keyword = keyword.replace("'", "''");  
    keyword = keyword.replace("[", "/[");  
    keyword = keyword.replace("]", "/]");  
    keyword = keyword.replace("%", "/%");  
    keyword = keyword.replace("&","/&");  
    keyword = keyword.replace("_", "/_");  
    keyword = keyword.replace("(", "/(");  
    keyword = keyword.replace(")", "/)");  
    return keyword

class InMemoryDatabase():
    '''内存数据库'''
    def __init__(self):
        self.db = sqlite3.connect( ':memory:' ) #创建内存数据库
        cur = self.db.cursor();
        cur.execute("CREATE TABLE SHOPS(poiid INT NOT NULL, name VARCHAR(255), avgScore FLOAT, address TEXT, phone TEXT,openTime VARCHAR(255), extraInfos TEXT, hasFoodSafeInfo TINYINT, longitude DOUBLE, latitude DOUBLE, avgPrice INT, brandId INT, brandName TEXT, PRIMARY KEY (poiid) )")
        cur.execute("CREATE TABLE COMMENTS()") #TODO
    def insert(self,row,table="SHOPS"):
        cur = self.db.cursor()
        if table=="SHOPS":
            cur.execute("INSERT INTO SHOPS()") #TODO
        elif table=="COMMENTS":
            cur.execute("INSERT INTO COMMENTS()") #TODO
        pass
    def query(self,key="*",filters=[]):
        pass
        

class DataProcess():
    def __init__(self):
        self.shops = ShopDetails()
        self.comments = Comments()
    def get_all_shops(self):
        results = []
        for poiid in self.shops.hash_table:
            shop_name = self.shops.hash_table[poiid][1] 
            shop_add = self.shops.hash_table[poiid][2]
            shop_coo = (self.shops.hash_table[poiid][8], self.shops.hash_table[poiid][9])
            results.append([ poiid,shop_name,shop_add,shop_coo ])
        return results

class DataLoader():
    '''读取csv文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        #self.db = InMemoryDatabase()
        self.hash_table = dict()

    def load(self,fn,key_col):
        '''读取csv文件
        fn:文件名
        key_col:索引所在列
        '''
        f_handle = open(fn,"r")
        csv_reader = csv.reader(f_handle)
        csv_row_count = 0
        print("Loading",fn,'...')
        for row in csv_reader:
            if row[key_col].isnumeric():
                self.hash_table[row[key_col]] = row
                #self.db.insert(row)
            csv_row_count += 1
        print("Csv loaded, {0} rows in csv file, {1} rows in memory.".format(csv_row_count,len(self.hash_table)))
        print("Hash Table memory usage:",int(sys.getsizeof(self.hash_table)/1024),"kb.")

class ShopDetails(DataLoader):
    '''读取商店信息文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_details.csv",0)

class Comments(DataLoader):
    '''读取评论信息文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_comments.csv",9)

TEST_FLAG = False

if TEST_FLAG and __name__ == '__main__':
    c = Comments()
