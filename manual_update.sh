#!/bin/bash
temp_date=$(date)

#进入这个路径，因为这里是git的环境
#因为有可能在其他路径下执行这个脚本
#fix bug on 09/11/2015
cd /home/jun/git/code && /usr/bin/git branch tmp
cd /home/jun/git/code && /usr/bin/git checkout tmp
cd /home/jun/git/code && /usr/bin/git add . --all
#echo "please input commit message:"
#read message
cd /home/jun/git/code && /usr/bin/git commit -m "code on $temp_date"
cd /home/jun/git/code && /usr/bin/git checkout master
cd /home/jun/git/code && /usr/bin/git merge tmp
cd /home/jun/git/code && /usr/bin/git push origin master
cd /home/jun/git/code && /usr/bin/git branch -d tmp
