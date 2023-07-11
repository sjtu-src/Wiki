# -*- coding: utf-8 -*-


import os
import fnmatch

# 指定路径
dir_path = "./docs/"

# 排除的目录
exclude_dirs = {"*/uploads*"}

# 如果不存在则创建路径
os.makedirs(dir_path, exist_ok=True)

with open(f"{dir_path}index.md", 'w') as md_file:
    md_file.write("---\nhtml:\n    toc: true\n    toc_float: true\n---\n\n")

# 遍历文件和子文件夹
for root, dirs, files in os.walk(dir_path):
    # 排除目录
    if any(fnmatch.fnmatch(root, pattern) for pattern in exclude_dirs):
        continue
    print(root)
    # 计算缩进级别
    indent_count = root.count(os.sep)-1

    # 生成缩进字符串
    indent_adoc = "    " * indent_count

    # 获取目录名
    dir_name = os.path.basename(root)
    if dir_name=="":
        dir_name="Home"
    file_link=os.path.join("Home",dir_name)
    with open(f"{dir_path}index.md", 'a') as md_file:
        md_file.write(f"## [{dir_name}]({file_link}.md)\n")
    with open(f"{dir_path}Home/{dir_name}.md", 'w') as md_file:
                md_file.write(f"---\nlayout: default \ntitle: {dir_name}\n---\n")

    # 遍历目录下的文件
    for file in files:
        if file.endswith(".md"):
            print(file)
            if file=="index.md":
                continue
            # 计算缩进级别
            file_indent_count = indent_count + 1
            # 生成缩进字符串
            file_indent_adoc = "    " * file_indent_count
            file_indent_md="#"*(file_indent_count+1)
            # 获取文件名，不包含扩展名
            print(file)
            no_extension = os.path.splitext(file)[0]
            print(no_extension)
            # 生成文件链接
            file_link = os.path.join(root, file)
            print(file_link)


            with open(f"{dir_path}Home/{dir_name}.md", 'a') as md_file:
                md_file.write(f"{file_indent_md} [{no_extension}](.{file_link})\n")

import datetime
with open(f"{dir_path}index.md", 'a') as md_file:
    md_file.write("\n\n---\n\n")
    md_file.write("created on:{curtime}\n".format(curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    md_file.write("SJTU-SRC-All Rights Reserved\n")

print("文件已创建并写入到", dir_path)
