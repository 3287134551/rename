import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, Qt
from Ui_untitled import Ui_Form


class UI(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # 加载ui文件
        self.setupUi(self)
        
        # 选择目录的lineEdit
        self.lineEdit.textChanged.connect(self.loadDirectoryImg)
        
        # 保存目录的lineEdit_2
        self.lineEdit_2.textChanged.connect(self.saveDirectory)
        self.save_directory = ""  # 保存目录路径
        
        # 初始化显示空白图片
        self.pixmap = QPixmap()
        self.label_3.setPixmap(self.pixmap)
        
        # 滑条控制图片大小 
        self.horizontalSlider.valueChanged.connect(self.changeImageSize)
        
        # 记录滑条的值
        self.slider_value = 0
        
        # lineEdit_3
        self.lineEdit_3.returnPressed.connect(self.saveCurrentImage)
        self.lineEdit.textChanged.connect(self.loadDirectoryImg)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(2000)
        
        # 初始化数量
        self.lcd_count = 0
        
        # 更新lcdNumber的值
        self.lcdNumber.display(self.lcd_count)

    def saveDirectory(self):
        self.save_directory = self.lineEdit_2.text()

    def loadDirectoryImg(self):
        directory = self.lineEdit.text()
        if os.path.isdir(directory):
            file_names = [file_name for file_name in os.listdir(directory) if
                          file_name.endswith(".png") or file_name.endswith(".jpg")]
            if file_names:
                self.file_names = file_names
                self.index = 0
                self.loadNextImage()
                self.lcd_count = len(file_names)  # 更新总数量
                self.lcdNumber.display(self.lcd_count)  # 显示总数量
                self.lcdNumber_2.display(self.lcd_count)  # 显示剩余数量

    def loadNextImage(self):
        file_names = self.file_names
        if file_names:
            file_name = file_names[self.index]
            image_path = os.path.join(self.lineEdit.text(), file_name)
            self.pixmap = QPixmap(image_path)
            
            # 根据滑条的值调整图片大小
            scaled_pixmap = self.pixmap.scaled(self.slider_value, self.slider_value, Qt.AspectRatioMode.KeepAspectRatio)
            self.label_3.setPixmap(scaled_pixmap)
            
            self.lineEdit_3.setText(file_name)  # 设置完整文件名
            self.lineEdit_3.setCursorPosition(self.lineEdit_3.text().index('_'))

            self.index = (self.index + 1) % len(file_names)

    def saveCurrentImage(self):
        file_names = self.file_names
        if file_names:
            file_name = file_names[self.index - 1]
            new_file_name = self.lineEdit_3.text() # 保持后缀名不变
            
            # 获取原始图片路径和新图片路径
            source_image_path = os.path.join(self.lineEdit.text(), file_name)
            target_image_path = os.path.join(self.save_directory, new_file_name)
            
            # 更改文件名
            os.rename(source_image_path, target_image_path)
            
            # 更新剩余数量并显示
            self.lcd_count -= 1
            self.lcdNumber_2.display(self.lcd_count)
            
            self.loadNextImage()

    def changeImageSize(self, value):
        # 更新滑条值
        self.slider_value = value
        
        # 根据滑条的值调整当前显示图片的大小
        scaled_pixmap = self.pixmap.scaled(self.slider_value, self.slider_value, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_3.setPixmap(scaled_pixmap)


app = QApplication([])
window = UI()
window.show()
app.exec()
