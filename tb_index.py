from flask import Flask, render_template, request, jsonify
import os
import subprocess
from gevent import pywsgi

app = Flask(__name__)

# 資料夾路徑
base_folder = "./logs/"

# 取得第一層的資料夾列表
first_level_folders = [f for f in os.listdir(
    base_folder) if os.path.isdir(os.path.join(base_folder, f))]


@app.route('/')
def index():
    return render_template('index.html', first_level_folders=first_level_folders)


@app.route('/get_subfolders', methods=['POST'])
def get_subfolders():
    selected_folder = request.form.get('selected_folder')
    folder_path = os.path.join(base_folder, selected_folder)

    # 取得下一層的資料夾列表
    subfolders = [f for f in os.listdir(
        folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    return {'subfolders': subfolders}


@app.route('/show_selected_folders', methods=['POST'])
def show_selected_folders():
    first_level_folder = request.form.get('first_level_folder')
    subfolder = request.form.get('subfolder')

    # 獲取完整路徑
    full_path = os.path.join(base_folder, first_level_folder, subfolder) if subfolder else os.path.join(
        base_folder, first_level_folder)

    # 在這裡，您可以使用完整路徑進行相應的處理
    # 例如，您可以將它傳遞到網頁或進行其他操作

    # 返回JSON格式的資料，包括完整路徑
    return jsonify({'first_level_folder': first_level_folder, 'subfolder': subfolder, 'full_path': full_path})


@app.route('/run_tensorboard', methods=['POST'])
def run_tensorboard():
    selected_path = request.form.get('selected_path')
    print(selected_path)
    os.system("kill $(ps -e | grep 'tensorboard' | awk '{print $1}')")
    # 使用 subprocess 执行 tensorboard 命令
    command = ['tensorboard', '--logdir',
               "./logs/"+selected_path, "--bind_all"]
    result = subprocess.run(command, capture_output=True, text=True)

    res = jsonify({'result': result.stdout, 'error': result.stderr})
    # 返回执行结果
    return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
