# 这玩意得研究一下，免费的
# 但是太慢了 寻找代理
import httpx
from g4f.client import Client

# 需要启动崔老师的ProxyPool项目
proxypool_url = 'http://127.0.0.1:5555/random'

def get_proxy() -> str:
    proxy = "http://" + httpx.get(proxypool_url).text.strip()
    print(proxy)
    return proxy

def main():
    client = Client()
    proxy = get_proxy()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "你是谁"}],
            proxy=proxy,
        )
        print(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == '__main__':
    main()
