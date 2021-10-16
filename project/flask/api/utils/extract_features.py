import sys

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb

def extract_book_info():
    """
    Extract book data info from database
    :return: list of book info
    """
    conn = conn_mysqldb()
    cursor = conn.cursor()
    sql = "SELECT isbn13,title,author,description FROM Book;"
    cursor.execute(sql)
    book_info = cursor.fetchall()
    cursor.close()
    conn.close()
    return book_info

def save_to_csv(path, data, name):
    """
    Save data to csv file
    """
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv(path + f"{name}.csv", index=False)
    return df

def compare_db():
    conn = conn_mysqldb()
    cursor = conn.cursor()
    sql = "SELECT isbn13 FROM Book;"
    cursor.execute(sql)
    book_info = [int(x[0]) for x in cursor.fetchall()]
    sql = 'SELECT isbn13 FROM Review'
    cursor.execute(sql)
    review_info = [x[0] for x in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    not_exist = []
    for isbn in review_info:
        if isbn not in book_info:
            not_exist.append(isbn)
    print('length of not exist:', len(not_exist))
    return not_exist
if __name__ == "__main__":
    # info = extract_book_info()
    # path = './project/CrawlingData/'
    # save_to_csv(path ,info, "book_info")
    print(compare_db())