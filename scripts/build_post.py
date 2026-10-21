"""Build plain text and a rich-text HTML preview from the reviewed publication draft."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STYLE = """
body { margin: 0; background: #fff; color: #171b1e;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; }
.toolbar { max-width: 720px; margin: 24px auto 0; padding: 20px 28px; background: #f3f6fa; border-radius: 14px; }
.toolbar p { margin: 0 0 14px; line-height: 1.6; font-size: 15px; }
button { cursor: pointer; border: 0; border-radius: 9px; padding: 12px 18px;
  font: inherit; font-size: 15px; background: #1769dd; color: white; margin: 0 8px 10px 0; }
button.secondary { background: #e2e8f0; color: #171b1e; }
#status { display: block; min-height: 24px; font-size: 14px; color: #354555; }
#post { max-width: 720px; margin: 32px auto 80px; padding: 0 28px;
  font-size: 18px; line-height: 1.72; overflow-wrap: anywhere; }
strong { font-weight: 700; }
@media (max-width: 600px) { #post { margin-top: 26px; font-size: 17px; padding: 0 20px; }
  .toolbar { margin: 12px; padding: 18px; } }
"""
SCRIPT = r"""
const post = document.getElementById('post');
const plainText = JSON.parse(document.getElementById('post-text').textContent);
const status = document.getElementById('status');

function copyWithEvent(rich) {
  const selection = window.getSelection();
  const saved = [];
  for (let i = 0; i < selection.rangeCount; i++) saved.push(selection.getRangeAt(i).cloneRange());
  const range = document.createRange();
  range.selectNodeContents(post);
  selection.removeAllRanges();
  selection.addRange(range);
  let handled = false;
  const onCopy = (event) => {
    if (!event.clipboardData) return;
    event.preventDefault();
    event.clipboardData.setData('text/plain', plainText);
    if (rich) event.clipboardData.setData('text/html', '<div>' + post.innerHTML + '</div>');
    handled = true;
  };
  document.addEventListener('copy', onCopy);
  try {
    return document.execCommand('copy') && handled;
  } finally {
    document.removeEventListener('copy', onCopy);
    selection.removeAllRanges();
    for (const previous of saved) selection.addRange(previous);
  }
}

async function copyPost(rich) {
  status.textContent = '正在复制…';
  try {
    if (rich && navigator.clipboard && window.ClipboardItem) {
      const item = new ClipboardItem({
        'text/html': new Blob(['<div>' + post.innerHTML + '</div>'], {type: 'text/html'}),
        'text/plain': new Blob([plainText], {type: 'text/plain'})
      });
      await navigator.clipboard.write([item]);
    } else if (!rich && navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(plainText);
    } else if (!copyWithEvent(rich)) {
      throw new Error('Clipboard unavailable');
    }
  } catch (error) {
    try {
      if (!copyWithEvent(rich)) throw error;
    } catch (_) {
      status.textContent = '浏览器未允许复制。请改用配套 TXT 文件，或选中下方正文复制。';
      return;
    }
  }
  status.textContent = rich
    ? '已复制正文、加粗和空行。请回 X 替换旧正文，按 Ctrl+V 粘贴并检查段落。'
    : '已复制纯文本与空行。请回 X 替换旧正文后粘贴；重点加粗需在编辑器里设置。';
}

document.getElementById('copy-rich').addEventListener('click', () => copyPost(true));
document.getElementById('copy-plain').addEventListener('click', () => copyPost(false));
"""


def main():
    markdown = (DOCS / "X-LONGPOST.md").read_text(encoding="utf-8")
    plain = "\n".join(line.rstrip() for line in markdown.replace("**", "").splitlines()) + "\n"
    (DOCS / "X-LONGPOST.txt").write_text(plain, encoding="utf-8")
    paragraphs = []
    for block in markdown.strip().split("\n\n"):
        block = "\n".join(line.rstrip() for line in block.splitlines())
        content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(block), flags=re.S)
        content = content.replace("\n", "<br>")
        paragraphs.append(content)
    # X kept inline <br> breaks but discarded the old <p> boundaries on paste.
    # Keep paragraph spacing in the clipboard itself, not in CSS margins.
    fragment = "<br><br>".join(paragraphs)
    payload = json.dumps(plain, ensure_ascii=False).replace("<", "\\u003c")
    document = ('<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>币安 Agentic Wallet 长文 · 复制到 X 专用</title>'
                f'<style>{STYLE}</style></head><body>'
                '<div class="toolbar"><p><strong>复制到 X：保留加粗与空行</strong><br>'
                '点下方按钮复制正文，再回到 X 替换旧正文并粘贴。内容与原长版一致。</p>'
                '<button id="copy-rich" type="button">复制正文（含加粗与空行）</button>'
                '<button id="copy-plain" class="secondary" type="button">复制纯文本</button>'
                '<span id="status" role="status" aria-live="polite">复制后请检查 X 编辑器中的段落。</span></div>'
                f'<div id="post" role="article">{fragment}</div>'
                f'<script id="post-text" type="application/json">{payload}</script>'
                f'<script>{SCRIPT}</script></body></html>\n')
    for name in ("X-LONGPOST.html", "X-PASTE.html"):
        (DOCS / name).write_text(document, encoding="utf-8")
    print(f"Built plain and HTML drafts: {len(plain)} characters; {markdown.count('**') // 2} bold spans")


if __name__ == "__main__":
    main()
