#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer
from main_window import MainWindow
from data_manager import PromptManager
from floating_ball import FloatingBall


def create_tray_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    painter.setBrush(QColor(10, 132, 255))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(8, 8, 48, 48)
    
    painter.setPen(QColor(255, 255, 255))
    painter.setFont(painter.font())
    font = painter.font()
    font.setPixelSize(36)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "💡")
    
    painter.end()
    
    return QIcon(pixmap)


class PromptManagerApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setQuitOnLastWindowClosed(False)
        
        # 初始化数据管理器
        self.data_manager = PromptManager()
        
        # 获取当前风格
        current_style = self.data_manager.config.get("ui_style", "premium")
        
        # 创建浮动球，传递 data_manager 用于保存/加载位置
        self.floating_ball = FloatingBall(self.data_manager, style=current_style)
        self.floating_ball.clicked.connect(self.toggle_window)
        
        # 创建主窗口，传入浮动球引用
        self.main_window = MainWindow(self.data_manager, self.floating_ball)
        
        self.setup_tray()
        
        # 初始化时显示浮动球，隐藏主窗口
        self.main_window.hide()
        print("🎈 准备显示浮动球...")
        self.floating_ball.show()
        self.floating_ball.raise_()
        self.floating_ball.activateWindow()
        
        # 使用QTimer延迟检查，确保窗口系统完成渲染
        QTimer.singleShot(500, self.check_floating_ball)
        
        print(f"✅ 浮动球已调用显示: isVisible={self.floating_ball.isVisible()}")
        print(f"📍 浮动球位置: {self.floating_ball.pos()}")
        print(f"📏 浮动球大小: {self.floating_ball.size()}")
        print("💡 提示: 浮动球应该在屏幕中心偏右的位置")
        print("   如果看不到，请尝试:")
        print("   1. 按 Ctrl+Shift+P 打开主窗口")
        print("   2. 检查 macOS 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能")
        
        # 安装事件过滤器，监听全局点击事件
        self.installEventFilter(self)
    
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(create_tray_icon(), self)
        
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3A3A3C;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3A3A3C;
            }
        """)
        
        show_action = tray_menu.addAction("显示/隐藏")
        show_action.triggered.connect(self.toggle_window)
        
        stats_action = tray_menu.addAction("使用统计")
        stats_action.triggered.connect(self.show_stats)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
        
        self.tray_icon.setToolTip("Prompt Manager\n点击浮动球或按 Ctrl+Shift+P 显示")
    
    def toggle_window(self):
        if self.main_window.isVisible():
            self.main_window.hide_to_ball()
        else:
            self.main_window.show_from_ball()
    
    def quick_add(self):
        """快速添加（从剪贴板）"""
        # 确保窗口可见
        if not self.main_window.isVisible():
            self.main_window.show_from_ball()
        
        # 触发快速添加
        self.main_window.quick_add_from_clipboard()
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_window()
    
    def show_stats(self):
        from stats_window import StatsWindow
        stats_window = StatsWindow(None, self.data_manager)
        stats_window.exec()
    
    def quit_app(self):
        self.main_window.save_window_state()
        self.quit()
    
    def eventFilter(self, obj, event):
        """事件过滤器 - 监听全局点击，实现点击外部收起"""
        if event.type() == event.Type.MouseButtonPress:
            # 仅在主窗口可见且展开保护期结束时检查
            if self.main_window.isVisible() and not self.main_window.just_expanded:
                # 获取点击位置
                if hasattr(event, 'globalPosition'):
                    click_pos = event.globalPosition().toPoint()
                elif hasattr(event, 'globalPos'):
                    click_pos = event.globalPos()
                else:
                    return super().eventFilter(obj, event)
                
                # 检查是否点击在主窗口内
                main_rect = self.main_window.geometry()
                if not main_rect.contains(click_pos):
                    # 检查是否点击在浮动球内（如果浮动球可见且始终显示）
                    if self.floating_ball.isVisible():
                        ball_rect = self.floating_ball.geometry()
                        if ball_rect.contains(click_pos):
                            # 点击了浮动球，不处理（让浮动球自己处理）
                            return super().eventFilter(obj, event)
                    
                    # 如果有预览tooltip，也检查是否在tooltip内
                    if self.main_window.current_tooltip and self.main_window.current_tooltip.isVisible():
                        tooltip_rect = self.main_window.current_tooltip.geometry()
                        if tooltip_rect.contains(click_pos):
                            return super().eventFilter(obj, event)
                    
                    # 点击在外部，立即收起
                    self.main_window.hide_to_ball()
        
        return super().eventFilter(obj, event)
    
    def check_floating_ball(self):
        """检查浮动球状态"""
        print("\n🔍 延迟检查浮动球状态:")
        print(f"   可见性: {self.floating_ball.isVisible()}")
        print(f"   位置: {self.floating_ball.pos()}")
        print(f"   大小: {self.floating_ball.size()}")
        print(f"   窗口标志: {self.floating_ball.windowFlags()}")
        if self.floating_ball.isVisible():
            print("✅ 浮动球应该已经显示在屏幕上了！")
        else:
            print("❌ 浮动球未显示，尝试重新显示...")
            self.floating_ball.show()
            self.floating_ball.raise_()


def main():
    app = PromptManagerApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
