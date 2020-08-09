---
title: Shadowsocks的配置
tags: 计算机网络
article_header:
  type: cover
  image:
    src: /assets/images/computer_network.jpg
---

之前入手一个vultr的vps，顺便搭了ss梯子，整理一下。

<!--more-->

## 一、SS服务器端配置

[GitHub地址](https://github.com/Chaphlagical/shadowsocks)

**安装：**

```shell
apt-get install python-pip
pip install shadowsocks
```

**参数配置：**

创建文件`/etc/shadowsocks.json` ，编辑以下内容：

```json
{
    "server":"my_server_ip",
    "server_port":8388,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"mypassword",
    "timeout":300,
    "method":"aes-256-cfb",
    "obfs":"plain",
    "obfs_param": "",
    "fast_open": false,
    "workers": 1
}
```

具体参数解释如下：

| Name          | Explanation                                                  |
| ------------- | ------------------------------------------------------------ |
| server        | the address your server listens                              |
| server_port   | server port                                                  |
| local_address | the address your local listens                               |
| local_port    | local port                                                   |
| password      | password used for encryption                                 |
| timeout       | in seconds                                                   |
| method        | default: "aes-256-cfb", see [Encryption](https://github.com/shadowsocks/shadowsocks/wiki/Encryption) |
| fast_open     | use [TCP_FASTOPEN](https://github.com/shadowsocks/shadowsocks/wiki/TCP-Fast-Open), true / false |
| workers       | number of workers, available on Unix/Linux                   |

前台运行：

```shell
ssserver -c /etc/shadowsocks.json
```

后台运行：

```shell
ssserver -c /etc/shadowsocks.json -d start
ssserver -c /etc/shadowsocks.json -d stop
```

## 二、Windows客户端下载

## 三、手机客户端下载

## 四、Ubuntu客户端下载

[下载地址](https://github.com/qingshuisiyuan/electron-ssr-backup/releases)

