# my-project

画报版+视频展示网站，对应 www.cii.中国 内容。

## 启动

**方法一（推荐）**：双击 `start.bat`
**方法二**：在终端中运行
```powershell
cd C:\Users\Holy\Desktop\my-project
python server.py
```

- 前台：http://localhost:5099
- 后台：http://localhost:5099/admin

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 画报版+视频网站（未来风设计） |
| `admin.html` | 后台分级管理系统 |
| `server.py` | Flask 后端（数据API） |
| `calculator.py` | Python 计算器 |
| `logo.png` | 网站 LOGO |
| `data/*.json` | 磁盘数据文件 |

## 前台功能

- **9 张全屏画报幻灯片**：封面 / 时政深一度 / 后稀缺时代 / 蓝星体系 / 地外文明 / 新闻头条 / 视频中心 / 破茧者说 / 心灯无界
- **中英双语语音播报**：点击 🔊 按钮，先中文后英文朗读
- **自动翻页**：8秒间隔
- **手动翻页**：◀▶ 按钮 / 键盘 ← → 键 / 圆点导航
- **视频中心**：嵌入视频播放，支持后台管理
- **子目录详情**：点击卡片弹出详情弹窗
- **粒子动效**：背景动态粒子效果

## 默认管理员

| 用户名 | 密码 | 角色 |
|--------|------|------|
| superadmin | admin123 | 超级管理员 |
| content | content123 | 内容管理员 |
| template | template123 | 模板管理员 |

## 后台功能

概览 / 栏目内容管理 / 新闻管理 / 视频管理 / 模板管理 / 管理员管理

## GitHub

https://github.com/zuhuawu28-alt/my-project
