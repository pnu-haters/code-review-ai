import os
import sys
import tomllib
from github import Github

def load_config():
  with open(".env.toml", 'rb') as f:
    config = tomllib.load(f)

  return config


def main():
  config = load_config()
  week = sys.argv[1]
  
  g = Github()

  repo = g.get_repo(config["code_review"]["github_repo"])

  for user in config["code_review"]["users"]:
    files = repo.get_contents(f"{user}/{week}") # 폴더 경로

    for content_file in files:
      print(f"이름: {content_file.name}, 타입: {content_file.type}")


  


if __name__ == "__main__":
    main()

