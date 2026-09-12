"""QA-Tool 视觉插件入口 — 基于主应用插件接口 v2。

主应用不包含任何视觉代码；本插件通过 entry point `qa_tool.plugins` 注册，
贡献 Tab（视频时间研究）、Agent 工具（vision_*）与设置页。
"""
from __future__ import annotations

from core.plugin_api import Dependency, IQAToolPlugin, PluginManifest


class VisionPlugin(IQAToolPlugin):
    manifest = PluginManifest(
        id="vision",
        name="视频时间研究",
        version="0.1.0",
        api_version="2.0",
        entry="qa_tool_vision.plugin:VisionPlugin",
        description="摄像头/视频 → 动作识别（工作·空闲·走动·搬运·离岗）"
                    "→ 作业周期 → 标准工时",
        category="ie",
        icon="🎥",
        requires={"qa_tool": ">=3.8"},
        optional_deps=(
            Dependency("cv2", "pip install \"qa-tool-vision-expansion[vision]\""),
            Dependency("mediapipe",
                       "pip install mediapipe>=1.0（缺失时自动降级 OpenCV 运动特征）"),
        ),
        capabilities=("tab", "agent_tools", "settings"),
    )

    def is_available(self) -> tuple[bool, str]:
        from qa_tool_vision import INSTALL_HINT, cv2_available

        if not cv2_available():
            return False, f"未安装 OpenCV，安装: {INSTALL_HINT}"
        return True, ""

    def create_tab(self, host, parent=None):
        from qa_tool_vision.tab import VisionTab

        return VisionTab(parent)

    def register_agent_tools(self, registry, context=None):
        from qa_tool_vision.tools import register_tools

        register_tools(registry, context)

    def create_settings_page(self, host, parent=None):
        from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

        from qa_tool_vision import INSTALL_HINT, backend_info

        page = QWidget(parent)
        layout = QVBoxLayout(page)
        info = backend_info()
        backend = {"mediapipe": "MediaPipe 骨架",
                   "opencv-motion": "OpenCV 运动特征（降级）",
                   "unavailable": "不可用"}.get(info["backend"], info["backend"])
        text = (f"后端: {backend}\n"
                f"OpenCV: {'✓' if info['cv2'] else '✗'}　"
                f"MediaPipe: {'✓' if info['mediapipe'] else '✗'}\n"
                f"姿态模型: {'已就绪' if info['pose_model'] else '未下载（运动特征降级）'}\n"
                f"模型路径: {info['pose_model_path'] or '—'}")
        if not info["available"]:
            text += f"\n安装依赖: {INSTALL_HINT}"
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch()
        return page
