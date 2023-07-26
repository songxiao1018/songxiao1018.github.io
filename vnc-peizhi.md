---
title: linux中配置vnc登录
date: 2022-10-18 19:12:12
tags: 
    - VNC
    - GUI
categories: 
    - 系统
---
debian vnc 配置

介绍 (Introduction)
Virtual Network Computing, or VNC, is a connection system that allows you to use your keyboard and mouse to interact with a graphical desktop environment on a remote server. It makes managing files, software, and settings on a remote server easier for users who are not yet comfortable with the command line.

虚拟网络计算 (VNC)是一种连接系统，使您可以使用键盘和鼠标与远程服务器上的图形桌面环境进行交互。 对于尚不熟悉命令行的用户，它使在远程服务器上管理文件，软件和设置更加容易。

In this guide, you’ll set up a VNC server on a Debian 10 server and connect to it securely through an SSH tunnel. You’ll use TightVNC, a fast and lightweight remote control package. This choice will ensure that our VNC connection will be smooth and stable even on slower internet connections.

在本指南中，您将在Debian 10服务器上设置VNC服务器，并通过SSH隧道安全地连接到该服务器。 您将使用TightVNC ，这是一种快速，轻便的远程控制程序包。 此选择将确保即使在较慢的Internet连接上，我们的VNC连接也将保持平稳。

先决条件 (Prerequisites)
To complete this tutorial, you’ll need:

要完成本教程，您需要：

One Debian 10 server set up by following the Debian 10 initial server setup guide, including a non-root user with sudo access and a firewall.

按照Debian 10初始服务器设置指南设置一台Debian 10服务器，包括具有sudo访问权限和防火墙的非root用户。

On Windows, you can use TightVNC, RealVNC, or UltraVNC.

在Windows上，可以使用TightVNC ， RealVNC或UltraVNC 。

On macOS, you can use the built-in Screen Sharing program, or can use a cross-platform app like RealVNC.

在macOS上，您可以使用内置的屏幕共享程序，也可以使用RealVNC之类的跨平台应用程序。

On Linux, you can choose from many options, including vinagre, krdc, RealVNC, or TightVNC.

在Linux上，可以从许多选项中进行选择，包括vinagre ， krdc ， RealVNC或TightVNC 。

步骤1 —安装桌面环境和VNC服务器 (Step 1 — Installing the Desktop Environment and VNC Server)
By default, a Debian 10 server does not come with a graphical desktop environment or a VNC server installed, so we’ll begin by installing those. Specifically, we will install packages for the latest Xfce desktop environment and the TightVNC package available in the official Debian repository.

默认情况下，Debian 10服务器未安装图形桌面环境或VNC服务器，因此我们将从安装它们开始。 具体来说，我们将为最新的Xfce桌面环境安装软件包，并在Debian官方存储库中提供TightVNC软件包。

On your server, update your list of packages:

在您的服务器上，更新软件包列表：

sudo apt update
sudo apt更新
Now install the Xfce desktop environment on your server:

现在，在您的服务器上安装Xfce桌面环境：

sudo apt install xfce4 xfce4-goodies
sudo apt安装xfce4 xfce4-goodies
During the installation, you’ll be prompted to select your keyboard layout from a list of possible options. Choose the one that’s appropriate for your language and press Enter. The installation will continue.

在安装过程中，系统会提示您从可能的选项列表中选择键盘布局。 选择适合您的语言的一种，然后按Enter 。 安装将继续。

Once the installation completes, install the TightVNC server:

安装完成后，安装TightVNC服务器：

sudo apt install tightvncserver
sudo apt安装tightvncserver
To complete the VNC server’s initial configuration after installation, use the vncserver command to set up a secure password and create the initial configuration files:

要在安装后完成VNC服务器的初始配置，请使用vncserver命令设置安全密码并创建初始配置文件：

vncserver
vncserver
You’ll be prompted to enter and verify a password to access your machine remotely:

系统将提示您输入并验证密码以远程访问您的计算机：

 
   
    Output
   You will require a password to access your desktops.
 
Password:
Verify:
The password must be between six and eight characters long. Passwords more than 8 characters will be truncated automatically.

密码长度必须介于六到八个字符之间。 超过8个字符的密码将被自动截断。

