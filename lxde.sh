#!/bin/sh
#
echo  ----- Ubuntu 办公电脑设置程序  ----------

export ROOTDIR="$(pwd)"

# ------------------------------
# 添加第三方源
# ------------------------------
CODENAME="$(lsb_release -sc)"
cp -f /etc/apt/sources.list /etc/apt/sources.list.bak
if [ -f /etc/lsb-release ] || [ -z "$( cat /etc/lsb-release | grep debian )" ]; then
    # 替换源为国内服务器
    if [ -f "$( grep 'ubuntu.com' /etc/apt/sources.list )" ];then
        sed -i 's/cn.archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
        sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
        sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
    fi
    # Ubuntu
    dist='ubuntu'
    if [ -f /etc/apt/sources.list.d/official-package-repositories.list ];then
        mv -f /etc/apt/sources.list.d/official-package-repositories.list /etc/apt/sources.list
    fi
    if [ -n "$( grep deepin /etc/apt/sources.list )" ];then
        dist='deepin'
        sed -i "s#http://.*/#http://mirrors.aliyun.com/#" /etc/apt/sources.list
    elif [ -n "$( grep mint /etc/apt/sources.list )" ];then
        dist='mint'
        # 判断mint对应ubuntu版本
        if [ -n "$( grep linuxmint  /etc/apt/sources.list )" ];then
            CODENAME="$( awk '/canonical/{print $3}' /etc/apt/sources.list )"
        fi
        apt-get -y purge libreoffice*    # 删除，替换按照wps
        # 替换源为国内服务器
        sed -i 's#packages.linuxmint.com#mirrors.ustc.edu.cn/linuxmint#g' /etc/apt/sources.list
        # 增加搜狗拼音
        apt-key adv --keyserver keyserver.ubuntu.com --recv-keys D259B7555E1D3C58
        echo "deb http://archive.ubuntukylin.com:10006/ubuntukylin/ $CODENAME main" > /etc/apt/sources.list.d/ubuntukylin.list
        soft="$soft pidgin caja-sendto ttf-wqy-microhei xfonts-wqy fcitx fcitx-frontend-gtk3 fcitx-ui-classic fcitx-table-wubi  mint-backgrounds-* ubuntu-restricted-extras ttf-xfree86-nonfree language-pack-zh-hans language-pack-gnome-zh-hans thunderbird-locale-zh-hans firefox-locale-zh-hans sogoupinyin fcitx-config-gtk fcitx-module-kimpanel"
    fi
else
    echo "操作系统版本错误."
    exit 255
fi
sed -i /deb-src/d /etc/apt/sources.list

# ------------------------------
# 屏蔽软件安装需要确认提示
# ------------------------------
export DEBIAN_FRONTEND='noninteractive'
user="$(awk -F: '{if($3==1000)print $1 }' < /etc/passwd )"

# ------------------------------
# 升级系统
# ------------------------------
apt-get -y update
apt-get -y upgrade

# ------------------------------
#  安装需要的程序
# ------------------------------
apt-get -y install vim-gnome vim-scripts htop traceroute terminator p7zip-full p7zip-rar rar remmina-plugin-rdp exuberant-ctags ssh build-essential libcurl3 myspell-en-us amule numlockx bash-completion seahorse rdesktop network-manager-openvpn-gnome git python-xlib curl  unace sharutils arj lunzip lzip clipit firefox-locale-zh-hans resolvconf
apt-get -y install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy
if [ ! -f /usr/bin/git ];then
	exit 255
fi
if [ -n $soft];then
    apt-get -y install $soft
