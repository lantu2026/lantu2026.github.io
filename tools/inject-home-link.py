#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给作品集下所有子页面统一注入「返回作品集」回流入口。

设计约束
--------
1. 幂等：以单对 <!-- pf-home:start/end --> 包裹整体，重复运行只保留一份
2. 不侵入：不改动原页面任何布局，只用 fixed 定位浮层
3. 低干扰：左下角半透明胶囊，默认 opacity .55，hover/focus 才完全显形
4. 不遮挡：左下角是各学件最空的区域；避开左上角的 logo / 标题
5. 可打印：@media print 隐藏
6. 手机可用：触屏无 hover，故默认保留可见度；小屏提到 .74
7. 相对路径 ../../ 回仓库根，GitHub Pages 与本地 file:// 均可用

用法
----
    python tools/inject-home-link.py            # 注入 / 更新
    python tools/inject-home-link.py --check    # 只检查不写入
    python tools/inject-home-link.py --revert   # 移除注入
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK_START = "<!-- pf-home:start -->"
MARK_END = "<!-- pf-home:end -->"

PAYLOAD = MARK_START + """
<a id="pf-home" href="../../" aria-label="返回符京雷数字教学作品集" title="返回作品集（Alt+←）"><span class="pf-ar">&larr;</span><span class="pf-tx">作品集</span></a>
<style>
#pf-home{position:fixed;left:14px;bottom:14px;z-index:2147483000;display:inline-flex;align-items:center;gap:5px;height:32px;padding:0 13px 0 11px;border-radius:16px;background:rgba(255,255,255,.93);-webkit-backdrop-filter:blur(10px) saturate(140%);backdrop-filter:blur(10px) saturate(140%);border:1px solid rgba(15,23,42,.13);box-shadow:0 2px 12px rgba(15,23,42,.15);color:#1e293b!important;font:600 13px/1 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif!important;text-decoration:none!important;letter-spacing:.02em;opacity:.9;transition:opacity .2s ease,transform .2s ease,box-shadow .2s ease,background .2s ease;-webkit-tap-highlight-color:transparent;white-space:nowrap}
#pf-home:hover,#pf-home:focus-visible{opacity:1;background:#fff;box-shadow:0 5px 18px rgba(15,23,42,.22);transform:translateY(-1px);outline:none}
#pf-home .pf-ar{font-size:14px;line-height:1;opacity:.65}
@media (hover:none){#pf-home{opacity:.95}}
@media (max-width:520px){#pf-home{opacity:.95;height:30px;padding:0 11px;font-size:12px}}
@media print{#pf-home{display:none!important}}
</style>
<script>
(function(){try{
  if(window.__pfHome)return;window.__pfHome=1;
  document.addEventListener('keydown',function(e){
    if(e.altKey&&e.key==='ArrowLeft'&&!e.ctrlKey&&!e.metaKey){
      var a=document.getElementById('pf-home');if(a){e.preventDefault();location.href=a.getAttribute('href');}
    }
  });
}catch(e){}})();
</script>
""" + MARK_END

PAT = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", re.S)


def targets():
    out = []
    for grp in ("works", "learn"):
        base = os.path.join(ROOT, grp)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            f = os.path.join(base, name, "index.html")
            if os.path.isfile(f):
                out.append(f)
    return out


def strip_all(html):
    """循环剥离，兼容历史遗留的多份标记。"""
    prev = None
    while prev != html:
        prev = html
        html = PAT.sub("", html)
    return html


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--apply"
    files = targets()
    touched = skipped = 0
    for f in files:
        with open(f, "r", encoding="utf-8", errors="surrogateescape") as fh:
            html = fh.read()
        rel = os.path.relpath(f, ROOT).replace("\\", "/")

        if mode == "--check":
            n = len(PAT.findall(html))
            print(f"{'✅' if n == 1 else '⚠️ '} 标记 {n} 份  {rel}")
            continue

        clean = strip_all(html)

        if mode == "--revert":
            if clean != html:
                with open(f, "w", encoding="utf-8", errors="surrogateescape") as fh:
                    fh.write(clean)
                touched += 1
                print("已移除  " + rel)
            else:
                skipped += 1
            continue

        low = clean.lower()
        if "</body>" not in low:
            print("跳过（无 body）  " + rel)
            skipped += 1
            continue
        idx = low.rfind("</body>")
        new = clean[:idx] + PAYLOAD + "\n" + clean[idx:]
        if new != html:
            with open(f, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(new)
            touched += 1
            print("已注入  " + rel)
        else:
            skipped += 1
            print("无变化  " + rel)

    print("-" * 46)
    print(f"共 {len(files)} 个页面｜改动 {touched}｜跳过 {skipped}")


if __name__ == "__main__":
    main()
