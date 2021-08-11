# 半次元开播提醒

MacOS 版 B 站开播提醒

还在为每天无法准时 DD 苦恼不已吗？还不来试试俺滴开播提醒！！！

# Usage

1. 确保安装 Python 且版本 >= 3.7
2. 安装 requests 包：`pip install requests`
3. 打开配置文件 `./conf/live.conf`，设置直播间房间号及提醒文案
4. 在 cron 中为主程序 `./src/alert.py` 添加定时任务

> **Note**: 如何设置 cron
> 
> 打开 Terminal，输入命令 `crontab -e`。按 a 切换到编辑模式，然后在 cron 中加入一行：
> 
> PS: 注意了，要记得把下面的 [PATH_TO_YOUR_SCRIPT] 替换成你自己的路径哦！！！
> 
> ```*/3 * * * * source ~/.bash_profile; cd [PATH_TO_YOUR_SCRIPT]; python alert.py >> ../log/alert.log 2>> ../log/alert.err```
> 
> 按 ESC 键，输入 `:x` 然后按回车键退出

# Useful resources

osascript 介绍：

- [osascript](https://ss64.com/osx/osascript.html)

设置 cron 时可能遇到的问题：

- [crontab: Operation not permitted](https://serverfault.com/questions/954586/osx-mojave-crontab-tmp-tmp-x-operation-not-permitted)
<!-- - [PermissionError: [Errno 1] Operation not permitted after macOS Catalina Update](https://stackoverflow.com/questions/58479686/permissionerror-errno-1-operation-not-permitted-after-macos-catalina-update) -->