fi
apt-get -y install aliedit
if [ "$dist" == 'mint' ];then
    wget http://mirrors.ustc.edu.cn/deepin/pool/non-free/d/deepinwine-qqintl/wine-qqintl_0.1.3-2_i386.deb
    wget http://packages.linuxdeepin.com/deepin/pool/main/d/deepin-scrot/deepin-scrot_2.0-0deepin_all.deb
    wget http://mirrors.ustc.edu.cn/deepin/pool/non-free/w/wps-office/wps-office_9.1.0.4909~a16p1_i386.deb
    wget http://mirrors.ustc.edu.cn/deepin/pool/non-free/w/wps-office-fonts/wps-office-fonts_1.0_all.deb
    wget http://mirrors.ustc.edu.cn/deepin/pool/non-free/w/wps-office-mui-zh-cn/wps-office-mui-zh-cn_9.1.0.4751~a15_all.deb
    im-switch -s fcitx -z default
    apt-get install -f

    #   添加中文编码支持
    locale-gen zh_CN zh_CN.utf8  zh_CN.GB18030 zh_CN.GBK zh_HK zh_HK.utf8 zh_SG.utf8 zh_TW zh_TW.utf8

    # ------------------------------
    #  安装字体
    # ------------------------------

    # mkdir -p /usr/share/fonts/msyh
    # wget -T 10 -t 3 http://soft.oa.com/msyh.ttf  -O  /usr/share/fonts/msyh/msyh.ttf
    # wget -T 10 -t 3 http://soft.oa.com/msyhbd.ttf -O  /usr/share/fonts/msyh/msyhbd.ttf
    # wget -T 10 -t 3 http://soft.oa.com/symbol-fonts_1.1_all.deb -O /tmp/symbol-fonts_1.1_all.deb

fi
dpkg -i *.deb
rm -f *.deb

echo '15 15 * * * root /usr/sbin/ntpdate 0.debian.pool.ntp.org > /dev/null 2>&1' >> /etc/crontab #设置自动对时
echo "apt-get update && apt-get -y upgrade > /dev/null 2>&1" >> /etc/rc.local #设置自动更新

# ------------------------------
# 修改QQ崩溃问题
# ------------------------------
if [ -d "/home/$user/.cxoffice/Deepin-QQ/drive_c/users/crossover/Application Data/Tencent/QQ/Misc/com.tencent.wireless/SDK/" ];then
    chmod 000 "/home/$user/.cxoffice/Deepin-QQ/drive_c/users/crossover/Application Data/Tencent/QQ/Misc/com.tencent.wireless/SDK/"
fi

# ------------------------------
# 设置SUDO 修改图形执行gksu-properties改为sudo模式
# ------------------------------
    chmod +w /etc/sudoers
    echo "$user     ALL=NOPASSWD:ALL" >> /etc/sudoers
    chmod 0440 /etc/sudoers

# ------------------------------
# 设置Host
# ------------------------------
echo "nospoof on        #禁止ip地址欺骗" >>/etc/host.conf

# -------------------
#  判断目录
# -----------------
if [ -d /work ];then
    work=work
else
    work=web
fi

# -------------------
#  配置windows 测试服务器的菜单
# -----------------
mkdir -p /$work/tools
    echo "#!/bin/bash
xmodmap -e "keysym Alt_L = Alt_L"
rdesktop -z -g 1680x1000 -D -u telking -p telking -r disk:$work=/$work -r clipboard:PRIMARYCLIPBOARD -a 24 -x lan  windows.oa.com" > /$work/tools/windows

    echo "[Desktop Entry]
Name=Windows Develop Computer
Name[zh_CN]=Windows开发电脑
Encoding=UTF-8
GenericName=Windows Develop Computer
GenericName[zh_CN]=Windows开发电脑
Comment='Windows Develop Computer'
Comment[zh_CN]=开发测试使用Windows主机
Icon=remmina
Exec=bash /$work/tools/windows
MimeType=text/x-tex;
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;Application;Development;" > /usr/share/applications/windows.desktop

# ------------------------------
# 设置BASH彩色 即时显示效果命令：source ~/.bashrc#
# ------------------------------
wget  --no-check-certificate -T 10 -t 3 -O /etc/dir_colors https://raw.github.com/seebi/dircolors-solarized/master/dircolors.ansi-universal
echo 'eval `dircolors /etc/dir_colors`' >> /etc/bash_profile
echo "unset MAILCHECK" >> /etc/profile
echo   "#apt-get install自动补全
if [ -f /etc/bash_completion ]; then
           . /etc/bash_completion
       fi
