# BookCode 

## Python 가상환경 설정 방법
1. vscode에서 21_HF216 폴더 열기
2. 터미널에 `cd .\bookcode\Scripts\Activate.ps1` 입력 후 실행
   ![image](https://user-images.githubusercontent.com/68543150/124729720-a80e9000-df4b-11eb-8f80-5b63bb73cfae.png)

    -> `(bookcode) PS C:\21_hf216\bookcode\Scripts>` 라고 뜨면 성공
3. 인터프리터 설정 

    - `Ctrl + Shift + P` 누르고 Python: Select Interpreter 엔터
    - bookcode: venv 설정
     ![image](https://user-images.githubusercontent.com/68543150/124729592-8ad9c180-df4b-11eb-872e-4f24649f5aa2.png)

## Requirements.txt 설정
1. 기존 라이브러리 가져오기
   - 가상환경 실행해놓은 상태에서 `pip install -r requirements.txt`
    ![image](https://user-images.githubusercontent.com/68543150/124730350-3a169880-df4c-11eb-8a90-3e022ecf8820.png)
2. 라이브러리를 추가하고 requirements.txt 최신화하려면
   - `pip freeze > requirements.txt`
    ![image](https://user-images.githubusercontent.com/68543150/124730299-2e2ad680-df4c-11eb-978a-bdd4365c983f.png)


 