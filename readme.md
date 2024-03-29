如果利用学校的vpn直接访问实验室的173服务器，则无需进行以下配置。

实验室173服务器的linux系统信息如下 (uname -a)：

```
Linux server173 4.4.0-154-generic #181-Ubuntu SMP Tue Jun 25 05:29:03 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

docker版本如下 (docker -v)：

```
Docker version 18.09.0, build 4d60db4
```


如果希望在自己的服务器上启动后台服务，请自行安装对应版本的docker，并按以下说明进行配置。

#### 一、docker配置方法
1.启动docker，命名为```nni```, 挂载于宿主机 ```~/icerno``` 目录下，该目录可自由更改。

```
docker run -p 1100:8080 -p 1101:8081 -p 1102:8082 -p 1500:5000  -ti -d --ipc=host --name="nni"  -v  ~/icerno:/workspace tensorflow/tensorflow:latest-gpu-py3
```

关于命令中各参数的含义，可自行参阅docker相关技术手册。 启动nni容器后，可以进入nni容器内部：

```
docker exec -it nni bash
```

2.根据 [nni官方文档](https://github.com/microsoft/nni/blob/master/README.md) 在nni容器内部安装nni。

```
python3 -m pip install --upgrade nni
```


3.将本项目置于docker内的```/workspace```路径下

4.用本项目中的[nnictl.py](https://github.com/XLab-Tongji/NNIFlaskBackend/blob/master/nnictl.py)替换源码中的```nnictl.py```，其位置在nni容器内部的```/usr/local/lib/python3.6/dist-packages/nni_cmd```目录下。



#### 二、依赖安装
在nni容器内部执行以下命令：

```
pip install flask
pip install flask_cors
pip install flask_restful

```

#### 三、后端启动方法
在nni容器内部，进入本项目所在的目录，执行本项目的入口文件：

```
python app.py
```
如启动信息如下图所示，则说明后台正常启动。

![](https://github.com/XLab-Tongji/NNIFlaskBackend/blob/master/pic/start.png)

#### 四、前端路由
在[前端项目](https://github.com/XLab-Tongji/NNIFrontend) 中全局搜索`10.60.38.173`(这是实验室173服务器的地址),替换为当前部署了nni容器的服务器的ip地址。