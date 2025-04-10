import os
from PIL import Image

def split_image(input_path, output_path, image_name, prefix, size=256):
    """
    将一张大图分割为多个小图并保存。

    Args:
        input_path (str): 输入图像的路径。
        output_path (str): 输出图像的保存路径。
        image_name (str): 输入图像的文件名。
        prefix (str): 输出图像的前缀（如 't1', 't2', 'gt'）。
        size (int, optional): 小图的大小。默认为256。
    """
    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)

    # 打开图像
    img = Image.open(input_path)
    width, height = img.size

    # 计算切割的步长
    step = size

    # 提取序号
    seq_num = image_name.split('_')[-1].split('.')[0]

    # 切割并保存图像
    for i in range(0, width, step):
        for j in range(0, height, step):
            # 计算切割区域
            left = i
            upper = j
            right = i + size
            lower = j + size

            # 如果超出边界，调整切割区域
            if right > width:
                right = width
                left = width - size
            if lower > height:
                lower = height
                upper = height - size

            # 切割图像
            img_crop = img.crop((left, upper, right, lower))

            # 生成输出文件名
            x = left // step
            y = upper // step
            output_name = f"{prefix}_{x}_{y}_{image_name}"
            output_file = os.path.join(output_path, output_name)

            # 保存切割后的图像
            img_crop.save(output_file)
            print(f"Saved: {output_file}")

def process_dataset(input_a_path, input_b_path, input_label_path, output_path):
    """
    处理整个数据集，将每张图像分割为多个小图并保存。

    Args:
        input_a_path (str): 变化前图像的路径。
        input_b_path (str): 变化后图像的路径。
        input_label_path (str): 标签图像的路径。
        output_path (str): 输出图像的保存路径。
    """
    # 获取所有图像文件名
    image_files = [f for f in os.listdir(input_a_path) if f.endswith('.png')]

    for image_file in image_files:
        # 处理变化前的图像
        input_a_file = os.path.join(input_a_path, image_file)
        split_image(input_a_file, output_path, image_file, 't1')

        # 处理变化后的图像
        input_b_file = os.path.join(input_b_path, image_file)
        split_image(input_b_file, output_path, image_file, 't2')

        # 处理标签图像
        input_label_file = os.path.join(input_label_path, image_file)
        split_image(input_label_file, output_path, image_file, 'gt')

if __name__ == "__main__":
    # 输入路径
    input_a_path = r"E:\DataSet\LEVIR\train\A"
    input_b_path = r"E:\DataSet\LEVIR\train\B"
    input_label_path = r"E:\DataSet\LEVIR\train\label"

    # 输出路径
    output_path = r"E:\DataSet\LEVIR\train\train_dataset"

    # 处理数据集
    process_dataset(input_a_path, input_b_path, input_label_path, output_path)