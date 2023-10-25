import subprocess,sys,argparse

# 要执行的Python脚本
script = 'main.py'
script_cmd = 'main.pyw'

# 创建解析器
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cmd", action="store_true", help="打开cmd")
args = parser.parse_args()

if args.cmd:
    # 打开命令行窗口，并执行Python脚本
    subprocess.Popen(['cmd.exe', '/c', f'python {script}'])
else:
    # 在后台运行Python脚本，不打开命令行窗口
    subprocess.Popen([sys.executable, script_cmd])
