import aiohttp
from bs4 import BeautifulSoup

async def get_problem(boj_problem_id):
  url = f"https://www.acmicpc.net/problem/{boj_problem_id}"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
  }

  async with aiohttp.ClientSession() as session:
    async with session.get(url, headers=headers) as response:

      html = await response.text()

  soup = BeautifulSoup(html, 'html.parser')
  cells = soup.select_one("#problem-info tbody tr").find_all("td")

  return {
    "title": soup.select_one("#problem_title").getText(),
    "time_limit": cells[0].get_text(strip=True),
    "memory_limit": cells[1].get_text(strip=True),
    "description": soup.select_one("#problem_description").getText(),
    "input": soup.select_one("#problem_input").getText(),
    "output": soup.select_one("#problem_output").getText(),
    # "algorithm_types": soup.select_one("#problem_tags").getText(),
    # 없는 경우가 있다.
  }


def problem_to_markdown(data):
  return f"""\
**제목**: {data["title"]}  
**시간 제한**: {data["time_limit"]}  
**메모리 제한**: {data["memory_limit"]}  

**설명**: {data["description"]}  
**입력**: {data["input"]}  
**출력**: {data["output"]}  
"""