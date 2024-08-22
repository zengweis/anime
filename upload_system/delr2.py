import boto3

# 配置 Cloudflare R2 端点和凭证
s3_client = boto3.client('s3',
                         endpoint_url='https://ae7b21228c0af396feb1372330a8b87a.r2.cloudflarestorage.com',
                         aws_access_key_id='4ebfc38641a6ea825bdbdf141d67b2f8',
                         aws_secret_access_key='9a685c3fabb3a75d4894a6ecadf074afb9729d3bb3cba86646de1a28a3f5bea7')

bucket_name = 'anime-web-aliyun'

def list_files_with_subdirectories():
    """列出所有子目录及其文件"""
    try:
        # 列出根目录下的子目录
        response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
        subdirs = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]
        
        all_files = {}
        
        print("\n子目录及其文件:")
        for i, subdir in enumerate(subdirs, 1):
            print(f"\n子目录 {i}: {subdir}")
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=subdir)
            files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'] != subdir]
            
            if files:
                all_files[i] = files
                for j, file in enumerate(files, 1):
                    print(f"  {i}.{j} {file}")
            else:
                print("  该子目录下没有文件。")
        
        return subdirs, all_files

    except Exception as e:
        print(f"列出文件时出错: {e}")
        return [], {}

def delete_file(file_key):
    """删除指定文件"""
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"已删除文件: {file_key}")
    except Exception as e:
        print(f"删除文件时出错: {e}")

def delete_subdir(subdir_key):
    """删除指定子目录及其所有文件"""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=subdir_key)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"已删除文件: {obj['Key']}")
        print(f"已删除子目录及其所有文件: {subdir_key}")
    except Exception as e:
        print(f"删除子目录时出错: {e}")

def main():
    while True:
        subdirs, all_files = list_files_with_subdirectories()
        
        if not subdirs:
            print("没有找到子目录。")
            break
        
        try:
            # 选择删除模式
            mode = input("\n选择删除模式:\n1. 删除特定文件\n2. 删除整个子目录及其所有文件\n请输入模式编号 (1 或 2): ").strip()
            
            if mode == '1':
                # 删除特定文件
                delete_input = input("\n请输入要删除的文件（格式为 '子目录序号/文件序号'，例如 '1/1'），或输入 '0' 取消: ").strip()
                
                if delete_input == '0':
                    print("取消删除。")
                    continue
                
                if '/' in delete_input:
                    try:
                        subdir_num, file_num = map(int, delete_input.split('/'))
                        if 1 <= subdir_num <= len(subdirs) and subdir_num in all_files:
                            if 1 <= file_num <= len(all_files[subdir_num]):
                                file_key = all_files[subdir_num][file_num - 1]
                                confirm = input(f"您确定要删除文件 '{file_key}' 吗？ (y/n): ").strip().lower()
                                if confirm == 'y':
                                    delete_file(file_key)
                                else:
                                    print("取消删除。")
                            else:
                                print("文件编号无效。")
                        else:
                            print("子目录编号无效。")
                    except ValueError:
                        print("输入格式无效。")
                else:
                    print("输入无效。请使用 '子目录序号/文件序号' 格式。")
            
            elif mode == '2':
                # 删除整个子目录及其所有文件
                subdir_input = input("\n请输入要删除的子目录编号，或输入 '0' 取消: ").strip()
                
                if subdir_input == '0':
                    print("取消删除。")
                    continue
                
                try:
                    subdir_num = int(subdir_input)
                    if 1 <= subdir_num <= len(subdirs):
                        subdir_key = subdirs[subdir_num - 1]
                        confirm = input(f"您确定要删除子目录 '{subdir_key}' 及其所有文件吗？ (y/n): ").strip().lower()
                        if confirm == 'y':
                            delete_subdir(subdir_key)
                        else:
                            print("取消删除。")
                    else:
                        print("子目录编号无效。")
                except ValueError:
                    print("输入格式无效。")
            
            else:
                print("输入无效。请输入 '1' 或 '2'。")
        
        except ValueError:
            print("输入无效。请重新输入。")

if __name__ == "__main__":
    main()