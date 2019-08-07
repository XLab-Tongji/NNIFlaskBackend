如果利用学校的vpn直接访问实验室的173服务器，则无需进行以下配置。


如果希望在自己的服务器上启动后台服务，则需要按以下说明进行配置。

#### 一、docker配置方法
1.启动docker，命名为```nni```, 挂载于宿主机 ```~/icerno``` 目录下，该目录可自由更改。

```
docker run -p 1100:8080 -p 1101:8081 -p 1102:8082 -p 1500:5000  -ti -d --ipc=host --name="nni"  -v  ~/icerno:/workspace tensorflow/tensorflow:latest-gpu-py3
```

2.根据 [nni官方文档](https://github.com/microsoft/nni/blob/master/README.md) 在docker内通过pip安装nni。

```
python3 -m pip install --upgrade nni
```


3.将本项目置于docker内的```/workspace```路径下

4.用本项目中的[nnictl.py](https://github.com/XLab-Tongji/NNIFlaskBackend/blob/master/nnictl.py)替换源码中的```nnictl.py```，位置位于docker内的```/usr/local/lib/python3.6/dist-packages/nni_cmd```目录下。



####二、依赖安装
```
pip install flask
pip install flask_cors
pip install flask_restful

```

### 三、后端启动方法
```
python app.py
```

### 四、前端路由
[前端项目](https://github.com/XLab-Tongji/NNIFrontend) 中全局搜索10.60.38.173,替换为部署docker的服务器ip地址。