# 常用命令
alias run='sudo python manage.py runserver --threaded -h 0 -p 80'
alias cman='man -M /usr/share/man/zh_CN'
export EDITOR=vim
alias vi='vim'
#定制命令行彩色
alias ls='ls --color=auto'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias run='sudo python3 manage.py runserver --threaded -h 0 -p 80'
alias run2='sudo python manage.py runserver --threaded -h 0 -p 80'
alias run3='sudo python3 manage.py runserver --threaded -h 0 -p 80'
# colorful man page
export LESS_TERMCAP_mb=$'\E[01;34m'
export LESS_TERMCAP_md=$'\E[01;34m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;33m'
" >> /etc/bash.bashrc
echo 'export PAGER="`which less` -s"
export BROWSER="$PAGER"' >> /etc/bash.bashrc
echo "PS1='[\u\[\033[00m\]@\$(hostname -f) \[\033[01;34m\]\$(hostname -i)\[\033[00m\]:\w]\\$ '
unset MAILCHECK" >> /etc/profile

echo 'set bell-style none
set match-hidden-files off
set show-all-if-ambiguous on
set completion-ignore-case on
"\ep": history-search-backward
"\e[A": history-search-backward
"\e[B": history-search-forward' >> /etc/inputrc

# ------------------------------
# 设置zsh
# ------------------------------
echo   "
# 常用命令
alias run='sudo python3 manage.py runserver --threaded -h 0 -p 80'
alias run2='sudo python manage.py runserver --threaded -h 0 -p 80'
alias run3='sudo python3 manage.py runserver --threaded -h 0 -p 80'
#定制命令行彩色
alias ls='ls --color=auto'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias tree='tree -C'
export CLICOLOR=1
#export LSCOLORS=gxfxcxdxbxegedabagacad
# colorful man page
export LESS_TERMCAP_mb=$'\E[01;34m'
export LESS_TERMCAP_md=$'\E[01;34m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;33m'
# 设置用户
DEFAULT_USER=\"$user\"
" >> /home/$user/.zshrc
echo '#彩色补全菜单
eval `dircolors ~/.dir_colors`
export ZLSCOLORS="${LS_COLORS}"
# 插件补齐
plugins+=(git gitignore git-flow  python supervisor redis-cli zsh-completions command-not-found gnu-utils colored-man colorize history pip sudo autojump osx docker-compose docker postgres zsh-syntax-highlighting extract z rsync ubuntu)
autoload -U compinit && compinit' >>  /home/$user/.zshrc
sed -i 's/}%c/}%~/' /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
sed -i 's/git://' /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
sed -i 's/cyan/blue/' /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
sed -i 's/➜ :/:/' /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
echo 'ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[yellow]%}✗%{$fg[blue]%})"' >> /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
sed -i 's/ % / %(#.#.$) /' /usr/share/oh-my-zsh/themes/robbyrussell.zsh-theme
# sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="gentoo"/' /home/$user/.zshrc
echo 'ZSH_THEME_GIT_PROMPT_PREFIX="(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%} %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%}" ' >> /usr/share/oh-my-zsh/themes/gentoo.zsh-theme
sudo -u $user -s source /home/$user/.zshrc

# ------------------------------
# 设置SSH
# ------------------------------
sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/ssh_config
sed -i "s/Port 22/Port 51450/" /etc/ssh/sshd_config  #修改端口
mkdir -p /home/$user/.ssh
echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCj3KTpWWjbvsZeOrUIORR+Ve1aT2qdqVTVpltKZjGkg17fk6h/PlSYMFvQVBziMxyXwPmDFJY7E4eTp6XmcNISpMuemYhagTeHMcE97XY2vjPlvNVfwLRbxVmvXUiB3weKF0gBAIXJcacgjHPGo2YGZ3fhrZqgTyeDzwFV7n+/NsBI215R62yTzUfdbSSAj1wiI1EHUIm8FQen4TksOwoeZ6uasdyfXKADouXolhAq0m2rSytsCb+xST95hhlOiLiEHl1tlW4cNSUVb9j5ZDMHrsnjLOliEvtCcMT34J65jZqrJN006eNP+Q9HDCBhxda+MakGdiUNccd7a/XJtC6f ronin@ronin' >> /home/$user/.ssh/authorized_keys
chmod 600  /home/$user/.ssh/authorized_keys
chown -R  $user.$user /home/$user/
echo '      Port 51450' >>/etc/ssh/ssh_config
echo 'PasswordAuthentication no' >>/etc/ssh/ssh_config
echo 'ControlMaster auto' >>/etc/ssh/ssh_config
echo '' >>/etc/ssh/ssh_config
/etc/init.d/ssh restart

