import os

def convert():
    source_dir = 'domain-list-community/data'
    output_dir = 'mihomo_rules'
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    for filename in os.listdir(source_dir):
        input_path = os.path.join(source_dir, filename)
        if os.path.isfile(input_path) and not filename.startswith('.'):
            rules = []
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or 'include:' in line: continue
                    
                    domain = line.split(' @')[0].strip()
                    if domain.startswith('full:'):
                        rules.append(f"  - DOMAIN,{domain[5:]}")
                    else:
                        rules.append(f"  - DOMAIN-SUFFIX,{domain}")

            if rules:
                with open(os.path.join(output_dir, f"{filename}.yaml"), "w") as yf:
                    # 对于编译 MRS，标准的 rule-set 格式如下
                    yf.write("payload:\n")
                    yf.write("\n".join(rules))

if __name__ == "__main__":
    convert()
