# 野鱼

> v0.1.0

## 简介

一个 [Telegram Bot](https://core.telegram.org/bots/api)，[灵感买家俱乐部](https://club.q24.io/)·鮀浦镇 里的小小管理员。

这是一个功能不太复杂的 Bot，或许可以用来初探 Bot 开发。


## 基本功能
### 发送群组消息到频道
在群内发送的消息中带上特定标签（如：`#分享发现`），该条消息便会同步到[野鱼日报](https://t.me/ideabuyersclub)。
也可以回复想要分享的消息，同时发送特定的指令（如：`/share`）。

#### 分享发现
1. 标签：`#分享发现`
2. 指令：`/share`

#### 上电视
1. 标签：`#上电视`
2. 指令：`/tv`

### 野鱼之声
解析音乐链接为音频，支持一条消息包含多条音乐链接。

#### 聊天模式
私聊或群组直接发送带音乐链接的文字消息，等待下载完毕即可收听。

#### 频道模式
发送带音乐链接的消息，同时带上标签 `#野鱼屏幕`，即可发送音乐到[野鱼日报](https://t.me/ideabuyersclub)。

### 心象局
每天早晨发送一条投票，根据投票结果修改群组的标题。

### 易书馆（待开发）
- 书籍格式转换
- PDF -> 图片

## 其他指令
- `/about`：关于我们

## 部署
### 配置
新建一个 `config.ini` 文件，添加相关私密数据的变量。

你需要一个 Bot Token，请找 [Bot Father](https://t.me/BotFather) 领取。

### 开发依赖

`python -m pip install -r requirements.txt` 以下载所有依赖。
