import csv
import sys

class CsvData(dict):
    '''读取csv文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
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
                self[row[key_col]] = row
            csv_row_count += 1
        print("Csv loaded, {0} rows in csv file, {1} rows in memory.".format(csv_row_count,len(self)))
        print("Csv loaded with memory usage of",int(sys.getsizeof(self)/1024),'kb.')

class ShopDetails(CsvData):
    '''读取商店信息文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_details.csv",0)

class Comments(CsvData):
    '''读取评论信息文件'''
    def __init__(self,*args,**kwargs):
        super(__class__,self).__init__(*args,**kwargs)
        self.load("shop_comments.csv",9)

TEST_FLAG = True

if TEST_FLAG or __name__ == '__main__':
    c = Comments()