# ------------------------------
# 设置Terminator
# ------------------------------
mkdir -p /home/$user/.config/terminator
echo '[profiles]
  [[default]]
    use_system_font = False
    font = 文泉驿等宽微米黑 11
    scrollback_infinite = True
    show_titlebar = False
    #login_shell = True
    #use_custom_command = True
    custom_command = tmux -2' > /home/$user/.config/terminator/config
chown $user.$user  /home/$user/.config/terminator/config

# ------------------------------
# 设置使用VIM
# ------------------------------
vim="$( find /usr/share/vim -name vim7* -type d )"
sed -i 's/*.ini/*.ini,*.conf/' $vim/filetype.vim
vimrc=/etc/vim/vimrc
mkdir -p /home/$user/.vimbackup
mkdir -p /root/.vimbackup
echo '
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 文件编码选项
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set encoding=utf-8
set fileencodings=ucs-bom,utf-8,chinese,prc,taiwan,latin-1
set fileencoding=utf-8
set ffs=unix,dos,mac        "保存文件格式fileformats
set ff=unix                 "设置缓冲区换行符格式
set nobomb                  "禁止BOM标识(字节顺序标记)
"set langmenu=none          "禁止中文提示信息
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 常规选项
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set backspace=indent,eol,start  "设置后退键
set whichwrap=b,s,<,>,[,]   "设置移动换行
autocmd! bufwritepost _vimrc source %    "修改_vimrc后自动生效
autocmd bufenter * cd %:p:h     "设置工作目录到当前路径
autocmd bufreadpost * lcd %:p:h
autocmd bufwritepre * lcd %:p:h
"autocmd bufwritepre * sil! %s/\s\+$//e   "保存文件时自动删除行尾空格或Tab
set clipboard=unnamedplus   "共享外部剪贴板
set viminfo+=!              "保存全局变量
set wildmenu                "增强模式中的命令行自动完成操作
set wildmode=longest,list   "命令行使用补全模式
set showcmd                 "显示未完成命令
set autochdir               "自动设当前编辑的文件所在目录为当前工作路径
set history=1024
set paste
set tabpagemax=20
set autoread                "文件被其他程序修改时自动载入
set ambiwidth=double        "修复中文标点显示
set formatoptions+=mM       "正确地处理中文字符的折行和拼接
let g:vimim_disable_chinese_punctuation=1       "关闭中文标点
let g:vimim_disable_seamless_english_input=1    "中英文之间不加空格
set nocompatible            "使用VIM键盘模式
set ignorecase              "搜索忽略大小写
set confirm                 "在处理未保存或只读文件的时候，弹出确认
set mouse=a                 "支持鼠标
set selection=exclusive     "可以在buffer的任何地方使用鼠标
set selectmode=mouse,key    "可以在buffer的任何地方使用鼠标
set hlsearch                "搜索结果高亮
syntax enable               "彩色显示
syntax on                   "彩色显示
set t_Co=256                "指定配色方案是256色,会造成启动慢
set number                  "显示行号
set shortmess=atI           "启动的时候不显示那个援助索马里儿童的提示
set fillchars=vert:\ ,stl:\ ,stlnc:\  "在被分割的窗口间显示空白，便于阅读
filetype on                 "检测文件类型
filetype plugin indent on   "载入文件类型插件
set ruler                   "右下角显示光标位置的状态行
set noerrorbells            "关闭遇到错误时的声音提示
set vb t_vb=                "关闭遇到错误时的声音提
set history=1000            "记录历史行数
set cursorline              "高亮显示当前行
"hi cursorline guibg=#222222
"hi CursorColumn guibg=#333333
set scrolloff=3             "光标移动到buffer的顶部和底部时保持3行距离
set report=0                "告诉我们文件的哪一行被改变过
set guioptions-=b           "隐藏底部滚动条
set novisualbell            "不要闪烁
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => F12处理行尾的空格以及文件尾部的多余空行
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Automatically remove trailing spaces when saving a file.
autocmd BufRead,BufWrite * if ! &bin | silent! %s/\s\+$//ge | endif
"Remove indenting on empty line
map <F12> :w<CR>:call CleanupBuffer(1)<CR>:noh<CR>
function! CleanupBuffer(keep)
    " Skip binary files
    if (&bin > 0)
        return
    endif
    " Remove spaces and tabs from end of every line, if possible
    silent! %s/\s\+$//ge
    " Save current line number
    let lnum = line(".")
    " number of last line
    let lastline = line("$")
    let n        = lastline
    " while loop
    while (1)
        " content of last line
        let line = getline(n)
        " remove spaces and tab
        if (!empty(line))
            break
        endif
        let n = n - 1
    endwhile
    " Delete all empty lines at the end of file
    let start = n+1+a:keep
    if (start < lastline)
        execute n+1+a:keep . "," . lastline . "d"
    endif
    " after clean spaces and tabs, jump back
    exec "normal " . lnum . "G"
