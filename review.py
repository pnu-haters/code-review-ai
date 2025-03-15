from openai import AsyncOpenAI


class ReviewAI:
  def __init__(self, openai_config):
    self.client = AsyncOpenAI(
      api_key=openai_config["api_key"],
    )
    self.prompt = openai_config["prompt"]
    self.model = openai_config["model"]

  async def review(self, boj_problem_text, code, code_type):
    response = await self.client.responses.create(
      model=self.model,  # "gpt-4o-mini",
      instructions=self.prompt,
      input=f"다음은 내가 풀어야 하는 문제야.\n{boj_problem_text}\n\n다음은 내 코드야.\n{code}",
    )

    return f"""```{code_type}\n{code}\n```\n\n{response.output_text}"""

  # "o1-mini" o1-mini는 chat.completions을 통해서만 사용 가능함.
  async def review_chat_completions_api(self, boj_problem_text, code, code_type):
    completion = await self.client.chat.completions.create(
      model=self.model,
      messages=[
        {
          "role": "user",
          "content": f"{self.prompt}\n\n다음은 내가 풀어야 하는 문제야.\n{boj_problem_text}\n\n다음은 내 코드야.\n{code}",
        }
      ],
    )

    return f"""```{code_type}\n{code}\n```\n\n{completion.choices[0].message.content}"""
