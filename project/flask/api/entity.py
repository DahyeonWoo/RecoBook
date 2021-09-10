from db_model import mysql
import pandas as pd

class Entity:

    @staticmethod
    def title_to_excel():
        #책 제목 리스트에 저장
        titleList = []
        #빠지는 책의 개수 셀 변수
        howMany=0

        db = mysql.conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT title FROM Book"
        cursor.execute(sql)
        titles = cursor.fetchall()
        for title in titles:
            #title = title.replace("[^가-힣]","")
            real = title[0]
            if len(real)>=40:
                howMany += 1
                continue
            
            titleList.append(real)

        print(howMany)

        #df생성
        data = {'엔티티 이름':'book', '대표어':titleList, '유사어':'', '민감 정보 보안설정':'일반 정보'}
        df = pd.DataFrame(data)
        df = df.drop_duplicates()
        print(df.shape)
        
        #print(df.head())
        writer = pd.ExcelWriter('/Users/zogak/hanium/bookEntity.xlsx')
        df.to_excel(writer, sheet_name='bookEntity')
        writer.close()  
    
    def writer_to_excel():
        writerList=[]
        
        db = mysql.conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT name FROM AuthorOrigin"
        cursor.execute(sql)
        authors = cursor.fetchall()
        for author in authors:
            real = author[0]
            writerList.append(real)


        #df생성
        data = {'엔티티 이름':'writer', '대표어':writerList, '유사어':'', '민감 정보 보안설정':'일반 정보'}
        df = pd.DataFrame(data)
        df = df.drop_duplicates()
        print(df.shape)
        
        #print(df.head())
        writer = pd.ExcelWriter('/Users/zogak/hanium/writerEntity.xlsx')
        df.to_excel(writer, sheet_name='writerEntity')
        writer.close()  
        

if __name__ == '__main__':
    Entity.title_to_excel()
    #Entity.writer_to_excel()
        