Once you verify the password, you’ll have the option to create a a view-only password. Users who log in with the view-only password will not be able to control the VNC instance with their mouse or keyboard. This is a helpful option if you want to demonstrate something to other people using your VNC server, but this isn’t required.

验证密码后，您可以选择创建仅查看密码。 使用仅查看密码登录的用户将无法使用其鼠标或键盘来控制VNC实例。 如果您想向使用VNC服务器的其他人演示某些内容，这是一个有用的选项，但这不是必需的。

The process then creates the necessary default configuration files and connection information for the server:

然后，该过程为服务器创建必要的默认配置文件和连接信息：

 
   
    Output
   Would you like to enter a view-only password (y/n)? n
xauth:  file /home/sammy/.Xauthority does not exist
 
New 'X' desktop is your_hostname:1
 
Creating default startup script /home/sammy/.vnc/xstartup
Starting applications specified in /home/sammy/.vnc/xstartup
Log file is /home/sammy/.vnc/your_hostname:1.log
Now let’s configure the VNC server.

现在，让我们配置VNC服务器。

步骤2 —配置VNC服务器 (Step 2 — Configuring the VNC Server)
The VNC server needs to know which commands to execute when it starts up. Specifically, VNC needs to know which graphical desktop it should connect to.

VNC服务器启动时需要知道要执行哪些命令。 具体来说，VNC需要知道它应该连接到哪个图形桌面。

These commands are located in a configuration file called xstartup in the .vnc folder under your home directory. The startup script was created when you ran the vncserver command in the previous step, but we’ll create our own to launch the Xfce desktop.

这些命令位于主目录下.vnc文件夹中名为xstartup的配置文件中。 在上一步中运行vncserver命令时创建了启动脚本，但是我们将创建自己的脚本来启动Xfce桌面。

When VNC is first set up, it launches a default server instance on port 5901. This port is called a display port, and is referred to by VNC as :1. VNC can launch multiple instances on other display ports, like :2, :3, and so on.

首次设置VNC时，它将在端口5901上启动默认服务器实例。 此端口称为显示端口 ，VNC将该端口称为:1 。 VNC可以在其他显示端口上启动多个实例，例如:2 ， :3等。

Because we are going to be changing how the VNC server is configured, first stop the VNC server instance that is running on port 5901 with the following command:

因为我们将要更改VNC服务器的配置方式，所以首先使用以下命令停止在端口5901上运行的VNC服务器实例：

vncserver -kill :1
vncserver -kill：1
The output should look like this, although you’ll see a different PID:

输出将看起来像这样，尽管您将看到一个不同的PID：

 
   
    Output
   Killing Xtightvnc process ID 17648
Before you modify the xstartup file, back up the original:

在修改xstartup文件之前，请备份原始文件：

mv ~/.vnc/xstartup ~/.vnc/xstartup.bak
mv〜/ .vnc / xstartup〜/ .vnc / xstartup.bak
Now create a new xstartup file and open it in your text editor:

现在创建一个新的xstartup文件，并在文本编辑器中将其打开：

nano ~/.vnc/xstartup
纳米〜/ .vnc / xstartup
Commands in this file are executed automatically whenever you start or restart the VNC server. We need VNC to start our desktop environment if it’s not already started. Add these commands to the file:

每当启动或重新启动VNC服务器时，该文件中的命令就会自动执行。 如果尚未启动桌面环境，我们需要VNC来启动它。 将以下命令添加到文件中：

~/.vnc/xstartup
〜/ .vnc / xstartup
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
The first command in the file, xrdb $HOME/.Xresources, tells VNC’s GUI framework to read the user’s .Xresources file. .Xresources is where a user can make changes to certain settings for the graphical desktop, like terminal colors, cursor themes, and font rendering. The second command tells the server to launch Xfce, which is where you will find all of the graphical software that you need to comfortably manage your server.

文件中的第一个命令xrdb $HOME/.Xresources告诉VNC的GUI框架读取用户的.Xresources文件。 用户可以在.Xresources中更改图形桌面的某些设置，例如终端颜色，光标主题和字体渲染。 第二个命令告诉服务器启动Xfce，在这里您将找到轻松管理服务器所需的所有图形软件。

To ensure that the VNC server will be able to use this new startup file properly, we’ll need to make it executable.

