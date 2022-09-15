# PoemsBackServer-Flask
    诗词后端

## venv虚拟环境安装
***Mac***
   * 参看 https://www.lizenghai.com/archives/8528.html

***Ubuntu***
   * 暂无  
   
***Windows***
   * 暂无

## venv 环境启动
***在项目根目录下***
* virtualenv --no-site-packages venv 生成当前项目的venv
* source venv/bin/activate  进入当前项目的venv
* deactivate                退出venv


## 线上环境部署（Nginx+Gunicorn+Supervisor）

***1.安装venv***
* pip3 install virtualenv                  安装virtualenv
* cd /data/www/my_poemsServer
* which python3 -> /usr/bin/python3
* virtualenv -p /usr/bin/python3 venv      在项目根目录下生成 virtualenv相关的环境文件，已有就不再生成


***2.安装Gunicorn***
* python web 环境
* 安装 pip3 install gunicorn
* 启动 gunicorn -w 4 -b ip:5000 run:app 


***3.安装supervisor***
* 确保程序的自动启动保活
* apt-get install supervisor
* cd /etc/supervisor/conf.d
* vim poemsServer.conf 添加以下
    - [program:poemsServer]
    - command=/root/www/PoemsServer/venv/bin/gunicorn -b 192.168.1.105:5000 -w 4 run:app
    - directory=/root/www/PoemsServer
    - user=root
    - autostart=true
    - autorestart=true
    - stopasgroup=true
    - killasgroup=true


***4.安装MySql替换sql***
* 安装所需的扩展 pip3 install pymysql
* 安装mysql apt-get mysql 
* 设置root用户及密码
* 添加poemsServer用户 并设置相关数据库访问权限
* 在.env 文件中添加 DATABASE_URI=mysql+pymysql://poemsServer:my-poemsServer1234@localhost:3306/poemsServer


***5.安装ningx***
* 暂无

***6.启动线上服务***
* cd /data/www/my_poemsServer
* . venv/bin/activate                          开启virtualenv
* gunicorn -w 4 -b 127.0.0.1:5000 run:app      开启gunicorn
* service nginx start                          开启nginx
* 若supervisor、nginx 已安装配置完成，直接启动 supervisoctl start 即可 

## 更新代码
* 需在venv中
* git pull
* sudo supervisorctl stop poemsServer
* flask db upgrade
* flask translate compile
* sudo supervisorctl start poemsServer


## 开发调试
***1.邮件***
* 终端1 python3 -m smtpd -n -c DebuggingServer localhost:8025
* 终端2 set MAIL_SERVER=localhost  set MAIL_PORT=8025

***2.requirements.txt 自动生成***
* pip3 freeze > requirements.txt

***3.flask-migrate***
* .env文件中 FLASK_APP=run.py 
* flask db init
* flask db migrate -m 'init migrate'
* flask db upgrade
* flask db history
    - 输出格式： 版本号 (head), initial migration
* flask db downgrade 版本号

***4..env .flaskenv***
* 需依赖 python-dotenv 安装包
* 添加 .env 文件
* 设置程序运行入口文件
   - FLASK_APP=run.py 
    
***5.添加自定义flask命令***
* import click 添加命令行参数 
   - @click.argument('lang')
* import app.cli 添加自定义命令
   - @app.cli.group(name='自定义命令组名称',help='命令组功能描述') 添加命令组
   - @自定义命令组名称.command(name='自定义命令',help='命令功能描述')
* 必须将自定义命令command.py 导入到入口脚本中(run.py)
* 自定义命令组使用
   - flask 自定义命令组名称 自定义命令 参数


***6.语言本地化***
######flask—babel 安装使用翻译功能
* pip安装flask-babel扩展
* 根目录下添加配置文件babel.cfg
   - [python: app/**.py]
   - [jinja2: app/templates/**.html]
   - extensions=jinja2.ext.autoescape,jinja2.ext.with_
* cd /data/www/my_poemsServer
* pybabel extract -F babel.cfg -k _l -o messages.pot .   根据babel.cfg 读取_()_l()标记的代码和模版，生成.pot文件
* pybabel init -i messages.pot -d app/translations -l zh  生成中文语言目录及相关的对照翻译文档.po
* pybabel compile -d app/translations                   编译.po文件生成.mo文件，用于应用加载翻译

######flask—babel 更新翻译
* cd /data/www/my_poemsServer
* pybabel extract -F babel.cfg -k _l -o messages.pot .   
* pybabel update -i messages.pot -d app/translations
* pybabel compile -d app/translations  

######flask—babel 翻译函数使用
* _() 用于request,如route .html中
* _l() 用于form中 from flask_babel import lazy_gettext as _l
* _('Hi,%(username)s.Welcome to login!',username=current_user.username)) 其中%(username)s是格式符号

 
   
                                                                                       