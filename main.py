import os
import sys
import boj
import tomllib
import asyncio
import base64
import githubkit
from githubkit import GitHub
from review import ReviewAI

def load_config():
  with open(".env.toml", 'rb') as f:
    config = tomllib.load(f)

  return config

async def get_code_and_review_it(github, review_ai, repo, path, boj_id):
  try:
    resp = await github.rest.repos.async_get_content(
      *repo.split("/"),
      path,
    )
  except githubkit.exception.RequestFailed:
    return ""

  code = base64.b64decode(resp.parsed_data.content).decode("utf-8")

  boj_problem_text = boj.problem_to_markdown(await boj.get_problem(boj_id))

  # async with semaphore:
  reviewed_text = await review_ai.review_chat_completions_api(boj_problem_text, code, os.path.splitext(path)[1][1:])

  print(f"✅ {path} 코드를 리뷰했습니다.")

  return reviewed_text

async def fetch(config, user, selected_dir, github, review_ai):
  try:
    resp = await github.rest.repos.async_get_content(
      *config["code_review"]["github_repo"].split("/"),
      f"{user}/{selected_dir}",
    )
  except githubkit.exception.RequestFailed:
    return []

  files = resp.parsed_data
  tasks = []

  # semaphore = asyncio.Semaphore(2)

  for file in files:    
    task = asyncio.create_task(get_code_and_review_it(
      github, 
      review_ai, 
      # semaphore,
      config["code_review"]["github_repo"], 
      file.path, 
      file.name.split("_")[1],
    ), name=file.name)

    tasks.append(task)
  
  await asyncio.gather(*tasks)

  return tasks

async def main():

  config = load_config()
  selected_dir = sys.argv[1]

  github = GitHub(config["github"]["api_key"])
  review_ai = ReviewAI(config["openai"])

  tasks = []

  for user in config["code_review"]["users"]:
    task = asyncio.create_task(fetch(config, user, selected_dir, github, review_ai), name=user)

    tasks.append(task)

  await asyncio.gather(*tasks)
  review_sum = {}

  for fetched in tasks:
    username = fetched.get_name()

    for review in fetched.result():
      filename = review.get_name()
      boj_id = filename.split("_")[1]

      if boj_id not in review_sum:
        boj_problem_text = boj.problem_to_markdown(await boj.get_problem(boj_id))

        review_sum[boj_id] = f"# 문제\n{boj_problem_text}\n"
        review_sum[boj_id] += f"\n## {username}\n{filename}\n\n{review.result()}\n"
      else:
        review_sum[boj_id] += f"\n## {username}\n{filename}\n\n{review.result()}\n"

  if not os.path.exists("reviews"):
    os.makedirs("reviews")

  for boj_id, markdown in review_sum.items():
    with open(f"reviews/{boj_id}_AI_코드리뷰.md", "w", encoding="utf-8") as file:
      file.write(markdown)


if __name__ == "__main__":
  asyncio.run(main())