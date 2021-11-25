import csv
import sys
import sqlite3
from wordcloud import WordCloud
from PIL import Image
import io

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

def wordcloudgen(dp,id_="0",type_="0"):
    img = io.BytesIO()
    font = "Deng.ttf"
    if type_=="shop":
        txt = dp.comments.get(id_)
    else:
        #txt = open("bee.txt",'r').read()
        txt = "餐饮词云 好耶 好耶 好耶 好耶"
    wordcloud = WordCloud(font_path=font,width=370,height=350,background_color="white",colormap="plasma").generate(txt).to_image().save(img,format="PNG")
    img.seek(0)
    #print(img)
    return img

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
    def get_all_shops(self,filter_):
        results = []
        sff,sft,pff,pft = filter_
        for poiid in self.shops.hash_table:
            shop = self.shops.hash_table[poiid]

            avgScore = shop[2]
            if avgScore: 
                avgScore = float(avgScore)
                if avgScore<1:
                    avgScore = 1.0
            else:
                avgScore = 1.0
            avgPrice = shop[10]
            if avgPrice: 
                avgPrice = float(avgPrice)
                if avgPrice>100:
                    avgPrice = 99
                if avgPrice<5:
                    avgPrice = 6
            else:
                avgPrice = 5.0

            if avgScore<sff or avgScore>sft or avgPrice<pff or avgPrice>pft:
                continue
            shop_name = shop[1] 
            shop_add = shop[2]
            shop_coo = (shop[8], shop[9])
            results.append([ poiid,shop_name,shop_add,shop_coo ])
        return results
    def get_shop_detail(self,poiid):
        result = dict()
        shop_data = self.shops.hash_table[poiid]
        result['name'] = shop_data[1]
        result['avgScore'] = shop_data[2]
        result['address'] = shop_data[3]
        result['phone'] = shop_data[4]
        result['openTime'] = shop_data[5]
        result['extraInfos'] = shop_data[6]
        result['avgPrice'] = shop_data[10]
        result['brandId'] = shop_data[11]
        result['brandName'] = shop_data[12]
        return result

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
    '''读取商店信息文件 字段：poiid , name  avgScore , address  phone openTime  extraInfos , hasFoodSafeInfo , longitude , latitude , avgPrice , brandId , brandName '''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_details.csv",0)

class Comments(DataLoader):
    '''读取评论信息文件 字段: userName,avgPrice,comment,picUrls,commentTime,zanCnt,userLevel,userId,star,reviewId,anonymous,poiId'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_comments.csv",9)
        self.poiid_lookup = dict()
        for comment in self.hash_table:
            poiid = self.hash_table[comment][-1]
            if poiid in self.poiid_lookup:
                self.poiid_lookup[poiid].append(self.hash_table[comment][2])
            else:
                self.poiid_lookup[poiid] = [self.hash_table[comment][2] ]
    
    def get(self,poiid):
        if poiid in self.poiid_lookup:
            if  len(self.poiid_lookup[poiid]) <3:
                return "数据不足"
            return " ".join(self.poiid_lookup[poiid])
        else:
            return "数据不足"


TEST_FLAG = True

if TEST_FLAG and __name__ == '__main__':
    wordcloudgen()
