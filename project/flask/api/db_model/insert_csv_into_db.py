# csv 파일을 db에 넣는 함수
from mysql import conn_mysqldb

def insert_csv_into_db(csv_file_path, table_name):
    mysql_db = conn_mysqldb()
    db_cursor = mysql_db.cursor()

    sql = f"""
    LOAD DATA INFILE '{csv_file_path}'
    INTO TABLE {table_name}
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS
    """
    db_cursor.execute(sql)
    mysql_db.commit()
    db_cursor.close()
    print('Done')

if __name__ == '__main__':
    insert_csv_into_db('C:/21_hf216/project/CrawlingData/merge2_removed.csv', 'Author')