from db_model import mysql

class Entity:

    @staticmethod
    def save_to_csv():
        #f = open('title.csv', 'w')
        bookTitles=''
        db = mysql.conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT title FROM Book"
        cursor.execute(sql)
        titles = cursor.fetchall()
        for title in titles:
            #title = title.replace("[^가-힣]","")
            real = title[0]
            print(real)
            #bookTitles = bookTitles+','+str(title)
        #f.write(bookTitles)
        #f.close()
    

if __name__ == '__main__':
    Entity.save_to_csv()
        