为了确保VNC服务器能够正确使用此新启动文件，我们需要使其成为可执行文件。

sudo chmod +x ~/.vnc/xstartup
须藤chmod + x〜/ .vnc / xstartup
Now, restart the VNC server.

现在，重新启动VNC服务器。

vncserver
vncserver
You’ll see output similar to this:

您将看到类似于以下的输出：

 
   
    Output
   New 'X' desktop is your_hostname:1
 
Starting applications specified in /home/sammy/.vnc/xstartup
Log file is /home/sammy/.vnc/your_hostname:1.log
With the configuration in place, let’s connect to the server from our local machine.

完成配置后，让我们从本地计算机连接到服务器。

步骤3 —安全地连接VNC桌面 (Step 3 — Connecting the VNC Desktop Securely)
VNC itself doesn’t use secure protocols when connecting. We’ll use an SSH tunnel to connect securely to our server, and then tell our VNC client to use that tunnel rather than making a direct connection.

连接时，VNC本身不使用安全协议。 我们将使用SSH隧道安全地连接到我们的服务器，然后告诉我们的VNC客户端使用该隧道，而不是直接建立连接。

Create an SSH connection on your local computer that securely forwards to the localhost connection for VNC. You can do this via the terminal on Linux or macOS with the following command:

在本地计算机上创建一个SSH连接，该连接安全地转发到VNC的localhost连接。 您可以使用以下命令通过Linux或macOS上的终端执行此操作：

ssh -L 5901:127.0.0.1:5901 -C -N -l sammy your_server_ip

ssh -L 5901 ：127.0.0.1： 5901 -C -N -l sammy your_server_ip

The -L switch specifies the port bindings. In this case we’re binding port 5901 of the remote connection to port 5901 on your local machine. The -C switch enables compression, while the -N switch tells ssh that we don’t want to execute a remote command. The -l switch specifies the remote login name.

-L开关指定端口绑定。 在这种情况下，我们绑定端口5901的远程连接端口5901在本地机器上。 -C开关启用压缩，而-N开关告诉ssh我们不想执行远程命令。 -l开关指定远程登录名。

Remember to replace sammy and your_server_ip with your non-root username and the IP address of your server.

请记住用非root用户名和服务器的IP地址替换sammy和your_server_ip 。

If you are using a graphical SSH client, like PuTTY, use your_server_ip as the connection IP, and set localhost:5901 as a new forwarded port in the program’s SSH tunnel settings.

如果使用的是图形SSH客户端(如PuTTY)，请使用your_server_ip作为连接IP，并在程序的SSH隧道设置中将localhost:5901设置为新的转发端口。

Once the tunnel is running, use a VNC client to connect to localhost:5901. You’ll be prompted to authenticate using the password you set in Step 1.

隧道运行后，使用VNC客户端连接到localhost:5901 。 系统将提示您使用在步骤1中设置的密码进行身份验证。

Once you are connected, you’ll see the default Xfce desktop.

建立连接后，您将看到默认的Xfce桌面。

Select Use default config to configure your desktop quickly.

选择“ 使用默认配置”以快速配置您的桌面。

You can access files in your home directory with the file manager or from the command line, as seen here:

您可以使用文件管理器或从命令行访问主目录中的文件，如下所示：

On your local machine, press CTRL+C in your terminal to stop the SSH tunnel and return to your prompt. This will disconnect your VNC session as well.

在本地计算机上，在终端中按CTRL+C停止SSH隧道并返回到提示符。 这也将断开您的VNC会话。

Next let’s set up the VNC server as a service.

接下来，我们将VNC服务器设置为服务。

步骤4 —将VNC作为系统服务运行 (Step 4 — Running VNC as a System Service)
Next, we’ll set up the VNC server as a systemd service so we can start, stop, and restart it as needed, like any other service. This will also ensure that VNC starts up when your server reboots.

接下来，我们将VNC服务器设置为系统服务，以便可以像其他任何服务一样根据需要启动，停止和重新启动它。 这还将确保在服务器重新引导时VNC启动。

First, create a new unit file called /etc/systemd/system/vncserver@.service using your favorite text editor:

首先，使用您喜欢的文本编辑器创建一个名为/etc/systemd/system/vncserver@.service的新单元文件：

