import random
import json
import os

# 定义保存配置的JSON文件名
config_file = 'configs.json'


def save_configs(configs):
    """保存多个配置到JSON文件"""
    try:
        with open(config_file, 'w') as f:
            json.dump(configs, f)
    except IOError as e:
        print(f"无法写入配置文件: {e}")


def load_configs():
    """从JSON文件加载多个配置"""
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"配置文件损坏: {e}")
    return {}


def get_positive_int(prompt):
    """获取用户输入的正整数"""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("请输入一个正整数。")
        except ValueError:
            print("输入不是数字，请重新输入。")


def get_user_input():
    """获取用户输入的配置"""
    title = input("请输入标题: ")
    while not title.strip():
        print("标题不能为空，请重新输入。")
        title = input("请输入标题: ")

    num_options = get_positive_int("请输入选项个数: ")
    options = []
    for i in range(1, num_options + 1):
        option = input(f"请输入选项{i}: ")
        while not option.strip():
            print("选项不能为空，请重新输入。")
            option = input(f"请输入选项{i}: ")
        options.append(option)
    return title, options


def delete_config(configs):
    """删除配置"""
    if not configs:
        print("没有配置可以删除。")
        return
    print("已保存的配置列表：")
    for key, config in configs.items():
        print(f"{key}: {config['title']}")
    while True:
        choice = input("请输入要删除的配置编号: ")
        if choice in configs:
            del configs[choice]
            save_configs(configs)
            print("配置已删除。")
            break
        elif choice.isdigit():
            print("无效的配置编号，请重新输入。")
        else:
            print("输入无效，请输入数字编号。")


def view_configs(configs):
    """查看所有配置"""
    if not configs:
        print("没有配置可以查看。")
        return
    print("\n已保存的配置列表：")
    for key, config in configs.items():
        print(f"编号: {key}, 标题: {config['title']}, 选项: {', '.join(config['options'])}")


def select_or_add_config(configs):
    """选择或添加配置"""
    if not configs:
        print("没有找到配置列表，将创建新的配置。")
        config_id = "1"
    else:
        print("已保存的配置列表：")
        for key, config in configs.items():
            print(f"{key}: {config['title']}")
        config_id = input("请输入配置编号选择已有配置，或输入新编号添加新配置: ")
        if config_id.isdigit():
            config_id = config_id  # 保持为字符串类型
            if config_id in configs:
                return config_id
            else:
                print("编号不存在，将创建新的配置。")
                config_id = str(max(int(key) for key in configs.keys()) + 1) if configs else "1"
        else:
            print("输入无效，将创建新的配置。")
            config_id = str(max(int(key) for key in configs.keys()) + 1) if configs else "1"

    title, options = get_user_input()
    configs[config_id] = {'title': title, 'options': options}
    save_configs(configs)
    return config_id


def main():
    configs = load_configs()

    while True:
        print("\n1. 选择或添加配置")
        print("2. 删除配置")
        print("3. 查看所有配置")
        print("4. 退出")
        choice = input("请选择一个操作: ")

        if choice == '1':
            config_id = select_or_add_config(configs)
            title = configs[config_id]['title']
            options = configs[config_id]['options']
            print(f"{title}?")
            print(random.choice(options))
        elif choice == '2':
            delete_config(configs)
        elif choice == '3':
            view_configs(configs)
        elif choice == '4':
            print("退出程序。")
            break
        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()