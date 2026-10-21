# 只看这一页：四步接好钱包助手

**先装环境，再登录，最后查询。安装不等于授权交易。**

## 第一步：准备并安装

安装 [Node.js 24 LTS](https://nodejs.org/)，下载入门包并解压，在文件夹打开终端，输入：

```bash
node starter.mjs install
```

等到出现“安装完成”。首次需下载运行环境，保持终端开着。

## 第二步：登录模型账号

```bash
node starter.mjs workbuddy-login
node starter.mjs magpie-ui
```

在浏览器登录本人的国际 WorkBuddy AI 账号，检查免费额度。Magpie 页面和终端保持运行。

## 第三步：把模型接给爱马仕

另开一个终端，进入同一文件夹：

```bash
node starter.mjs models
```

复制一个本人账号可用的 `workbuddy-ai/…` 完整 ID，替换下面的占位文字：

```text
node starter.mjs set-model workbuddy-ai/真实模型ID
node starter.mjs agent
```

在 Hermes 中发“请用中文回复模型连接正常”。能回复，才算这次模型调用成功。

## 第四步：扫码接钱包

对 Hermes 说：

```text
先读取 binance-agentic-wallet 技能和认证说明，再用当前项目的
node starter.mjs wallet-login 连接币安 Agentic Wallet。
完整展示配对码与链接，等我在 App 核对确认；保持验证运行，检查到 CONNECTED。
之后只查询 BSC 钱包地址和余额，不买币、不转账。
```

接下来就可以用中文查钱包、拿报价。买币时另行确认币种、金额、滑点和风险。

**免费额度不等于免费交易。** 模型用量看本人账号；本金、Gas、钱包服务费另算。

出错看 [排错](TROUBLESHOOTING.md)，完整步骤看 [教程](TUTORIAL.md)。有本机终端权限的 AI 可照 [安装提示词](AI-INSTALL-PROMPT.md) 代装；普通网页聊天只能指导你操作。