sudo nano /etc/systemd/system/vncserver@.service
须藤纳米/etc/systemd/system/vncserver@.service
The @ symbol at the end of the name will let us pass in an argument we can use in the service configuration. We’ll use this to specify the VNC display port we want to use when we manage the service.

名称末尾的@符号将使我们传递可在服务配置中使用的参数。 我们将使用它来指定我们在管理服务时要使用的VNC显示端口。

Add the following lines to the file. Be sure to change the value of User, Group, WorkingDirectory, and the username in the value of PIDFILE to match your username:

将以下行添加到文件中。 确保在PIDFILE的值中更改User ， Group ， WorkingDirectory和用户名的值以匹配您的用户名：

/etc/systemd/system/vncserver@.service
/etc/systemd/system/vncserver@.service
[Unit]
Description=Start TightVNC server at startup
After=syslog.target network.target
 
[Service]
Type=forking
User=sammy
Group=sammy
WorkingDirectory=/home/sammy
 
PIDFile=/home/sammy/.vnc/%H:%i.pid
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :%i
ExecStop=/usr/bin/vncserver -kill :%i
 
[Install]
WantedBy=multi-user.target

The ExecStartPre command stops VNC if it’s already running. The ExecStart command starts VNC and sets the color depth to 24-bit color with a resolution of 1280x800. You can modify these startup options as well to meet your needs.

如果ExecStartPre命令已经在运行，它将停止它。 ExecStart命令启动VNC并将颜色深度设置为24位颜色，分辨率为1280x800。 您也可以修改这些启动选项，以满足您的需求。

Save and close the file.

保存并关闭文件。

Next, make the system aware of the new unit file.

接下来，使系统知道新的单位文件。

sudo systemctl daemon-reload
sudo systemctl守护进程重新加载
Enable the unit file.

启用单位文件。

sudo systemctl enable vncserver@1.service
sudo systemctl启用vncserver@1.service
The 1 following the @ sign signifies which display number the service should appear over, in this case the default :1 as was discussed in Step 2..

@符号后的1表示服务应显示在哪个显示号上，在这种情况下，默认值:1如步骤2所述。

Stop the current instance of the VNC server if it’s still running.

如果VNC服务器的当前实例仍在运行，请停止它。

vncserver -kill :1
vncserver -kill：1
Then start it as you would start any other systemd service.

然后像启动其他任何systemd服务一样启动它。

sudo systemctl start vncserver@1
sudo systemctl启动vncserver @ 1
You can verify that it started with this command:

您可以验证它是否使用以下命令启动：

sudo systemctl status vncserver@1
sudo systemctl状态vncserver @ 1
If it started correctly, the output should look like this:

如果正确启动，则输出应如下所示：

 
   
    Output
   ● vncserver@1.service - Start TightVNC server at startup
   Loaded: loaded (/etc/systemd/system/vncserver@.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2019-10-10 17:56:17 UTC; 5s ago
  Process: 935 ExecStartPre=/usr/bin/vncserver -kill :1 > /dev/null 2>&1 (code=exited, status=2)
  Process: 940 ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :1 (code=exited, status=0/SUCCESS)
 Main PID: 948 (Xtightvnc)
. . .
Your VNC server will now be available when you reboot the machine.

重新启动计算机后，您的VNC服务器现在将可用。

Start your SSH tunnel again:

再次启动SSH隧道：

ssh -L 5901:127.0.0.1:5901 -C -N -l sammy your_server_ip

ssh -L 5901 ：127.0.0.1： 5901 -C -N -l sammy your_server_ip

Then make a new connection using your VNC client software to localhost:5901 to connect to your machine.

然后使用您的VNC客户端软件与localhost:5901建立新连接，以连接到您的计算机。

结论 (Conclusion)
You now have a secured VNC server up and running on your Debian 10 server. Now you’ll be able to manage your files, software, and settings with an easy-to-use and familiar graphical interface, and you’ll be able to run graphical software like web browsers remotely.

现在，您已在Debian 10服务器上启动并运行了安全的VNC服务器。 现在，您将可以使用易于使用且熟悉的图形界面来管理文件，软件和设置，并且可以远程运行Web浏览器等图形软件。

翻译自: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-debian-10

debian vnc 配置