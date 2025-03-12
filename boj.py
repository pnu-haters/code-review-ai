import re
import json
import base64
import requests

def get_problem(boj_problem_id):
  url = f"https://www.acmicpc.net/problem/{boj_problem_id}"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
  }

  response = requests.get(url, headers=headers)
  html = response.text

  matched = re.search(r'<div id="problem-lang-base64">(.*?)</div>', html)

  if not matched:
    raise Exception(f"백준 {boj_problem_id} 문제를 정상적으로 가져올 수 없습니다.")
  
  decoded = base64.b64decode(matched.group(1))
  boj_data = json.loads(decoded)

  print(boj_data[0])

  return boj_data[0]