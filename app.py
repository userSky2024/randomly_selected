from flask import Flask, request, jsonify, render_template
import json
import os
import random

from flask_cors import CORS

app = Flask(__name__)

# 允许所有域名跨域访问
CORS(app)

# 定义保存配置的JSON文件名
config_file = 'configs.json'

def load_configs():
    """从JSON文件加载多个配置"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_configs(configs):
    """保存多个配置到JSON文件"""
    with open(config_file, 'w') as f:
        json.dump(configs, f)

@app.route('/')
def index():
    """根端点，显示API文档"""
    return render_template('api_docs.html')

@app.route('/configs', methods=['GET'])
def get_configs():
    """获取所有配置"""
    configs = load_configs()
    return jsonify(configs)

@app.route('/configs/<int:config_id>', methods=['GET'])
def get_config(config_id):
    """根据ID获取特定配置"""
    configs = load_configs()
    if str(config_id) in configs:
        return jsonify(configs[str(config_id)])
    else:
        return jsonify({'error': 'Config not found'}), 404

@app.route('/configs', methods=['POST'])
def add_config():
    """添加新配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # 检查必要的字段是否存在
        required_fields = ['title', 'options']
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        configs = load_configs()
        config_id = str(max(int(key) for key in configs.keys()) + 1) if configs else "1"
        configs[config_id] = data
        save_configs(configs)
        return jsonify({"message": "配置添加成功"}), 200

    except Exception as e:
        # 这里可以记录日志或者进行其他错误处理
        return jsonify({'error': 'An error occurred while processing the request'}), 500

@app.route('/configs/<int:config_id>', methods=['DELETE'])
def delete_config(config_id):
    """删除配置"""
    configs = load_configs()
    if str(config_id) in configs:
        del configs[str(config_id)]
        save_configs(configs)
        return jsonify({"message": "配置删除成功"}), 200
    else:
        return jsonify({'error': 'Config not found'}), 404

@app.route('/random/<int:config_id>', methods=['GET'])
def random_option(config_id):
    """随机选择特定config_id配置的选项"""
    configs = load_configs()
    if str(config_id) in configs:
        config = configs[str(config_id)]
        if config['options']:
            random_option = random.choice(config['options'])
            return jsonify({'config_id': config_id, 'random_option': random_option})
        else:
            return jsonify({'error': 'No options available for this config'}), 404
    else:
        return jsonify({'error': 'Config not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)