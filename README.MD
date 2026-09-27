<p align="center"><img src="assets/cockpit-logo.png" width="280" alt="cockpit 驾驶舱" /></p>

<p align="center"><strong>cockpit 驾驶舱 · AI 开发与内容工作流</strong></p>
<h1 align="center">把案例做成系统，把过程变成作品。</h1>
<p align="center">从需求整理、AI 开发到图文、视频与代码交付，让每一步都有记录。</p>
<p align="center">喜文FDE案例系列 · Python · MIT</p>
<p align="center"><a href="https://resume.fangnan.club/cockpit/">了解 cockpit</a> · <a href="https://resume.fangnan.club/">认识作者</a> · <a href="LICENSE">MIT 许可证</a></p>

## 认识作者，一起把想法做出来

**我是方楠，智能体工程师 / 全栈工程师。**

专注 AI 编程、智能体开发与业务系统落地，具备 Python、前后端开发、数据工程与技术交付经验。这个项目记录我如何把具体需求拆成开发任务，再把系统实现、操作演示和项目资料组织成可以持续维护的工作流。

**有相似需求？欢迎交流业务场景、AI 开发实践与项目合作。**

| 联系方式 | 入口 |
| :--- | :--- |
| 个人主页 | [方楠 · 个人简历](https://resume.fangnan.club/) |
| 电话 / 微信 | 16607557430 |
| 抖音 | 喜文官方企业号 · 抖音号：75604309245 |
| cockpit 介绍 | [cockpit 驾驶舱](https://resume.fangnan.club/cockpit/) |

<p align="center"><img src="assets/douyin-qr.png" width="320" alt="喜文官方企业号抖音码，抖音号75604309245" /></p>
<p align="center"><strong>关注喜文官方企业号，看需求如何一步步变成系统。</strong><br />真实开发过程 · 系统操作演示 · 项目复盘</p>

---

## 门店销售看板解决什么问题？

面向零售，围绕“销售录入、门店汇总与同比环比”提供可操作的演示系统。当前交付状态：**已完成中台功能验收；用于业务演示，未完成生产部署验收**。

## 系统架构

```text
浏览器页面 → JavaScript 校验与业务计算 → localStorage
浏览器页面 ← 列表 / 指标 / CSV ← 当前浏览器中的演示记录
```

cockpit 用于 AI 开发过程，不是此系统运行的必需服务。本系统没有因为使用 AI 开发而自动接入运行时大模型。

## 本地运行

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 http://127.0.0.1:8000/index.html 。无需构建或后端依赖，也可直接打开 index.html；建议固定 HTTP 地址，避免浏览器存储来源变化。

## 代码目录

```text
index.html     页面、样式与业务逻辑
smoke-test.py  独立浏览器功能测试
assets/       README 品牌素材
README.MD      项目说明
LICENSE        MIT 许可证
```

## 操作与业务规则

## 使用


```sh
python3 -m http.server 8515 --bind 127.0.0.1
```


默认展示最近七天销售。筛选日期、门店和品类后，点“新增销售”，输入日期及正数金额保存；汇总、门店状态、品类分布、明细同步更新。明细中的“修改”可编辑记录。新增记录不属于当前筛选时会提示。CSV 导出包含当前筛选全部记录，不限当前页；重置必须再次确认。

同比为去年同日期区间，闰日映射上年2月28日；环比为紧邻之前的等长天数。当前没有记录或比较期金额为零时显示“暂无可比数据”。任一可比增长率不高于 -20% 时门店标红。仅有手工销售记录，不保证完整营业日覆盖，不冒充自动采集。

## 真实功能验证


```sh
python3 smoke-test.py
```



## 验证范围

发布前在独立导出目录验证启动与入口访问；实际结果随发布回执记录。业务验收状态与代码发布状态分开管理。原有测试记录属于历史开发验证，不代表生产环境验收。

## 交流与贡献

使用问题请在本仓库 Issues 提供环境、复现步骤与脱敏截图。欢迎提交改进建议或 Pull Request；业务交流见顶部公开联系方式。如果对你有帮助，欢迎 Star 收藏。

## 项目地址

- GitHub: https://github.com/fn199544123/cockpit-fde-15-store-sales
- 码云: https://gitee.com/xiwenfde/cockpit-fde-15-store-sales

## 许可证

本项目原创代码采用 [MIT](LICENSE)，允许在遵守许可声明的前提下使用、修改与商用。第三方组件适用各自许可证；cockpit 品牌素材用于项目归属展示，不代表商标授权或官方背书。

演示数据均为虚构编号与通用业务信息，不代表真实客户经营数据。

---

<p align="center"><strong>cockpit 驾驶舱 · 喜文FDE案例系列</strong></p>
