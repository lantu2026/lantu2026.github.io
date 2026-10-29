# 符京雷 · 数字教学作品集

常州市新北区汤庄桥小学 · 信息科技教师 · 教师发展处

在线地址：<https://lantu2026.github.io/>

## 结构

```
index.html          总入口（作品集首页：门牌 / 迎宾 / 分流 / 说明）
works/              专业成果（给老师看：讲座、手册、共建平台）
  shuzhi-funeng/      数智赋能 · 网页学件制作实战
  workbuddy-2/        WorkBuddy 教师数字化实战 2.0
  it-teacher-guide/   小学信息老师 WorkBuddy 应用全指南
  qinmei-wiki/        勤美汤小 wiki（教师端投稿 + 云端汇总）
learn/              学生学件（给学生用：即开即用）
  photosynthesis/     光合作用探索实验室
  planting/           种植体验 · 自动定时增湿
  thermos/            保温水壶 · 闭环控制流程图
  lamp/               组装台灯 · 过程与控制
  algorithm-flow/     多场景 · 算法流程图教学工具
  ai-literacy/        小学 AI 素养测评（护眼版）
  ai-literacy-dash/   小学 AI 素养测评（数据大屏）
  it-park/            小学生信息科技乐园
  task-arena/         课堂任务大闯关
  quiz/               课堂知识竞赛（出题版）
  typing/             打字乐园 · 年级闯关
  enumeration/        小智的采购任务 · 枚举算法
docs/
  GitHub教学作品集搭建手记.md   全流程复盘（选型、踩坑、双向门、隐私红线）
tools/
  inject-home-link.py 批量注入「← 作品集」回流入口（幂等，可 --check / --revert）
```

## 双向门

每个子页面左下角都有一个「← 作品集」胶囊，点一下回首页；键盘 `Alt + ←` 同样生效。

需要新增或调整时，不要手工改 16 个文件，跑脚本：

```bash
python tools/inject-home-link.py --apply    # 注入 / 更新
python tools/inject-home-link.py --check    # 检查每页标记份数（正常为 1）
python tools/inject-home-link.py --revert   # 全部撤掉
```

## 复盘文档

完整过程见 [docs/GitHub教学作品集搭建手记.md](docs/GitHub教学作品集搭建手记.md)：为什么选 GitHub Pages、英文界面速查表、七步上线流程、八个真实故障、双向门的设计取舍、隐私红线、可复用清单。


## 发布原则

- **不含学生个人信息**：姓名、学号、成绩、家长联系方式一律不上线
- **不含校内通讯录**：教师手机号等敏感信息不对外发布
- **单文件优先**：学件尽量自包含，减少外部依赖，便于离线使用
- 含真实学生数据的教学工具（班级签到墙、课堂点名评价系统、教务/班务工作台）仅在校内使用，不进入本仓库

## 许可

内容遵循 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)：欢迎同行取用改造，注明出处、非商业用途、相同方式共享。

## 维护

纯静态站点，无构建步骤。改内容直接改 HTML，提交推送即可，GitHub Pages 自动发布。
