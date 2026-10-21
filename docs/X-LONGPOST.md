**让爱马仕接上币安钱包：用免费模型额度，搭一个能查余额、看报价的 AI 助手**

最近在研究币安 Agentic Wallet，我把适合小白的入门路线整理成了教程，还配了一套 **MIT 开源安装脚本**。

不用先买 AI 订阅，先从 WorkBuddy AI 的免费额度开始。想自己操作就照着下面做；不想敲命令，也可以把源码包交给能操作电脑的 AI 帮你安装。

这套组合是：  
**WorkBuddy AI → Magpie → Hermes（爱马仕）→ 币安 Agentic Wallet**

先把名字说成人话：  
• WorkBuddy AI：提供模型，相当于大脑。  
• Magpie：把模型接给本机助手，相当于接线。  
• Hermes：理解你的话、调用技能，负责干活。  
• Agentic Wallet：在你授权的权限内处理钱包签名。

**为什么这次用爱马仕？**  
因为目标是长期放在电脑里用的个人助手。它支持技能和记忆，接好以后，可以继续用中文查地址、查余额、准备交易。钱包私钥不需要交给 AI。

下面以国际 WorkBuddy AI 为主，国内版放在后面。

**① 先装环境**

准备电脑、本人 WorkBuddy AI 账号，以及支持 Agentic Wallet 的币安账号和 App。先从 nodejs.org 安装 Node.js 24 LTS。

拿到配套源码包后解压，在解压后的项目文件夹打开终端，输入：

node starter.mjs install

脚本会安装所需环境、Magpie、Hermes 和币安官方钱包技能。第一次需要下载依赖，等它跑完。

**② 登录模型，保持 Magpie 开着**

按顺序输入：

node starter.mjs workbuddy-login  
node starter.mjs magpie-ui

在浏览器登录本人的国际 WorkBuddy AI 账号，查看额度。**Magpie 页面和这个终端保持运行。**

**③ 选模型，启动爱马仕**

再开一个终端，仍然进入同一个项目文件夹，输入：

node starter.mjs models

从列表中复制一个本人账号可用的 workbuddy-ai/… 完整模型 ID。**下面的「真实模型ID」要替换，别原样照抄：**

node starter.mjs set-model workbuddy-ai/真实模型ID  
node starter.mjs agent

启动后先发一句：“请用中文回复：模型连接正常。”

**能正常回复，再接钱包。** 如果模型列表为空，先解决登录或账号可用性，别急着往钱包里充钱。

**④ 扫码接钱包，先做一次查询**

把这段话发给爱马仕：

“先读取 binance-agentic-wallet 技能和认证说明，再用当前项目的 node starter.mjs wallet-login 连接币安 Agentic Wallet。完整展示配对码和官方链接，等我在币安 App 核对确认；保持登录验证运行，直到显示 CONNECTED。之后只查 BSC 钱包地址和余额，不买币、不转账。”

在币安 App 核对并确认。**电脑显示 CONNECTED，才算连接完成。**

以后可以直接说：  
“查一下我在 BSC 上的 BNB 和 USDT 余额。”  
“拿 0.0001 BNB 换 USDT 的报价，列出预计到账、费用和滑点，只报价。”

真要买币时，把链、完整合约、金额说清楚，**先看风险、报价和费用，再明确确认执行。** 提交后还要查交易结果。

**不想自己操作？** 把源码包交给能使用本机终端的 AI，再发这句话：

“请按项目里的 docs/AI-INSTALL-PROMPT.md 帮我安装。先检查环境，再安装、登录模型、测试回复。需要扫码时由我操作；最后只查钱包地址和余额，不做交易。”

普通网页豆包如果没有电脑操作权限，只能教你操作；有本机执行权限的 AI 才能代装。登录和扫码也需要你本人完成。

**关于「免费」，有三点要说清楚：**

• 国际 WorkBuddy AI 当前 Free 套餐为每月 100 积分，新用户另有 250 积分、14 天有效；以本人页面为准，不是无限调用。  
• 国内版登录可用 node starter.mjs workbuddy-login --region cn。国内免费额度与 CLI 权益不同，不能把国际版的可用性直接套过去。  
• **免费说的是模型额度。买币本金、链上 Gas、可能产生的钱包交易服务费另算。**

这是一套社区接入方案，并非几家厂商联合推出的产品。Windows 下的安装环境、技能加载和脚本检查已经验证；WorkBuddy 账号登录到 Hermes 实际调用，仍需用你自己的账号测试。

完整教程、排错说明、安装提示词和 MIT 源码包都整理好了。

**需要的评论区回复「钱包」领取。** 建议先收藏，第一次照着做，后面就可以直接用中文跟钱包助手交流了。

后续继续分享我实际研究的 AI × 链上工具。

资料口径：2026-10-21。国际额度说明：  
https://www.codebuddy.ai/docs/zh/ide/Account/Subscription
