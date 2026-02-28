# Django 企业后台管理系统

这是一个基于 Django + Bootstrap 5 + ECharts 开发的企业后台管理系统，包含了用户管理、部门管理、靓号管理、任务发布、订单处理及数据可视化等功能。

## 功能模块

- **部门管理**: 部门的增删改查。
- **用户管理**: 员工信息的维护（包含入职时间、账户余额等）。
- **靓号管理**: 手机靓号资源的录入与状态管理。
- **任务管理**: 任务发布与分发。
- **订单管理**: 订单处理流程。
- **数据统计**: 基于 ECharts 的柱状图、饼图数据展示。
- **权限认证**: 包含登录、注销及图片验证码功能。

## 技术栈

- **后端**: Python 3, Django 5
- **前端**: Bootstrap 5, jQuery, ECharts
- **数据库**: SQLite (默认) / MySQL (可选)

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8+。

安装项目依赖：

```bash
pip install -r requirements.txt
```

### 2. 数据库配置

项目默认使用 **SQLite** 数据库，无需额外配置即可直接运行。

> **注意**: 如果需要使用 **MySQL**，请修改 `DjangoProject/settings.py` 中的 `DATABASES` 配置，并确保已创建对应的数据库。

### 3. 初始化

进行数据库迁移：

```bash
python manage.py migrate
```

### 4. 运行项目

```bash
python manage.py runserver
```

启动后访问：[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

## 默认管理员账号

- **用户名**: `admin`
- **密码**: `123456`

## 目录结构

- `app01/`: 核心应用目录
  - `views/`: 视图函数（业务逻辑）
  - `models.py`: 数据模型
  - `templates/`: HTML 模板
  - `utils/`: 工具类（加密、分页、验证码等）
- `static/`: 静态文件（CSS, JS, 插件）
- `DjangoProject/`: 项目配置文件
