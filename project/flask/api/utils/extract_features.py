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
    sql = "SELECT isbn13,title,author FROM Book;"
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

if __name__ == "__main__":
    info = extract_book_info()
    path = './project/CrawlingData/'
    save_to_csv(path ,info, "book_info")