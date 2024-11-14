# 这玩意得研究一下，免费的
# 但是太慢了

from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "HELLO"}],
    # Add any other necessary parameters
)
print(response.choices[0].message.content)
