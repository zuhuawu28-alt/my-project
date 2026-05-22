# my-project

项目包含 Python 计算器、Cii.中国 画报版网站、后台管理系统。

## 文件说明

- **calculator.py**：Python 交互式计算器（+ - * / ^ %）
- **index.html**：Cii.中国 画报版展示网站（全屏幻灯片）
  - 栏目：时政深一度 / 后稀缺时代 / 蓝星体系 / 地外文明 / 破茧者说 / 心灯无界
  - 点击卡片可展开子目录详情弹窗
  - 功能：语音播报(Web Speech API)、自动8秒翻页、手动翻页(箭头/键盘/圆点)
  - LOGO 显示在左上角
- **admin.html**：后台管理系统
  - 登录地址：admin.html
  - 分级管理员：超级管理员 / 内容管理员 / 模板管理员
  - 功能：栏目内容管理、新闻管理、模板切换、管理员管理
- **logo.png**：网站 LOGO

## 默认管理员账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| superadmin | admin123 | 超级管理员（全部权限） |
| content | content123 | 内容管理员 |
| template | template123 | 模板管理员 |

## 运行方式

- `python calculator.py` — 运行计算器
- 双击 `index.html` — 打开画报版网站
- 双击 `admin.html` — 打开后台管理

## GitHub

- https://github.com/zuhuawu28-alt/my-project
- 提交：`git add . && git commit -m "信息"`
