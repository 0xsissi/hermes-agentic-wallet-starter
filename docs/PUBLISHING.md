# 一篇长文，配两张图

正文恢复为原来的长版，只调整段落与重点加粗，不再改成精简版。

- [加粗排版稿](X-LONGPOST.md)：在支持 Markdown 的阅读器中查看。
- [复制到 X 专用页](X-PASTE.html)：用浏览器打开，点击“复制正文（含加粗与空行）”，再回 X 替换旧正文并正常粘贴。
- [HTML 加粗预览](X-LONGPOST.html)：与专用复制页同步，保留完整长版内容。
- [纯文本备用](X-LONGPOST.txt)：没有 Markdown 标记，适合直接粘贴正文。

X 长推文支持原生加粗、斜体，见 [X 官方说明](https://help.x.com/en/using-x/x-premium-how-to)。不要依赖 `**文字**`、`# 标题` 等 Markdown 标记在发帖框自动转换。粘贴后检查加粗是否保留；如果没有，按预览稿选中文字，使用 X 编辑器的加粗功能。普通长推文与 Articles 的格式能力不同，本项目仍以单篇长推文为目标。

原预览稿用段落元素和 CSS 段距显示空白，用户实际粘贴到 X 后段落边界丢失，而段内换行仍保留。新版把每个段落之间改成两个明确的换行标签，复制时同时提供带加粗的 HTML 与含真实空行的纯文本，不修改正文。浏览器最终粘贴效果仍以 X 编辑器显示为准。

按顺序上传：

1. [封面](../assets/tutorial-cover.png)：1600 × 1000，突出路线和用途。
2. [四步操作图](../assets/tutorial-steps.png)：1600 × 2000，供读者保存对照。

正文采用“评论「钱包」领取源码包”的方式。现在也可以直接分享 [GitHub 仓库](https://github.com/0xsissi/hermes-agentic-wallet-starter) 或 [入门包下载链接](https://github.com/0xsissi/hermes-agentic-wallet-starter/releases/download/v0.1.0/hermes-agentic-wallet-starter-0.1.0.zip)。本项目不会自动回复、私信或发布。

建议封面替代文字：用 WorkBuddy AI 的免费模型额度，经 Magpie 接入 Hermes 爱马仕，再连接币安 Agentic Wallet；附教程与 MIT 安装脚本。

建议操作图替代文字：安装环境；登录模型并保持 Magpie 运行；选择真实模型 ID 并启动 Hermes；在币安 App 确认配对后，只查询钱包地址和余额。

文字和图示不包含个人钱包地址、登录信息，也不冒充应用实测截图。Windows 环境安装与技能加载已验证，但没有把独立项目描述为已完成 WorkBuddy 登录、模型实际调用和买币的全链路测试。

项目公开仓库：https://github.com/0xsissi/hermes-agentic-wallet-starter 。原始图稿由 [build_cover.py](../scripts/build_cover.py) 绘制，可修改文字后重新生成。社交发布仍由发布者自行操作。
