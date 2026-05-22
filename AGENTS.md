# my-project

对应 www.cii.中国 内容 — 门户网站 + 后台管理系统

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
| `index.html` | 门户前台（从服务器加载动态数据，应用模板CSS） |
| `admin.html` | 后台管理系统（文章/栏目/视频/留言/模板/管理员） |
| `server.py` | Flask 后端（完整CRUD API + 上传 + 留言） |
| `data/*.json` | 磁盘持久化数据文件 |
| `uploads/images/` | 上传的图片目录 |
| `logo.png` | 网站 LOGO |
| `calculator.py` | Python 计算器 |

## 数据模型

### Article（文章）
```json
{
  "id": "a_xxx",
  "section": "shizheng",
  "title": "标题",
  "content": "正文HTML",
  "images": ["/uploads/xxx.jpg"],
  "videos": [{"title": "视频", "url": "https://..."}],
  "comments": [{"id": "c_xxx", "user": "访客", "content": "...", "time": "...", "approved": false}],
  "source": "新华社",
  "date": "2026-04-30",
  "featured": true
}
```

### Template（模板）
每个模板包含 CSS 变量（:root），切换后前台自动应用新视觉风格。

## 前台功能
- **门户布局**：顶部导航 + 头条精选 + 栏目文章网格 + 视频中心 + 页脚
- **文章详情弹窗**：显示标题、来源、日期、图片、视频、正文内容
- **留言互动**：用户可在文章下方提交留言（需后台审核通过后显示）
- **模板切换**：后台切换模板后前台自动变色（颜色、字体、背景等）

## 后台功能

| 功能 | 说明 |
|------|------|
| 概览 | 文章/栏目/视频/留言统计数据 |
| 文章管理 | 按栏目筛选，支持富文本编辑，图片URL/上传，视频嵌入 |
| 栏目管理 | 添加/删除栏目 |
| 视频管理 | 添加/删除视频 |
| 留言审核 | 审核/删除访客留言 |
| 模板管理 | 添加/删除/切换模板，自定义CSS变量编辑器 |
| 管理员 | 添加/删除管理员 |

## 默认管理员

| 用户名 | 密码 | 角色 |
|--------|------|------|
| superadmin | admin123 | 超级管理员 |
| content | content123 | 内容管理员 |
| template | template123 | 模板管理员 |

## 角色权限

- **superadmin**：所有功能
- **content**：文章管理 + 栏目管理 + 视频管理 + 留言审核
- **template**：模板管理（创建/编辑CSS/切换）

## 模板CSS变量

```
--bg        背景色
--bg2       次要背景
--primary   主色
--secondary 辅色
--accent    强调色
--text      文字色
--text2     次要文字
--text3     淡色文字
--border    边框色
--card-bg   卡片背景
--font      字体
--radius    圆角
--hero-grad 渐变
```

## API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 登录 |
| `/api/logout` | POST | 退出 |
| `/api/session` | GET | 获取会话 |
| `/api/session/check` | GET | 校验会话 |
| `/api/data` | GET/POST | 完整数据 |
| `/api/frontend-data` | GET | 前台数据 |
| `/api/template/css` | GET | 当前模板CSS |
| `/api/comment` | POST | 提交留言 |
| `/api/comments` | GET | 所有留言 |
| `/api/comments/approve` | POST | 审核留言 |
| `/api/comments/delete` | POST | 删除留言 |
| `/api/upload` | POST | 上传图片 |

## GitHub

https://github.com/zuhuawu28-alt/my-project
