import requests
from bs4 import BeautifulSoup
from textwrap import dedent

def get_problem(boj_problem_id):
  url = f"https://www.acmicpc.net/problem/{boj_problem_id}"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
  }

  response = requests.get(url, headers=headers)
  html = response.text

  soup = BeautifulSoup(html, 'html.parser')

  return {
    "title": soup.select_one("#problem_title").getText(),
    "info": soup.select_one("#problem-info").getText(),
    "description": soup.select_one("#problem_description").getText(),
    "input": soup.select_one("#problem_input").getText(),
    "output": soup.select_one("#problem_output").getText(),
    # "algorithm_types": soup.select_one("#problem_tags").getText(),
    # 없는 경우가 있다.
  }


def problem_to_text(data):
  return dedent(f"""
      제목: {data["title"]}
      정보: {data["info"]}
      설명: {data["description"]}
      입력: {data["input"]}
      출력: {data["output"]}
    """)
