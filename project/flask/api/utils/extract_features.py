import sys

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb

def extract_book_isbn():
    """
    Extract book isbn from database
    :return: list of book isbn
    """
    conn = conn_mysqldb()
    cursor = conn.cursor()
    sql = "SELECT isbn13,title FROM Book;"
    cursor.execute(sql)
    book_isbn = cursor.fetchall()
    cursor.close()
    conn.close()
    return book_isbn

def save_to_csv(path, data, name):
    """
    Save data to csv file
    """
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv(path + f"{name}.csv", index=False)
    return df

if __name__ == "__main__":
    isbn = extract_book_isbn()
    print(isbn)
    print(isbn[0])
    path = './project/CrawlingData/'
    save_to_csv(path ,isbn, "isbn")