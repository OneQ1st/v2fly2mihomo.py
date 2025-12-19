import os
import shutil

def convert():
    # 1. 确定路径
    source_dir = 'domain-list-community/data'
    output_dir = 'mihomo_rules'
    
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"错误: 找不到源目录 {source_dir}。请检查 Git Clone 步骤是否成功。")
        exit(1) # 返回错误代码 1 供 GitHub Action 捕获

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # 2. 开始转换
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    print(f"找到 {len(files)} 个原始文件，准备转换...")

    for filename in files:
        if filename.startswith('.'): continue
        
        input_path = os.path.join(source_dir, filename)
        rules = []
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or 'include:' in line:
                    continue
                
                # 处理 v2fly 格式
                domain = line.split(' @')[0].strip()
                if domain.startswith('full:'):
                    rules.append(f"  - 'DOMAIN,{domain[5:]}'")
                else:
                    rules.append(f"  - 'DOMAIN-SUFFIX,{domain}'")

        if rules:
            output_file = os.path.join(output_dir, f"{filename}.yaml")
            with open(output_file, "w", encoding='utf-8') as yf:
                yf.write("payload:\n")
                yf.write("\n".join(rules))
                yf.write("\n")

    print("转换完成！")

if __name__ == "__main__":
    convert()
