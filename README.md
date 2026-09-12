# QA-Tool Vision Expansion

> 仓库: https://github.com/chrisliuu345/QA-Tool-Vision-expansion

QA-Tool 的独立视觉插件项目：摄像头/视频 → 动作识别（工作·空闲·走动·搬运·离岗）
→ 作业周期 → 标准工时 / 工作抽样。

主应用 **QA-Tool** 不包含任何视觉代码，只提供插件接口 v2；
本插件通过 pip entry point `qa_tool.plugins` 注册，贡献：

- **Tab**：侧栏「插件」→「视频时间研究」（视频源、实时预览、占比/周期、发送工时研究、JSON 导出）
- **Agent 工具**：`vision_status` / `vision_analyze_video` / `vision_time_study` / `vision_work_sampling`
- **设置页**：后端/模型依赖状态

## 安装

前置：QA-Tool ≥ 3.8（含插件接口 v2）。

```bash
# 在 QA-Tool 所在虚拟环境中安装（开发模式）
pip install -e "/path/to/QA-Tool-Vision-expansion[vision]"
```

或仅安装依赖、手动放置：

```bash
pip install -r requirements.txt
```

姿态模型（`pose_landmarker_lite.task`，约 5.6MB）不随包分发：
插件 Tab 内提供「下载姿态模型」按钮（SHA256 校验）；离线环境可用
`QA_TOOL_POSE_MODEL=/path/to/pose_landmarker_lite.task` 指定。
模型缺失时自动降级为 OpenCV 运动特征（MOG2 + 帧差 + 质心速度）。

## 验证

```bash
# 合成片段自检（无需摄像头/素材）
qa-tool-vision-benchmark --demo --min-accuracy 0.85

# 现场素材与人工标注对比（标签 CSV: start_ms,end_ms,state）
qa-tool-vision-benchmark --video clip.mp4 --labels labels.csv --min-accuracy 0.85
```

## 开发与测试

插件依赖主应用提供的接口与引擎（`core.plugin_api`、`core.agent.tools`、
`ui.tabs.base_tab`、`analysis.ie.time_study` / `work_sampling`）。
开发时把主应用目录加入 `PYTHONPATH`：

```bash
PYTHONPATH=/path/to/QA-Tool:/path/to/QA-Tool-Vision-expansion/src \
  python -m pytest tests -q
```

## 插件接口约定

- manifest：`id=vision`、`api_version=2.0`、`requires.qa_tool>=3.8`、能力 `tab/agent_tools/settings`
- 工具名由主应用自动加插件前缀：`vision_*`（注册时写 `status` 等短名即可）
- 未安装 OpenCV 时插件标记为不可用，主应用只显示安装指引，不崩溃

## 目录

```
src/qa_tool_vision/
  plugin.py      插件入口（manifest + 生命周期）
  tab.py         视频时间研究 Tab
  tools.py       Agent 工具注册
  camera.py      视频源（文件/USB/RTSP/MJPEG/合成）
  processor.py   帧处理（MOG2 ∪ 帧差 + 质心/速度）
  pose.py        MediaPipe Tasks + OpenCV 降级
  action.py      动作状态机（迟滞）
  session.py     会话编排（周期/占比/输出）
  model_store.py 模型下载 + SHA256
  benchmark.py   准确率基准 CLI
tests/
```
