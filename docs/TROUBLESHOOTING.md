# 排错：按实际错误处理

## node 找不到，或版本太低

从 [nodejs.org](https://nodejs.org/) 安装 Node.js 24 LTS（至少 24.5），关闭旧终端，再打开终端运行 `node --version`。

## 安装卡在下载

首次安装会下载 Hermes 的运行环境，不只是几份文字技能。先看终端是否还在输出下载或安装信息，不要同时反复运行安装器。

若网络需要代理，使用你已经配置好的本机 HTTP(S) 代理：

```text
node starter.mjs install --proxy http://127.0.0.1:你的真实端口
```

端口必须是你的软件实际提供的端口，不能照抄别人的。Windows 下脚本会尝试使用已启用的本机系统代理；PAC、自定义远程代理或 SOCKS 地址不会自动转换。需要时显式给 HTTP(S) 地址。

代理只传给本次进程和子进程，不改系统设置；127.0.0.1 上的 Magpie 网关保持直连。脚本不会替你注册代理服务。

## SHA-256 校验失败

停止安装。核对项目来源、`versions.json` 与对应官方发布。不要删除哈希检查或关闭 TLS 校验。维护者应核实上游版本后更新清单。

## Windows 报 Get-FileHash 不存在

脚本会优先使用已安装的 PowerShell 7；没有时使用 Windows PowerShell，并在该子进程移除可能不兼容的 `PSModulePath`。若仍失败，安装官方 PowerShell 7 后重试。无需修改系统执行策略。

## Python / uv 报安装目录冲突

当前脚本将引导 Python 的下载目录和缓存也隔离在 `.runtime/`。不要把你自己的 Python 或 uv 目录删掉。更新项目脚本后重试同一项目的 `install`；安装器会保留并尝试修复本项目已经下载的内容。

## WorkBuddy 登录成功，模型却不能调用

先核对登录地区：国际版是 `workbuddy-ai`，国内版是 `workbuddy`。使用 `models` 里返回的真实 ID，并查看本人套餐与可用模型。

社区插件的兼容性不是腾讯的可用性承诺。若返回不支持渠道、账号限制或风控错误，保留原始错误，停止测试，通过 WorkBuddy 官方帮助渠道处理；不通过改身份、批量账号或其他方式绕过。

当前插件使用浏览器登录。不要尝试解密或导出新版 WorkBuddy 的桌面登录文件。

## Magpie 没有 WorkBuddy 登录插件

重新运行 `node starter.mjs workbuddy-login`，它会添加 `versions.json` 固定的社区插件，再发起浏览器登录。

若你已有 Magpie 的插件配置冲突，先在自己的 Magpie 插件页确认哪个插件在提供 `workbuddy-ai`；不要直接删除整个 Magpie 配置目录。

## Hermes 说模型网关连接失败

先在第一个终端运行并保持：

```bash
node starter.mjs magpie-ui
```

再在另一个终端运行 `node starter.mjs doctor`。安装器不会把本机网关暴露到公网，也没有要求你开放路由器端口。

如果手动配置了模型，注意 Magpie 对 Hermes 的命令可能需要 `magpie/` 供应商前缀。请用本项目 `set-model`，它会选择正确前缀并核对 `model.provider=magpie`。模型不在当前目录里时会停止，不会静默改用默认付费供应商。

## 本来装过 Hermes，这个脚本为什么又装一个？

为避免覆盖已有记忆、配置和技能，本教程使用 `.runtime/hermes-home` 与 `.runtime/hermes-source`。请用 `node starter.mjs agent` 启动这个助手；单独运行全局 `hermes` 不一定是同一份配置。

`install --skip-hermes` 只用于维护者检查其余组件，不是一条完整的新手安装路线。

## Intel Mac 能不能用？

当前 Hermes 官方将 Intel Mac 列为不支持的平台。本项目会阻止该平台默认安装 Hermes。请使用官方支持设备；`--skip-hermes` 不会让 Hermes 在不支持平台上运行。

## 币安显示登录成功，电脑却未连接

重新运行 `wallet-login`，用新配对页面，在 App 核对配对码并确认。保持验证进程运行直到结束。只以官方 CLI 查询到 `CONNECTED` 为准。

不要把二维码、配对页面、`.runtime/baw` 或任何登录文件发到公开群聊、推文或 GitHub issue。

## wallet status 返回 illegal parameter

若本项目还没有完成第一次扫码登录，先运行 `wallet-login`。公开教程不能把这个错误解释为“交易成功”或“余额为零”。已完成登录仍报错时，保留错误并查官方支持，不反复提交交易。

## 报金额过小 / 没有路由 / 余额不足

这是报价或交易条件问题，不一定是安装失败。不要让 AI 擅自提高金额、增加滑点或改买别的代币。

## 开发者模式没开

正常市价 DEX 兑换不要求先为本教程开启开发者模式。自定义合约调用需要时，由用户在币安 App 开启；CLI 只能读设置。按官方流程先预览，解释风险，再确认执行。

## 关闭、更新与迁移

关闭 `agent` 和 `magpie-ui` 所在终端即可结束这些前台进程。钱包会话可能仍然有效；需要断开时，读取官方说明后运行：

```bash
node starter.mjs baw auth signout --json
```

不要在安装完成后随意移动项目文件夹：Hermes 的启动器可能记录安装路径。迁移前先阅读 Hermes 官方迁移文档，不要把包含登录凭据的 `.runtime` 当作开源项目发给其他人。

更新应先看官方版本与变更说明，再更新校验清单。此脚本不是自动追最新版本的更新器。
