# code-review-ai
code review AI for 2025 study

## 실행 방법
### 환경 설정
[.example.env.toml](https://github.com/pnu-haters/code-review-ai/blob/main/.example.env.toml)을 참고하여 `.env.toml` 파일을 생성합니다.

### 실행
```sh
# uv run main.py <공통 폴더>
$ uv run main.py week01
```


### 스터디 Repo 규칙

1. 최상위 폴더는 스터디원의 유저명입니다.
2. 각 유저 폴더 안에 공통 폴더를 생성합니다.  
   ( AI가 이 폴더에서 각 유저의 코드를 읽습니다. )
3. 공통 폴더 내 코드 파일명 규칙: `BOJ_<문제번호>_<문제이름>.<확장자>`  
   ( 문제 이름은 중요하지 않습니다. )
   ```
   user-1/week01/BOJ_1260_자동차.cpp
   user-2/week01/BOJ_1260_자동차.cpp
   user-3/week01/BOJ_1260_자동차.py
   ```

### 결과
AI가 생성하는 리뷰 결과물은 다음과 같습니다:

- 문제별로 하나의 리뷰 파일을 생성합니다.
- 각 파일에는 모든 스터디원의 코드 리뷰가 포함됩니다.
- 유저한테 없는 폴더나 파일은 자동으로 무시됩니다.

```
reviews
  ├── 1283_AI_코드리뷰.md
  ├── 1522_AI_코드리뷰.md
  └── ...
```

