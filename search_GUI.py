import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from pathlib import Path

# 在文章中找到关键词，并展示那一句话
def sentence_key(content, keywords):
    sentences = content.split('.')  # 假设句子以句号分隔
    for i, s in enumerate(sentences):
        for keyword in keywords:
            if keyword.lower() in s.lower():
                print(f"句子{i+1}: {s.strip()}")

# 检索文件夹中文件里某几个关键词出现次数大于3的文件，并打印文件名
def count_keyword_occurrences(file_path, keywords):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()  # 将内容转换为小写以进行不区分大小写的匹配
        count = sum(content.count(keyword) for keyword in keywords)
    return count

def search_files_with_keywords(src_folder, keywords, threshold):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(src_folder, file)
                occurrences = count_keyword_occurrences(file_path, keywords)
                if occurrences >= threshold:
                    messagebox.showinfo("关键词出现", f"文件 '{file}'\n关键词出现次数: {occurrences}")
                    sentence_key(open(file_path, 'r', encoding='utf-8').read(), keywords)

# 创建图形化界面
root = tk.Tk()
root.title("文本关键词搜索工具")

# 创建输入框和标签
keywords_label = tk.Label(root, text="请输入关键词（多个关键词用逗号分隔）:")
keywords_label.pack()
keywords_entry = tk.Entry(root)
keywords_entry.pack()

threshold_label = tk.Label(root, text="请输入关键词出现次数阈值:")
threshold_label.pack()
threshold_entry = tk.Entry(root)
threshold_entry.pack()

# 创建按钮
search_button = tk.Button(root, text="开始搜索", command=lambda: search_files_with_keywords(
    filedialog.askdirectory(title="选择源文件夹路径"),
    keywords_entry.get().split(','),
    int(threshold_entry.get())
))
search_button.pack()

# 运行图形化界面
root.mainloop()