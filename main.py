import os
import sys
import tomllib
import boj
from github import Github
from review import ReviewAI

def load_config():
  with open(".env.toml", 'rb') as f:
    config = tomllib.load(f)

  return config

def main():
  config = load_config()
  week = sys.argv[1]
  
  review_ai = ReviewAI(config["openai"])
  g = Github(login_or_token=config["github"]["api_key"])

  repo = g.get_repo(config["code_review"]["github_repo"])

  study_code = {}

  for user in config["code_review"]["users"]: # 문제들을 모두 problems에 저장하기
    files = repo.get_contents(f"{user}/{week}") # 폴더 경로

    for content_file in files:
      content = repo.get_contents(f"{user}/{week}/{content_file.name}")
      code = content.decoded_content.decode("utf-8")
      
      boj_id = content_file.name.split("_")[1]

      if boj_id in study_code:
        study_code[boj_id].append((user, content_file.name, code))
      else:
        study_code[boj_id] = [(user, content_file.name, code)]

  for boj_id, elem in study_code.items():
    boj_problem_text = boj.problem_to_markdown(boj.get_problem(boj_id))

    markdown = f"""\
# 문제
{boj_problem_text}
"""

    for user, filename, code in elem:
      reviewed_text = review_ai.review(boj_problem_text, code)
      
      markdown += f"""
## {user}
```{os.path.splitext(filename)[1][1:]}
{code}
```

{reviewed_text}
"""
    with open(f"{boj_id}_AI_코드리뷰.md", "w", encoding="utf-8") as file:
      file.write(markdown)
    
if __name__ == "__main__":
    main()

