import os


# 在文章中找到关键词，并打印那一句话
def sentence_key(content, keywords):
    # 将文章分割成句子
    sentences = content.split('.')  # 假设句子以句号分隔

    # 在每个句子中查找关键字
    for s in sentences:
        if any(keyword in s for keyword in keywords):
            print("句子: {}".format(s.strip()))


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
                    print(f"文件 '{file}' 中关键词出现次数: {occurrences}")
                    count += 1

                    # 以只读模式打开文件，并读取文件内容
                    with open(file_path, 'r') as c:
                        content = c.read()
                        sentence_key(content, search_keywords)

                    # dest_file_path = os.path.join(dest_folder, file)
                    # shutil.copy2(file_path, dest_file_path)
                    # print(f"复制文件: {file} 到 {dest_file_path}")
    print('包含关键词的文章数量:', count)


search_keywords = ['two wings','belt']
numbers_mot = 2
source_folder = 'D:\\陈林\\中国日报\\data'
search_files_with_keywords_copy(source_folder, search_keywords, numbers_mot)
