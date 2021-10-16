import sys
sys.path.append("./project/flask/")
from api.db_model.mysql import conn_mysqldb, conn_sadb
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api.utils.ColumnsFromDB import ColumnsFromDB
from scipy import spatial

class NLPRecommend:
    #작가 기반 추천
    def recommend_by_author(author):
        db = conn_mysqldb()
        db_cursor = db.cursor()
        try:
            sql = "SELECT author, vector FROM AuthorTest;"
            db_cursor.execute(sql)
            result = db_cursor.fetchall()
            author_df = pd.DataFrame(result,columns=['author','vector'])
            author_df['vector_']=author_df['vector'].apply(str_to_vector)

            embedding_list=list(author_df['vector_'])
            cosine_similarities = cosine_similarity(embedding_list, embedding_list)

            books = author_df[['author']]
            # 작가를 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장.
            indices = pd.Series(author_df.index, index = author_df['author']).drop_duplicates()
            idx = indices[author]

            # 입력된 작가와 작가설명(info)가 유사한 작가 5개 선정.
            sim_scores = list(enumerate(cosine_similarities[idx]))
            sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
            sim_scores = sim_scores[1:6]

            # 가장 유사한 작가 5권의 인덱스
            book_indices = [i[0] for i in sim_scores]

            # 전체 데이터프레임에서 해당 인덱스의 행만 추출. 5개의 행을 가진다.
            recommend = books.iloc[book_indices].reset_index(drop=True)

            # 순차적으로 출력
            return_list=list()
            for i in book_indices:
                return_list.append(books.loc[i]['author'])
            authors = '\n'.join(return_list)

            return authors
        except:
            return None

    #제목 기반 추천
    def recommend_by_title_using_reviews(title):
        db = conn_mysqldb()
        db_cursor = db.cursor()
        try:
            sql = "SELECT title, vector FROM Review;"
            db_cursor.execute(sql)
            result = db_cursor.fetchall()

            book_df = pd.DataFrame(result,columns=['title','vector'])
            book_df['vector_']=book_df['vector'].apply(str_to_vector)

            embedding_list=list(book_df['vector_'])
            cosine_similarities = cosine_similarity(embedding_list, embedding_list)

            books = book_df[['title']]
            # 책의 제목을 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장.
            indices = pd.Series(book_df.index, index = book_df['title']).drop_duplicates()
            idx = indices[title]

            # 입력된 책과 줄거리(document embedding)가 유사한 책 5개 선정.
            sim_scores = list(enumerate(cosine_similarities[idx]))
            sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
            sim_scores = sim_scores[1:6]

            # 가장 유사한 책 5권의 인덱스
            book_indices = [i[0] for i in sim_scores]

            # 전체 데이터프레임에서 해당 인덱스의 행만 추출. 5개의 행을 가진다.
            recommend = books.iloc[book_indices].reset_index(drop=True)

            # 데이터프레임으로부터 순차적으로 이미지를 출력
            return_list=list()
            for i in book_indices:
                return_list.append(books.loc[i]['title'])
            titles = '\n'.join(return_list)

            return titles
        except:
            return None


    # 키워드 기반 추천
    def recommend_by_keyword_using_reviews(keyword):
        db = conn_mysqldb()
        db_cursor = db.cursor()
        try:
            sql = f"SELECT vector FROM Keyword WHERE keyword = \'{keyword}\';"
            db_cursor.execute(sql)
            keyword_vector = db_cursor.fetchall()[0][0]

            sql ="SELECT title, vector FROM Review;" 
            db_cursor.execute(sql)
            df = pd.DataFrame(db_cursor.fetchall())
            df.columns = ['title','vector']
            Doc2Vec_list = list(df['vector'])
            books = df[['title']]
            
            cos_sim_list=[]
            
            for doc in Doc2Vec_list:
                cos_sim_list.append(1 - spatial.distance.cosine(str_to_vector(keyword_vector), np.array(str_to_vector(doc))))

            sim_scores = list(enumerate(cos_sim_list))
            sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
            sim_scores = sim_scores[:5]
            book_indices = [i[0] for i in sim_scores]
            recommend = books.iloc[book_indices].reset_index(drop=True)
            return_list = []

            for i in book_indices:
                return_list.append(books.loc[i]['title'])    

            return '\n'.join(return_list)
        except :
            return None

    # 유저 기반 추천
    def recommend_by_user_using_review(user_idx):
        db = conn_mysqldb()
        db_cursor = db.cursor()

        try:
            sql = f"SELECT bookWant FROM User WHERE idx LIKE {user_idx};"
            db_cursor.execute(sql)
            result = db_cursor.fetchall()[0][0]
            print(result)        

            bookWantList = result.split(';')
            bookWantList = ['\''+bookWant.strip()+'\'' for bookWant in bookWantList]            
            bookWantVector = []
            sql = f"SELECT title,vector FROM Review WHERE title LIKE {' OR title LIKE '.join(bookWantList)};"
            print(sql)
            db_cursor.execute(sql)  
            result = db_cursor.fetchall()      

            df = pd.DataFrame(result)
            df.columns = ['title','vector']
            df['vector'] = df['vector'].apply(str_to_vector)
            mean_Vector = df['vector'].mean()

            sql ="SELECT title, vector FROM Review;" 
            db_cursor.execute(sql)
            df = pd.DataFrame(db_cursor.fetchall())
            df.columns = ['title','vector']
            Doc2Vec_list = list(df['vector'])


            cos_sim_list=[]
              
            for doc in Doc2Vec_list:
                cos_sim_list.append(1 - spatial.distance.cosine(mean_Vector, np.array(str_to_vector(doc))))

            sim_scores = list(enumerate(cos_sim_list))
            sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
            sim_scores = sim_scores[2:7]
            book_indices = [i[0] for i in sim_scores]
            recommend = df.iloc[book_indices].reset_index(drop=True)
            return_list = []

            for i in book_indices:
                return_list.append(df.loc[i]['title'])    

            return '\n'.join(return_list)
        except:
            return None



    def recommend_by_title_using_description(title):
        """
        리스트 뷰가 아직 미완성됐으므로 일단 추천할 책의 제목만 반환함
        리스트 뷰가 완성되면 형식에 맞게 변환해야함.
        """
        db = conn_mysqldb()
        db_cursor = db.cursor()
        # test 용 title description 프린팅
        try:
            sql = f"SELECT title, description FROM total_view WHERE title LIKE '%{title}%'"
            db_cursor.execute(sql)
            result = db_cursor.fetchall()[0]
            print(result)
            # title에 해당하는 top_isbn 추출
            sql = f"SELECT top_isbn FROM total_view WHERE title LIKE '%{title}%'"
            db_cursor.execute(sql)
            top_isbn = db_cursor.fetchone()[0]
            # 문자형 리스트를 문자형 튜플로 변환
            top_isbn = str(tuple(eval(top_isbn)))
            # isbn에 해당하는 제목, 작가 추출
            sql = f"SELECT title FROM total_view WHERE isbn13 in {top_isbn}"
            db_cursor.execute(sql)
            result = db_cursor.fetchall()
            print(result)
            return result
        except:
            return None
    

    def random_recommend():
        """
        책 랜덤 추천
        DB에서 bestRank가 0이 아닌 책의 COUNT를 뽑아서 random int 하나를 뽑고,
        bestRank가 0이 아닌 책 중 해당 random int에 해당하는 책 리턴
        """
        import random
        engine = conn_sadb()
        with engine.connect() as connection:
            result = connection.execute("SELECT COUNT(*) FROM Book WHERE bestRank != 0")
            for row in result:
                count = row[0]
            idx = random.randint(1, count)
            print(f"랜덤 인덱스: {idx}")
        data = ColumnsFromDB.get_db_data('*', 'Book', 'idx', idx-1, random=True)
        return data

def str_to_vector(str_vector):    
    str_vector=str_vector.replace('[','').replace(']','').split()
    list_vector = list(map(float, str_vector))
    vector=np.array(list_vector)    
    return vector

if __name__ == '__main__':
    title = '7년의 밤'
    # print(NLPRecommend.recommend_by_title_using_reviews(title))
    # print(NLPRecommend.recommend_by_title_using_description(title))
    print(NLPRecommend.random_recommend())