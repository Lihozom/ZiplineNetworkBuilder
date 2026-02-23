import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from snapshot import capture_window_mss

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口尺寸
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        
        # 设置窗口属性
        self.setWindowTitle("Zipline Network Builder - 1280x720 Window")
        self.setGeometry(100, 100, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建水平分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建左边栏
        self.sidebar = self.create_sidebar()
        splitter.addWidget(self.sidebar)
        
        # 创建主内容区域
        self.main_content = self.create_main_content()
        splitter.addWidget(self.main_content)
        
        # 设置分割器比例
        splitter.setSizes([250, self.WINDOW_WIDTH - 250])  # 左边栏宽度为250像素
        
        # 将分割器添加到中央部件
        layout = QHBoxLayout(central_widget)
        layout.addWidget(splitter)

    def create_sidebar(self):
        # 创建左边栏容器
        sidebar = QWidget()
        sidebar.setFixedWidth(250)  # 固定左边栏宽度
        sidebar.setStyleSheet("background-color: #f0f0f0;")  # 设置背景色

        # 左边栏布局
        layout = QVBoxLayout(sidebar)

        # 添加标题
        title_label = QLabel("Zipline Network Builder")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px; background-color: #d0d0d0;")
        layout.addWidget(title_label)

        # 添加工具树
        map_tree = QTreeWidget()
        map_tree.setHeaderHidden(True)  # 隐藏表头
        
        # 创建四号谷地项目
        valley_IV = QTreeWidgetItem(map_tree)
        valley_IV.setText(0, "四号谷地")
        
        # 创建四号谷地的子项目
        the_hub = QTreeWidgetItem(valley_IV)
        the_hub.setText(0, "枢纽区")
        
        aburrey_quarry = QTreeWidgetItem(valley_IV)
        aburrey_quarry.setText(0, "采石场")
        
        valley_pass = QTreeWidgetItem(valley_IV)
        valley_pass.setText(0, "谷地通道")
        
        power_plateau = QTreeWidgetItem(valley_IV)
        power_plateau.setText(0, "供能高地")

        origin_lodespring = QTreeWidgetItem(valley_IV)
        origin_lodespring.setText(0, "矿脉源区")

        originium_science_park = QTreeWidgetItem(valley_IV)
        originium_science_park.setText(0, "源石研究园")

        wuling=QTreeWidgetItem(map_tree)
        wuling.setText(0, "武陵")

        jingyu_valley=QTreeWidgetItem(wuling)
        jingyu_valley.setText(0,"景玉谷")

        wuling_city=QTreeWidgetItem(wuling)
        wuling_city.setText(0,"武陵城")

        layout.addWidget(map_tree)
        # 添加操作按钮
        add_button = QPushButton("截图")
        add_button.clicked.connect(lambda: self.capture_and_display())
        load_button = QPushButton("加载项目")
        save_button = QPushButton("保存项目")
        
        layout.addWidget(add_button)
        layout.addWidget(load_button)
        layout.addWidget(save_button)
        


        # 添加弹簧以填充剩余空间
        layout.addStretch()
        
        return sidebar
    
    def create_main_content(self):
        # 创建主内容区域
        main_content = QWidget()
        main_content.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(main_content)

        # 添加说明标签
        label = QLabel("主工作区域 - 在这里显示网络图")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # 创建一个标签用于显示截图
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; font-size: 14px; color: gray;")
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setText("等待截图...")
        layout.addWidget(self.image_label)

        return main_content

    
    def capture_and_display(self):
        """截图并显示在主工作区域"""
        try:
            # 调用截图函数
            image = capture_window_mss("Endfield")
            
            if image is not None:
                # 将OpenCV图像(BGR)转换为RGB格式
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = rgb_image.shape
                bytes_per_line = 3 * width
                q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                
                # 缩放图片以适应显示区域，同时保持宽高比
                scaled_pixmap = pixmap.scaled(
                    self.image_label.width(), 
                    self.image_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("截图失败，请确保窗口存在")
        except Exception as e:
            print(f"截图过程中出现错误: {e}")
            self.image_label.setText(f"截图错误: {str(e)}")
    
    def keyPressEvent(self, event):
        # 添加ESC键退出功能
        if event.key() == Qt.Key.Key_Escape:
            self.close()