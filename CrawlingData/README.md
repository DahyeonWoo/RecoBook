## Review Crawler version1 사용법

* Requirement : ipynb실행환경, selenium, google chrome driver설치

* 실행 방법 : Cell1 - Cell7까지 실행시키고 Cell7이 다 끝나면 Cell8과 9를 실행시킨다.

__Cell1__ : 크롤러에 대한 설명 </br>
__Cell2__ : 필요한 라이브러리 import </br>
__Cell3__ : selenium관련 필요한 라이브러리 import </br>
__Cell4__ : fiveReview함수 </br>
  하나의 책을 클릭하면, 리뷰가 한 페이지에 5개씩 나오는데, 그 5개의 리뷰를 크롤링하는 함수 </br>
__Cell5__ : crawlReview 함수 </br>
책의 isbn13과, fiveReview함수를 사용하여 리뷰를 5개씩, 4페이지까지 가져와 총 20개 크롤링하는 함수 </br>
__Cell6__ : forOnePage 함수 </br>
책 목록이 나와 있는 페이지에서, 한 페이지에 20개의 책이 있다. 그 책을 차례로 하나씩 클릭해서 리뷰를 크롤링하고 다시 책 목록 페이지로 돌아오고, 다음 책을 클릭하고 돌아오는 것을 반복하는 함수 </br>
__Cell7__ : 책 목록 페이지 번호를 지정하고 크롬 드라이버를 원격 제어 </br>
*사용자의 구글드라이버 위치를 입력하고, 원하는 페이지를 입력하고, 원하는 페이지 주소를 입력한다.* </br>
__Cell8__ : 크롤링한 데이터를 데이터프레임이 저장 </br>
__Cell9__ : 데이터프레임을 csv로 변환하여 저장 </br>