"""插件契约测试 — manifest / 可用性 / 工具前缀 / Tab 与设置页工厂。"""
import pytest

pytest.importorskip("PySide6")

from core.agent.tools import ToolRegistry
from core.plugin_api import PluginToolRegistry, api_compatible
from qa_tool_vision.plugin import VisionPlugin


def test_manifest_contract():
    manifest = VisionPlugin.manifest
    assert manifest.id == "vision"
    assert api_compatible(manifest.api_version)
    assert manifest.supports("tab")
    assert manifest.supports("agent_tools")
    assert manifest.supports("settings")
    assert manifest.requires.get("qa_tool")
    assert {d.module for d in manifest.optional_deps} >= {"cv2", "mediapipe"}


def test_tools_registered_with_vision_prefix():
    registry = ToolRegistry()
    VisionPlugin().register_agent_tools(
        PluginToolRegistry(registry, "vision"), None)
    assert {"vision_status", "vision_analyze_video",
            "vision_time_study", "vision_work_sampling"} <= set(registry.names())


def test_tab_factory_returns_widget(_qt_application):
    ok, reason = VisionPlugin().is_available()
    if not ok:
        pytest.skip(reason)
    tab = VisionPlugin().create_tab(None, None)
    assert tab is not None
    tab._stop_workers()
    tab.close()
    tab.deleteLater()


def test_settings_page_factory(_qt_application):
    page = VisionPlugin().create_settings_page(None, None)
    assert page is not None
    page.deleteLater()
