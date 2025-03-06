import csv
import json

def process_dataset(input_path):
    result = []
    system_prompt = "你是一个没有礼貌的人渣，请用人渣的语气回复我"
    
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=["prompt", "chosen", "rejected"])
        next(reader)  # 跳过标题行
        
        for i, row in enumerate(reader, 1):
            try:
                # 提取用户问题
                user_part = row["prompt"].split("<|im_start|>user")[1]
                user_query = user_part.split("<|im_end|>")[0].strip()
                
                # 处理chosen响应
                chosen_content = row["chosen"].strip('"')
                if "," in chosen_content:
                    chosen_response = chosen_content.split(",", 1)[1].strip()
                else:
                    chosen_response = chosen_content
                
                result.append({
                    "system": system_prompt,
                    "prompt": user_query,
                    "response": chosen_response
                })
            except Exception as e:
                print(f"处理第 {i} 行时出错: {str(e)}")
                print(f"问题数据: {row}")
                continue
    
    return result

def save_to_jsonl(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            # 将每个字典包装成列表
            json_line = json.dumps([item], ensure_ascii=False)
            f.write(json_line + '\n')

if __name__ == "__main__":
    # 处理数据
    processed_data = process_dataset("train.csv")
    print(f"成功处理 {len(processed_data)} 条数据")
    
    # 保存为特殊格式的JSONL
    output_file = "output.jsonl"
    save_to_jsonl(processed_data, output_file)
    print(f"数据已保存至：{output_file}")
    
    # 打印首条示例
    print("\n首条数据示例：")
    print(json.dumps([processed_data[0]], ensure_ascii=False, indent=2))
