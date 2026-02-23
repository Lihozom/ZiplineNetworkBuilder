import sys
from PyQt6.QtWidgets import QApplication

# 从ui模块导入MainWindow
from ui import MainWindow

# 应用程序入口点
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序主循环
    sys.exit(app.exec())