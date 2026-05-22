# my-project

项目包含 Python 计算器、Cii.中国 画报版网站、后台管理系统、Flask 后端。

## 文件说明

| 文件 | 说明 |
|------|------|
| `calculator.py` | Python 交互式计算器（+ - * / ^ %） |
| `index.html` | Cii.中国 画报版展示网站（全屏幻灯片） |
| `admin.html` | 后台管理系统（需通过 server.py 访问） |
| `server.py` | Flask 后端服务器（数据存储 API） |
| `logo.png` | 网站 LOGO |
| `data/*.json` | 磁盘持久化数据文件 |

## 启动方式

```powershell
python server.py
```

- 前台：http://localhost:5099
- 后台：http://localhost:5099/admin

## 默认管理员账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| superadmin | admin123 | 超级管理员 |
| content | content123 | 内容管理员 |
| template | template123 | 模板管理员 |

## 前台功能

- 点击卡片展开子目录详情弹窗
- 语音播报（Web Speech API）
- 自动 8 秒翻页 / 手动翻页（箭头/键盘/圆点）
- LOGO 显示在左上角

## GitHub

- https://github.com/zuhuawu28-alt/my-project
