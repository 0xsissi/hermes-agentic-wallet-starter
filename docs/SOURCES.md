# 资料核验与来源

核验日期：2026-10-21（Asia/Shanghai）。以下为对应项目维护者或厂商的原始资料，不把搜索结果中的“无限免费”教程当作依据。

| 事项 | 核验结论 | 来源 |
|---|---|---|
| 国际 WorkBuddy AI 费用 | Free 每月 100 积分；新用户 250 积分、14 天有效；活动与模型权益会变化 | [国际订阅政策](https://www.codebuddy.ai/docs/zh/ide/Account/Subscription) |
| 国际版每日活跃奖励 | 当前有活动，要求通过官方客户端形成有效活跃；不能把 Magpie 调用或脚本签到算作必然获得奖励 | [同一政策的活跃奖励部分](https://www.codebuddy.ai/docs/zh/ide/Account/Subscription) |
| 国内版权益 | 体验版 500 积分/月；CLI 访问在表中属于付费权益；免费积分不等于第三方桥接授权 | [国内定价](https://www.codebuddy.cn/docs/workbuddy/Pricing) |
| WorkBuddy 客户端入口 | 国际版与国内版分开登录 | [国际官网](https://www.workbuddy.ai/)、[国内官网](https://www.codebuddy.cn/work/) |
| Magpie 作用 | 本机模型网关，给 Agent 提供供应商模型；支持工具调用转接 | [Magpie 入门文档](https://usemagpie.ai/docs/zh/start) |
| Magpie CLI | 支持 web、models、Hermes 配置和插件登录等命令 | [维护者参考手册](https://github.com/yetone/magpie/blob/main/docs/reference.md) |
| WorkBuddy 桥接 | 社区插件提供 workbuddy 与 workbuddy-ai；新版桌面登录文件可能加密，推荐浏览器登录；不承诺账号可用性 | [插件源码与说明](https://github.com/magpie-community/plugins/tree/main/packages/workbuddy) |
| Hermes 安装 | 有原生 Windows 和 POSIX 安装器；可隔离资料目录；当前 Intel Mac 不受支持 | [官方安装文档](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |
| Hermes 技能 | 支持 Agent Skills，技能默认在 Hermes 资料目录的 skills 子目录 | [官方技能文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| Hermes 记忆 | 有跨会话持久记忆；不是保证自动交易可靠性的依据 | [官方记忆说明](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| 钱包认证 | signin → 展示完整配对码与链接 → 用户 App 确认 → verify → wallet status | [币安认证说明](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-agentic-wallet/references/authentication.md) |
| 交易与确认 | 先查风险、报价和参数，确认后提交；订单号不等于成交，要查终态 | [币安钱包技能](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/binance-agentic-wallet) |
| 钱包服务费 | 根据链、代币类别和入口不同而变化，不能把模型免费写成交易免费 | [币安费用 FAQ](https://www.binance.com/zh-CN/support/faq/detail/87cbb1ca0df34a348eaecb73c26167d7) |

## 固定来源清单

机器可读清单见根目录 `versions.json`：

- Magpie CLI：v0.1.1307，各平台文件 SHA-256 取自维护者 GitHub release 的 digest。
- 币安 CLI：`@binance/agentic-wallet@1.11.0`。
- WorkBuddy 社区插件：`@magpie-community/opencode-workbuddy-auth@0.1.28`。包名包含 OpenCode 是其上游命名，不代表本教程安装或运行 OpenCode。
- 两份币安官方技能固定到 `binance/binance-skills-hub` 的具体提交，下载后核对 Git blob 哈希。
- Hermes 引导脚本固定到原始源码提交并校验 SHA-256；它安装运行时最新稳定版，后续依赖准备由 Hermes 官方 PM 负责。

本项目 MIT 许可只覆盖本项目原创脚本与文档。上游工具、模型服务与技能各自遵循其许可证和服务条款；安装时从上游获取，不把其登录数据或模型服务再分发。
