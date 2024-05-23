import configparser

# 初始化配置
conf = configparser.ConfigParser()

pip_config = "/etc/pip.conf"
# 添加节点
conf.add_section("global")
conf.add_section("install")

# 添加键值对
conf.set("global", "index-url", "https://pypi.tuna.tsinghua.edu.cn/simple")
conf.set("install", "trusted-host", "pypi.tuna.tsinghua.edu.cn")
conf.write(open(pip_config, "w"))
