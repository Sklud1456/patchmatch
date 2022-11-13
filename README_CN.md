# Patchmatch flask demo

## 需要的软件环境

python、mysql、nodejs

## 启动的方式

>首先在mysql导入data.sql文件。

data.sql文件位于https://drive.google.com/file/d/1CX1lxH5SZ3NhGpolkuO-vgW-UzEeetFf/view，需要先行下载。由于我使用的navicat的可视化界面，所以并不清楚如何在命令行导入data.sql的方法，这一点可以自行在网上搜索。在成功导入后，可以在数据库中看到all
_cve、cve、repo、totalcommit、vc_feature等五张表，其中的cve表中预先删除了一个数据，可以供你进行模型的使用尝试。

同时由于数据库设置的不同，需要在manage.py中更改SQLALCHEMY_DATABASE_URI的参数，将其调整为你电脑上对应数据库的信息。

> 其次准备python所需的环境

其中所需要的主要库在requirements.txt中列出，可以根据你使用的电脑配置进行调整。可以使用pip，也可以使用conda进行安装。若想一键安装，pip指令如下：

```python
activate (yourenv)#进入你电脑上特定的虚拟环境
(yourenv)pip install -r requirements.txt
```

但我并不是很推荐，因为不同的电脑配置不同，可能并不兼容这些库的版本。

> 然后通过npm命令搭建前端所需环境
```python
npm install
```
使用该命令后，nodejs会根据package.json文件自动进行环境配置。

> 在所有环境搭建完成后可以通过以下命令启动程序。
```python
python manage.py #开启后端服务

npm run dev#开启前端服务
```

在启动后，等待浏览器自动打开 http://localhost:8080

注：

上述npm和python命令需要在patchmatch-main的路径下才能正常使用。

由于每个人电脑环境不同，使用上述操作步骤可能不一定能正常启动应用，可以在github上留言或求助于Stack Overflow。
