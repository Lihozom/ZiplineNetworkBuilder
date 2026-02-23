import cv2
import numpy as np
import os

def template_match_with_chroma_key(image, template_path="resource/Zipline.png", threshold=0.7):
    """
    对图像进行带绿幕的模板匹配
    
    Args:
        image: 输入图像 (numpy array)
        template_path: 模板图像路径，默认为 "resource/Zipline.png"
        threshold: 匹配阈值，默认为0.8
    
    Returns:
        list: 包含匹配结果的列表，每个元素为 (x, y, confidence) 格式
    """
    
    # 检查模板文件是否存在
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    # 读取模板图像
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    
    if template is None:
        raise ValueError(f"无法读取模板图像: {template_path}")
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    # 定义绿色范围
    lower_green = np.array([0, 255, 0])
    upper_green = np.array([0, 255, 0])
    mask = cv2.inRange(template, lower_green, upper_green)
    # 反转掩码，使绿色区域变为0，其他区域为255
    mask = 255 - mask
    template_bgr = template
    cv2.imshow("Template", image)
    cv2.waitKey()

    result = cv2.matchTemplate(image, template_bgr, cv2.TM_CCOEFF_NORMED, mask=mask)
    
    # 找到所有匹配位置，其中置信度大于阈值
    locations = np.where(result >= threshold)
    
    # 组合匹配结果
    matches = []
    for pt in zip(*locations[::-1]):  # 反转坐标以匹配(x, y)格式
        confidence = result[pt[1], pt[0]]
        matches.append((pt[0], pt[1], float(confidence)))
    
    return matches


def find_best_match(image, template_path="resource/Zipline.png", threshold=0.8):
    """
    找到最佳匹配位置
    
    Args:
        image: 输入图像 (numpy array)
        template_path: 模板图像路径，默认为 "resource/Zipline.png"
        threshold: 匹配阈值，默认为0.8
    
    Returns:
        tuple: (x, y, confidence) 或 None（如果没有找到匹配）
    """
    matches = template_match_with_chroma_key(image, template_path, threshold)
    
    if not matches:
        return None
    
    # 返回置信度最高的匹配
    best_match = max(matches, key=lambda x: x[2])
    return best_match


def draw_matches(image, matches, threshold=0.8, template_shape=None, template_path="resource/Zipline.png"):
    """
    在图像上绘制匹配结果
    
    Args:
        image: 输入图像
        matches: 匹配结果列表，每个元素为 (x, y, confidence)
        template_shape: 模板图像的形状 (height, width)，如果不提供则从template_path读取
        template_path: 模板图像路径，用于获取模板尺寸（当template_shape未提供时）
    
    Returns:
        numpy array: 带有标记的图像
    """
    output_image = image.copy()
    
    # 获取模板尺寸
    if template_shape is not None:
        h, w = template_shape
    else:
        # 从文件读取模板图像以获取尺寸
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template is not None:
            h, w = template.shape[:2]
        else:
            # 如果无法读取模板，返回原图
            return output_image
    
    for (x, y, confidence) in matches:
        if confidence < 0.8: continue
        # 绘制矩形框
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        cv2.rectangle(output_image, top_left, bottom_right, (0, 255, 0), 2)
        
        # 标注置信度
        cv2.putText(output_image, f'{confidence:.2f}', 
                   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    return output_image