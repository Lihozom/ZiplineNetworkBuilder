import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from snapshot import capture_window_mss
from template_matching import template_match_with_chroma_key, draw_matches

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口尺寸
        self.WINDOW_WIDTH = 1980
        self.WINDOW_HEIGHT = 1080
        
        # 设置窗口属性
        self.setWindowTitle("Zipline Network Builder")
        self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
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
        snap_button = QPushButton("截图并标记滑索")
        snap_button.clicked.connect(lambda: self.capture_and_display())
        load_button = QPushButton("加载项目")
        save_button = QPushButton("保存项目")
        
        layout.addWidget(snap_button)
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

        # 创建一个标签用于显示截图
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; font-size: 14px; color: gray;")
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setText("等待截图...")
        layout.addWidget(self.image_label)

        return main_content

    
    def capture_and_display(self):
        """截图并进行滑索标记后显示在主工作区域"""
        try:
            # 调用截图函数
            image = capture_window_mss("Endfield")
            
            if image is not None:
                # 将OpenCV图像(BGR)转换为RGB格式
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # 调整图像到720p分辨率（1280x720）
                target_width, target_height = 1280, 720
                resized_rgb_image = cv2.resize(rgb_image, (target_width, target_height), interpolation=cv2.INTER_AREA)
                
                # 进行模板匹配
                matches = template_match_with_chroma_key(resized_rgb_image, 'resource/Zipline.png', 0.4)
                
                if matches is not None:
                    # 读取模板获取尺寸
                    template = cv2.imread('resource/Zipline.png', cv2.IMREAD_UNCHANGED)
                    if template is not None:
                        h, w = template.shape[:2]
                        result_img = draw_matches(resized_rgb_image, matches, (h, w))
                    else:
                        # 如果无法读取模板，使用一个默认大小
                        result_img = draw_matches(resized_rgb_image, matches, (50, 50))  # 假设模板大小
                    
                    # 转换为QImage并显示
                    result_rgb = result_img  # 已经是RGB格式
                    height, width, channel = result_rgb.shape
                    bytes_per_line = 3 * width
                    q_img = QImage(result_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_img)
                else:
                    # 如果没有匹配到，仍然显示调整大小后的原图
                    height, width, channel = resized_rgb_image.shape
                    bytes_per_line = 3 * width
                    q_img = QImage(resized_rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_img)
                
                # 显示处理后的图像
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText("截图失败，请确保窗口存在")
        except Exception as e:
            print(f"截图过程中出现错误: {e}")
            self.image_label.setText(f"截图错误: {str(e)}")
    
    def mark_ziplines(self):
        """对当前显示的截图进行滑索模板匹配并绘制结果"""
        threshold = 0.4
        try:
            # 获取当前显示的图像
            pixmap = self.image_label.pixmap()
            if pixmap is None:
                self.image_label.setText("请先截图再标记滑索")
                return
            
            # 将QPixmap转换为OpenCV图像格式
            qimg = pixmap.toImage()
            qimg = qimg.convertToFormat(QImage.Format.Format_RGB888)
            
            # 转换为numpy数组
            ptr = qimg.bits()
            ptr.setsize(qimg.sizeInBytes())
            img_array = np.array(ptr).reshape(qimg.height(), qimg.width(), 3)
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 进行模板匹配
            matches = template_match_with_chroma_key(img_array, 'resource/Zipline.png', threshold)
            
            if matches:
                # 绘制匹配结果
                # 需要知道模板的尺寸，这里我们读取模板获取尺寸
                template = cv2.imread('resource/Zipline.png', cv2.IMREAD_UNCHANGED)
                if template is not None:
                    h, w = template.shape[:2]
                    result_img = draw_matches(img_array, matches, threshold, (h, w, 3))
                else:
                    # 如果无法读取模板，使用一个默认大小
                    result_img = draw_matches(img_array, matches, threshold, (50, 50, 3))  # 假设模板大小
                
                # 转换回QPixmap并显示
                result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                height, width, channel = result_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(result_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                result_pixmap = QPixmap.fromImage(q_img)
                
                self.image_label.setPixmap(result_pixmap)
            else:
                self.image_label.setPixmap(result_pixmap)
                
        except Exception as e:
            print(f"标记滑索过程中出现错误: {e}")
            self.image_label.setText(f"标记滑索错误: {str(e)}")

    def keyPressEvent(self, event):
        # 添加ESC键退出功能
        if event.key() == Qt.Key.Key_Escape:
            self.close()