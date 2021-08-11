import pymysql

MYSQL_CONN = pymysql.connect(
    host='db-6slkr-kr.vpc-pub-cdb.ntruss.com',
    port=3306,
    user='domain',
    passwd='bookcode7!',
    db='bookcode',
    charset='utf8mb4'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN


if __name__ == '__main__':
    res = conn_mysqldb()
    print(res)