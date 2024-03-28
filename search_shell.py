import os
import shutil
from tkinter import Tk, filedialog, StringVar
from pathlib import Path


# 在文章中找到关键词，并打印那一句话
def sentence_key(content, keywords):
    # 将文章分割成句子
    sentences = content.split('.')  # 假设句子以句号分隔
    i = 0
    # 在每个句子中查找关键字（不区分大小写）
    for s in sentences:
        if any(keyword.lower() in s.lower() for keyword in keywords):
            i += 1
            print("句子{}: {}".format(i, s.strip()))


# 检索文件夹中文件里某几个关键词出现次数大于3的文件，并打印文件名
def count_keyword_occurrences(src_folder, keywords):
    with open(src_folder, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()  # 将内容转换为小写以进行不区分大小写的匹配
        count = sum(content.count(keyword.lower()) for keyword in keywords)
    return count


def search_files_with_keywords_copy(src_folder, keywords, threshold):
    # 获取文件夹中的所有文件
    files = os.listdir(src_folder)
    count = 0
    # 遍历文件夹中的每个文件
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(src_folder, file)

                # 检查文件中关键词的出现次数
                occurrences = count_keyword_occurrences(file_path, keywords)

                # 如果出现次数大于阈值，打印文件名
                if occurrences >= threshold:
                    print("-" * 100, "\n")
                    print(f"**文件 '{file}' \n**关键词出现次数: {occurrences}")
                    print("\n")
                    count += 1

                    # 以只读模式打开文件，并读取文件内容
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        sentence_key(content, search_keywords)

    print('包含关键词的文章数量:', count)


# 创建文件夹选择 GUI
# def select_folder():
#     folder_path = filedialog.askdirectory()
#     # entry_var.set(folder_path)

# 用户交互输入
root = Tk()
root.withdraw()  # 隐藏主窗口

# 创建文件夹选择 GUI
folder_path = filedialog.askdirectory(title="选择源文件夹路径")
if not folder_path:
    print("用户取消选择文件夹。退出程序。")
    exit()

search_keywords = input("请输入关键词（多个关键词用逗号分隔）: ").split(',')
numbers_mot = int(input("请输入关键词出现次数阈值: "))

# 搜索文件并打印关键词出现的句子
search_files_with_keywords_copy(folder_path, search_keywords, numbers_mot)
