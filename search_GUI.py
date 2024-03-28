import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


# 在文章中找到关键词，并返回包含关键词的句子
def find_sentences_with_keywords(content, keywords):
    sentences = content.split('.')  # 假设句子以句号分隔
    relevant_sentences = []
    for s in sentences:
        if any(keyword.lower() in s.lower() for keyword in keywords):
            relevant_sentences.append(s.strip())
    return relevant_sentences


# 检索文件中某几个关键词出现次数大于阈值的文件，并返回符合条件的文件列表
def search_files_with_keywords(src_folder, keywords, threshold):
    relevant_files = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    count = sum(content.count(keyword.lower()) for keyword in keywords)
                    if count >= threshold:
                        relevant_files.append((file, count, file_path))
    return relevant_files


# 显示文件内容和关键词句子
def show_file_content(file_path, keywords):
    window = tk.Toplevel()
    window.title("文件内容")
    text_area = ScrolledText(window, width=80, height=30, wrap=tk.WORD, font=("Arial", 12))
    text_area.pack(expand=True, fill="both")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        sentences = find_sentences_with_keywords(content, keywords)
        for sentence in sentences:
            start_index = content.find(sentence)
            end_index = start_index + len(sentence)
            text_area.insert(tk.END, content[:start_index])
            text_area.insert(tk.END, sentence, 'red')
            content = content[end_index:]
        text_area.insert(tk.END, content)

    # 设置标签以显示红色文本
    text_area.tag_configure('red', foreground='red')


# 创建主界面
def create_gui():
    root = tk.Tk()
    root.title("关键词搜索")

    def browse_folder():
        folder_path.set(filedialog.askdirectory(title="选择源文件夹路径"))

    def start_search():
        keywords = entry_keywords.get().split(',')
        threshold = int(entry_threshold.get())
        folder = folder_path.get()
        relevant_files = search_files_with_keywords(folder, keywords, threshold)
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        for file, count, file_path in relevant_files:
            result_text.insert(tk.END, f"{file} (关键词出现次数: {count})\n", 'file_link')
            result_text.tag_bind('file_link', '<Button-1>',
                                 lambda event, path=file_path: show_file_content(path, keywords))
        result_text.config(state=tk.DISABLED)

    folder_path = tk.StringVar()
    tk.Label(root, text="选择源文件夹路径:").grid(row=0, column=0, sticky="w")
    tk.Entry(root, textvariable=folder_path, width=50).grid(row=0, column=1)
    tk.Button(root, text="浏览", command=browse_folder).grid(row=0, column=2)

    tk.Label(root, text="请输入关键词（多个关键词用逗号分隔）:").grid(row=1, column=0, sticky="w")
    entry_keywords = tk.Entry(root, width=50)
    entry_keywords.grid(row=1, column=1)

    tk.Label(root, text="请输入关键词出现次数阈值:").grid(row=2, column=0, sticky="w")
    entry_threshold = tk.Entry(root, width=10)
    entry_threshold.grid(row=2, column=1)

    tk.Button(root, text="开始搜索", command=start_search).grid(row=3, column=0, columnspan=3, pady=10)

    tk.Label(root, text="搜索结果:").grid(row=4, column=0, sticky="w")
    result_text = tk.Text(root, wrap=tk.WORD, width=70, height=20)
    result_text.grid(row=5, column=0, columnspan=3, padx=10)
    result_text.tag_config('file_link', foreground='blue', underline=1)
    result_text.config(state=tk.DISABLED)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