endfunction
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 按键编排
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap w :w<cr>
nmap q :q!<cr>
nmap tn :tabnext<cr>
nmap tp :tabprevious<cr>
nmap tw :tabnew .<cr>
nmap te :tabedit<cr>
nmap tc :tabcloose<cr>
nmap tm :tabmove<cr>
nmap tl :tablast<cr>
nnoremap <c-s-f> 1G=G        "自动排版ctrl + shift + f
inoremap <c-s-f> <ESC>1G=Gi
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 文件备份选项
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set backup
set backupdir=~/.vimbackup
autocmd BufWritePre * let &backupext = strftime(".%m-%d-%H-%M")
set noswapfile              "关闭临时交换文件
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 代码折叠
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set foldmethod=indent       "使用高级模式
set foldnestmax=10          "最大折叠层次
set nofoldenable            "不设置为默认折叠
set foldlevel=1             "折叠级别
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => 编辑选项
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set autoindent              "自动缩进
set smartindent             "智能缩进
set shiftwidth=4            "自缩进4个空格
set expandtab               "将Tab转为空格
set smarttab                "一个Backspace就删除4个空格
set tabstop=4               "设置一个TAB四个空格
set softtabstop=4           "统一缩进4个空格
set showmatch               "显示括号匹配
set matchpairs=(:),{:},[:],<:>      "匹配括号的规则，增加针对html的<>
set matchtime=1             "括号匹配显示时间为1(最短的，似乎1,2,3,4,5可选)
set incsearch               "自动查询功能
let g:acp_mappingDriven = 1 "禁止在插入模式移动的时候出现 Complete 提示
autocmd BufNewFile,BufRead nginx.conf*,fcgi.conf,*.com*,*.net*.*.org*,*.cn* set syntax=apachestyle           "高亮nginx配置文件
autocmd BufNewFile,BufRead */conf/vhosts/* set syntax=apachestyle       "高亮nginx配置文件
autocmd FileType ruby,eruby set omnifunc=rubycomplete#Complete          "代码补全ruby,需要补全的时候ctrl-x ctrl-o
autocmd FileType python set omnifunc=pythoncomplete#Complete            "代码补全python
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS  "代码补全javascript
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags            "代码补全html
autocmd FileType css set omnifunc=csscomplete#CompleteCSS               "代码补全css
autocmd FileType xml set omnifunc=xmlcomplete#CompleteTags              "代码补全xml
autocmd FileType java set omnifunc=javacomplete#Complete                "代码补全java
" 插入匹配括号
inoremap ( ()<LEFT>
inoremap [ []<LEFT>
inoremap { {}<LEFT>
""""""""""""""""""""""""""""""
" => 能够漂亮的显示.NFO文件
""""""""""""""""""""""""""""""
function! SetFileEncodings(encodings)
    let b:myfileencodingsbak=&fileencodings
    let &fileencodings=a:encodings
endfunction
function! RestoreFileEncodings()
    let &fileencodings=b:myfileencodingsbak
    unlet b:myfileencodingsbak
endfunction
au BufReadPre *.nfo call SetFileEncodings('cp437')|set ambiwidth=single
au BufReadPost *.nfo call RestoreFileEncodings()
""""""""""""""""""""""""""""""
" => 状态栏
""""""""""""""""""""""""""""""
set laststatus=2            "总是显示状态行
"黓认状态栏格式
hi StatusLine  guifg=#FFFFFF guibg=#393939 gui=none
autocmd InsertEnter * hi StatusLine guifg=#E0E0E0 guibg=Grey40 gui=none
autocmd InsertLeave * hi StatusLine guifg=#FFFFFF guibg=#393939 gui=none
" 设置状态栏格式
set statusline=\ %F%m%r%h\ [%Y]\ [%{&ff}]\ %w\ \ \ \ \ Encoding:\ %{(&fenc==\"\")?&enc:&fenc}%{(&bomb?\"[BOM]\":\"\")}\ \ \ \ \ Line:\ %l\|%L:%c\ [%p%%-%P]
"set statusline=%F%m%r%h\ [%Y]\ [%{&ff}]\ [%{&fenc}:%{&enc}]\ [%08.8L]\ [%p%%-%P]\ [%05.5b]\ [%04.4B]\ [%08.8l]%<\ [%04.4c-%04.4v%04.4V]
"设置自定义的<leader>快捷键
let mapleader=","
let g:mapleader=","
"""""""""""""""""""""""""""""""
" =>上下移动一行或多行代码并自动调整缩进
" =>做改动前，保存当前光标位置和恢复位置
 """""""""""""""""""""""""""""""
nnoremap <C-u>  mz:m-2<cr>`z==
nnoremap <C-d>  mz:m+<cr>`z==
'>> $vimrc
echo "inoremap <C-u>  :m'<-2<cr>gv=gv
inoremap <C-d>  :m'>+<cr>gv=gv
autocmd bufwritepre * let s:saveCursor=getpos('.')
autocmd bufWritepost * call setpos('.',s:saveCursor)
" >> $vimrc
#
# 安装配色方案 -------
#
cd $vim/colors
wget -T 10 -t 3 -O eclm_wombat.vim http://www.vim.org/scripts/download_script.php?src_id=9702
wget -T 10 -t 3 -O blackboard.vim http://www.vim.org/scripts/download_script.php?src_id=11225
wget -T 10 -t 3 -O darkburn.vim http://www.vim.org/scripts/download_script.php?src_id=10756
wget --no-check-certificate -T 10 -t 3 -O solarized.vim https://github.com/altercation/vim-colors-solarized/raw/master/colors/solarized.vim
echo '
if has("gui")
    colorscheme blackboard
    set wrap                  "不折行
    set gcr=a:block-blinkon0    "光标不要闪烁
    let do_syntax_sel_menu=1    "在菜单上显示文件类型
    set guifont=文泉驿等宽微米黑\ 11    "设置GUI字体
    set guifontwide=文泉驿等宽微米黑\ 11
    set guioptions-=m           "隐藏菜单栏
    set guioptions-=T           "隐藏工具栏
    set sessionoptions+=resize "保存窗口大小
    set langmenu=zh_CN.UTF-8
    set imcmdline
    source $VIMRUNTIME/delmenu.vim
    source $VIMRUNTIME/menu.vim
    ' >> $vimrc
    echo "map <silent> <F2> :if &guioptions =~# 'T' <Bar>set guioptions-=T <Bar>set guioptions-=m <bar>else <Bar>set guioptions+=T <Bar>set guioptions+=m <Bar>endif<CR>
else
    syntax enable
    let g:solarized_termcolors=256
    set background=dark
    colorscheme solarized
    set wrap
endif
" >> $vimrc
#
# 安装常用插件-------
#
echo "
syntax on
filetype plugin indent on" >>  /home/$user/.vimrc
chown -R $user.$user /home/$user/.vim
chown $user.$user /home/$user/.vimrc
# 常用插件
cd $vim/plugin
#wget -T 10 -t 3 -O mru.vim http://www.vim.org/scripts/download_script.php?src_id=11919
wget -T 10 -t 3 -O python.vim http://www.vim.org/scripts/download_script.php?src_id=20604
wget -T 10 -t 3 http://gracecode.googlecode.com/files/mru.vim   #网友修改版
touch /home/$user/.vim_mru_files
echo '
imap <silent> <F3> <esc>:MRU<CR>
nmap <silent> <F3> :MRU<CR>
imap <silent> <F10> <esc>:NERDTreeToggle<CR>
nmap <silent> <F10> :NERDTreeToggle<CR>
' >> $vimrc

# ------------------------------
# 优化Linux内核
# ------------------------------
echo   "vm.swappiness=1" >>/etc/sysctl.conf

#
echo ------- 设置权限 ---------
#
if [ -d /home/$user/桌面 ];then
    desktop='桌面'
fi
if [ -d /home/$user/Desktop ];then
    desktop='Desktop'
fi
if [ ! -d /home/$user/下载 ] && [ -d /home/$user/下载 ];then
    ln -sf /home/$user/下载 /home/$user/Downloads
fi
ln -s  /home/$user/下载  /home/$user/$desktop/
ln -s  /home/$user/文档  /home/$user/$desktop/
chown $user.$user -R /home/$user

if [ -d /web ];then
    cd $ROOTDIR
# ------------------------------
#  安装开发环境
# ------------------------------
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
    echo "deb http://ppa.launchpad.net/webupd8team/brackets/ubuntu $CODENAME main" > /etc/apt/sources.list.d/brackets.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 2FF96FD1
    echo "deb http://ppa.launchpad.net/jerzy-kozera/zeal-ppa/ubuntu $CODENAME main" > /etc/apt/sources.list.d/zeal.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv 9ECBEC467F0CEB10
    echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" > /etc/apt/sources.list.d/mongodb.list
    apt-get update
    apt-get -y install filezilla  gegl git  meld gitg redis-server gcc-multilib  whois librtmp-dev python-dev python-pip  libev-dev liblapack-dev gfortran libcups2-dev libjpeg-dev giggle python-tk
    apt-get -y install libcurl4-openssl-dev libsctp1  libxml2-dev libxslt1-dev libcups2-dev libtiff5-dev libwebp-dev libfreetype6-dev libpng12-dev zlib1g-dev liblcms1-dev
    #apt-get -y install brackets
    apt-get -y install mongodb-org
    apt-get -y install firefox firefox-locale-zh-hans xul-ext-https-finder
    sed -i 's/# unixsocket/  unixsocket/' /etc/redis/redis.conf   # 使用socket接口
    sed -i 's/755/777/' /etc/redis/redis.conf   # 使用socket接口
    wget -T 10 -t 3 http://robomongo.org/files/linux/robomongo-0.8.5-x86_64.deb
    dpkg -i robomongo-*.deb # 安装mongodb管理工具
    rm -f robomongo-*.deb
    echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' >> /etc/rc.local
    echo 'echo never > /sys/kernel/mm/transparent_hugepage/defrag' >> /etc/rc.local

# -------------------
#  设置python镜像
# -------------------
echo '[global]
trusted-host = pypi.douban.com
index-url = http://pypi.douban.com/simple
timeout = 30' > /etc/pip.conf

# -------------------
#  安装python组件
# -------------------
pip install -U -i http://pypi.douban.com/simple/ ipython flake8 pydns Flask-DebugToolbar pep8 Pillow pyquery pycurl2 Flask-Bcrypt Flask-Security Flask-Uploads Flask-Script flask-csrf flask-redis flask-pymongo flask_mongoengine hanzi2pinyin gevent requests threadpool six Flask-DebugToolbar-Mongo
echo "/web/www/dliapi" > /usr/local/lib/python2.7/dist-packages/dliapi.pth
echo "/web/www/pomelo" > /usr/local/lib/python2.7/dist-packages/pomelo.pth
echo "/web/www/core" > /usr/local/lib/python2.7/dist-packages/core.pth
echo "/web/www/dcore" > /usr/local/lib/python2.7/dist-packages/dcore.pth
echo "/web/www/spider" > /usr/local/lib/python2.7/dist-packages/spider.pth

# -------------------
#  配置GIT
# -------------------
echo "[core]
        excludesfile = /home/$user/.gitignore
        quotepath = false
        pager = less -r
[push]
	default = simple
[alias]
        co  =   checkout
        ci  =   commit -a
        st  =   status
        br  =   branch
        lg  =   log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
[branch]
        autosetuprebase = always
[diff]
    external = git-meld
[merge]
   log = true
   summary = true
   ff = false
[color]
        status  =   auto
        interacitve = auto
        diff = auto
        branch  =   auto
        ui  =   auto" >> /home/$user/.gitconfig
echo '# 需要忽略文件名
*.o
*.a
*.so
*.[568vq]
*.cgo1.go
*.cgo2.c
_cgo_defun.c
_cgo_gotypes.go
_cgo_export.*
_testmain.go
*.exe
.*
*~
*.py[co]
*.swp
*.swo
*.db
*.zip
*.bz2
*.gz
*.orig
*.bak
*.log
*.lock
*.out
*.pot
*.coverage
*.egg
*.egg-info
*.tox
*.DS_Store
*.cache
*.class
*.rra
.installed.cfg
pip-log.txt
*.mo
*.tmp*
.mr.developer.cfg
local_settings.py
*.cfg
*.todo
# 需要忽略文件夹
projectFilesBackup
.idea
.settings
tmp_*
_obj
_test
eggs
develop-eggs
rra
parts
pack*
bin
var
sdist
nbproject/private/
dist
build
_project
docs/output
cache*
/upload*' > /home/$user/.gitignore
echo '#!/bin/sh
meld $2 $5' > /usr/local/bin/git-meld
chmod a+x /usr/local/bin/git-meld

# -------------------
#  配置git flow
# -------------------
wget -T 10 -t 3 --no-check-certificate -q -O - https://github.com/nvie/gitflow/raw/develop/contrib/gitflow-installer.sh | bash -
rm -rf gitflow*

# -------------------
#  配置git Git Extras
# -------------------
cd /tmp && git clone --depth 1 https://github.com/visionmedia/git-extras.git && cd git-extras && make install

# -------------------
#  配置git 分支显示
# -------------------
echo "# source /etc/bash_completion.d/git
export GIT_PS1_SHOWDIRTYSTATE=true
export GIT_PS1_SHOWUNTRACKEDFILES=true
export PYTHONDONTWRITEBYTECODE=x
PS1='\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$(__git_ps1 [%s])\$ ' " >> /home/$user/.bashrc

# -------------------
#  配置GIT服务器
# -------------------
echo 'host git
  user git
  hostname git.oa.com' >> /etc/ssh/ssh_config
sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/ssh_config

# ------------------------------
# 定义mongo命令行
# ------------------------------
git clone --depth 1 https://github.com/TylerBrock/mongo-hacker.git /web/tools/mongo-hacker
cd /web/tools/mongo-hacker
make
ln -sf /web/tools/mongo-hacker/mongo_hacker.js /home/$user/.mongorc.js
chown $user.$user /home/$user/.mongorc.js

# -------------------
#   安装sun java  安装完成需要使用sudo update-alternatives --config java  选择sun jdk
# -----------------
# wget -T 10 -t 3 http://soft.oa.com/jdk-8u5-linux-x64.tar.gz
apt-get -y install default-jdk

# -------------------
#  配置pycharm开发IDE
# -----------------
mkdir -p /web/tools
if [ ! -d /web/tools/pycharm ];then
        tar jxf pycharm.tar.bz2
        rm -f pycharm.tar.bz2
        mv -f pycharm /web/tools/
fi

echo '[Desktop Entry]
Name=Pycharm
Name[zh_CN]=Pycharm网站开发工具
Encoding=UTF-8
GenericName=Pycharm
GenericName[zh_CN]=Pycharm
Comment=Pycharm Web IDE
Comment[zh_CN]=强大的web集成开发工具
X-GNOME-FullName=Pycharm Web IDE
X-GNOME-FullName[zh_CN]=Pycharm 网站开发工具
Icon=/web/tools/pycharm/bin/pycharm.png
Exec=/web/tools/pycharm/bin/pycharm.sh
Terminal=false
Type=Application
StartupNotify=true
MimeType=text/xml;application/xhtml+xml;application/x-javascript;application/x-php;application/x-java;text/x-javascript;text/html;text/plain
Categories=GNOME;Development;IDE;' > /usr/share/applications/pycharm.desktop

    ln -sf  /web/www /home/$user/$desktop/
    ln -sf  /web  /home/$user/$desktop/
    chown $user.$user -R  /web

fi

chown $user.$user -R /home/$user
chmod 777 /tmp
apt-get autoremove -y
rm -f $PWD/lxde.sh
