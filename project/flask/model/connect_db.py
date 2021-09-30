import sys
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
import pandas as pd
from tqdm import tqdm
from db_model.mysql import conn_sadb

def insert_df_into_DB():
    """
    Book 테이블에 임베딩, top n isbn, cosine similarity 값을 저장하는 함수
    이를 위해 list 형태인 위 컬럼을 str로 변환
    변환한 df를 sqlalchemy를 통해 DB에 저장
    """
    db = conn_sadb()
    df = pd.read_json('/21_HF216/project/flask/model/top_isbn_with_scores.json', orient='index', convert_axes=False)
    df.index = df.index.astype(int)
    for i, row in df.iterrows():
        df.at[i, 'embedding'] = str(row['embedding'])
        df.at[i, 'top_isbn'] = str(row['top_isbn'])
        df.at[i, 'cosine_similarity'] = str(row['cosine_similarity'])
    df.to_sql(name='Score', con=db, index=False, if_exists='replace')


if __name__ == '__main__':
    insert_df_into_DB()