from typing import List


class Choice:
	def __init__(self, text, score):
		self.score = score
		self.text = text


class Question(object):
	def __init__(self, text, choices, prerequisites: List = None):
		self.text = text
		self.choices = choices
		self.prerequisites = prerequisites


def getQuestions():
	group1 = [
		Question('这份问卷里有的问题你不会做，你应该',
				 [
					 Choice('询问管理员', 0),
					 Choice('询问王璐', 6),
					 Choice('询问吴泽伟', 6),
					 Choice('查看项目主页的文档和<a href="http://aha.ipm.edu.mo" target="_blank">http://aha.ipm.edu.mo</a>', 10)
				 ]),
		Question('你用的SHELL是？（此后，本问卷用SHELL指代BASH或Z SHELL）',
				 [Choice('BASH，它的文档在<a href="https://www.gnu.org/software/bash/manual/" target="_blank">https://www.gnu.org/software/bash/manual/</a>', 10),
				  Choice('Z SHELL，它的文档在<a href="https://zsh.sourceforge.io/Doc/" target="_blank">https://zsh.sourceforge.io/Doc/</a>', 10)]),
	]

	questions = group1 + [
		Question('服务器运行的操作系统是', [Choice('Windows', 0), Choice('Ubuntu', 10), Choice('命令行', 0), Choice('CentOS', 5)], group1),
		Question('你不知道如何让conda列出当前环境安装的包，你应该', [
			Choice('发微信给管理员询问', 0),
			Choice('在Google搜索"conda列出当前环境安装的包"', 8),
			Choice('在该链接查找 https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html', 10),
			Choice('在服务器命令行输入conda --help', 10)
		], group1),
		Question('SPLENDOR_LEVEL=2 python alnet.py `pwd`/../config 在这段代码里，你不知道SPLENDOR_LEVEL=2的意思，你应该', [
			Choice('查《牛津高阶英汉双解词典》', 2),
			Choice('发微信给管理员询问', 0),
			Choice('查Python文档', 10),
			Choice('查alnet.py和相关文件的源代码', 10),
		], group1),
		Question('SPLENDOR_LEVEL=2 python alnet.py `pwd`/../config 在这段代码里，你不知道`的意思，你应该', [
			Choice('在Google搜索`', 0),
			Choice('发微信给管理员询问', 0),
			Choice('查Python文档', 0),
			Choice('查看SHELL文档', 10),
		], group1),
		Question('SPLENDOR_LEVEL=2 python alnet.py `pwd`/../config 在这段代码里，你不知道pwd的意思，你应该', [
			Choice('在Google搜索pwd', 8),
			Choice('发微信给管理员询问', 0),
			Choice('查看SHELL文档', 10),
			Choice('在这个链接查找 http://manpages.ubuntu.com', 10),
		], group1),
		Question('哪个ls的option只存在于在Ubuntu 20.04标准版、而不在20.04 Posix版和20.04 Plan9版',
				 [Choice('-Z', 10), Choice('-d', 0), Choice('-u', 0), Choice('-R', 0)]),
		Question('哪个grep的option只存在于Ubuntu 18.04或22.04（而非都有）', [Choice('--no-ignore-case', 10), Choice('--only-matching', 0), Choice('--fixed-strings', 0), Choice('-H', 0)], group1),
		Question('你不知道sit的用法，你应该', [
			Choice('发微信给管理员询问', 0),
			Choice('在Google搜索sit', 1),
			Choice('查看slurm文档 https://slurm.schedmd.com', 1),
			Choice('查看mpi-server主页或文档', 10)
		], group1),
		Question('你不知道sbatch的用法，你应该', [
			Choice('发微信给管理员询问', 0),
			Choice('在Google搜索sbatch', 8),
			Choice('查看slurm文档 https://slurm.schedmd.com', 10),
			Choice('查看mpi-server主页或文档', 7)
		], group1),
		Question('你修改了yolov5的代码，在你的机器上跑没事，在服务器上跑就出错了，你应该', [
			Choice('发微信给管理员询问', 0),
			Choice('在mpi-server主页搜索issues，如果别人没这个问题，就创建一个新issue', 10),
			Choice('在服务器上调试', 10),
			Choice('在yolov5的主页搜索issues，如果别人没这个问题，就创建一个新issue', 10),
		], group1),
		Question('你想要用squeue --json，但在服务器上出错了，你应该', [
			Choice('发微信给管理员询问', 0),
			Choice('在mpi-server主页搜索issues，如果别人没这个问题，就创建一个新issue', 10),
			Choice('在服务器上输入 man squeue 查看文档', 10),
			Choice('检查服务器的slurm版本', 10)
		], group1),
		Question('在服务器上你想要安装go语言编译器，你应该', [
			Choice('发微信给管理员，要他安装', 0),
			Choice('在mpi-server主页搜索issues，如果没有类似issue，就创建一个新issue', 10),
			Choice('在自己的家目录安装', 10),
			Choice('改用自己电脑做实验', 10)
		], group1),
		Question('下列哪种情况下可以给管理员发微信', [
			Choice('跟管理员约会', 10),
			Choice('服务器登陆不了', 6),
			Choice('把一个小文件传给管理员', 1),
			Choice('发现了一个服务器上的安全漏洞', 10)
		], group1),
		Question('以下关于服务器的叙述哪个是错的？', [
			Choice('服务器上不能运行带有图形界面的程序', 10),
			Choice('RaiDrive有可能让你无法连接服务器', 0),
			Choice('AHA节点不能运行计算任务', 0),
			Choice('mpi-server有计划限制我可以提交的slurm任务数量，但目前还没有。目前的任务限制是slurm本身的限制。', 0)], group1),
		Question('你在用的Bash版本是2.0.13.14，而最新的Bash版本已经到5.x了。你要查一些Bash的用法，你应该', [
			Choice('bash的功能一直以来没什么改变，在Google搜索，搜到的东西大致上是可以用的', 5),
			Choice('在 https://www.gnu.org/software/bash/manual/ 查看官方文档', 6),
			Choice('输入man bash查看文档', 10),
			Choice('在 http://ftp.gnu.org/gnu/bash/ 下载对应版本的源代码', 10)
		], group1),
		Question('关于mpi-servers的github主页，以下哪项是错的？', [
			Choice('管理员虽然可以直接提交代码，但是发起pull request可增加透明性，让其他人帮忙检查错误', 0),
			Choice('我们普通用户只能用pull request的方式提交代码', 0),
			Choice('我们普通用户最好先问过管理员，再创建issue', 10),
			Choice('写issue可以用中文', 0)
		], group1),
		Question('以下哪项编程原则比其他几项更重要？', [Choice('DRY', 10), Choice('WET', 0), Choice('SRP', 10), Choice('Document Your Code', 10), Choice('Fast Beats Right', 0)], group1),
		Question('以下哪项是“高效”使用shine集群的必要条件', [
			Choice('有Google账号', 0), Choice('有微信账号', 0), Choice('有百度账号', 0), Choice('有GitHub账号', 10)
		], group1),
		Question('用FinalShell无法连接服务器，或出了一些毛病，你第一步应该', [
			Choice('加入FinalShell微信群去提问', 6),
			Choice('在项目主页提出issue', 5),
			Choice('因为项目主页wiki只使用Putty演示，所以改用Putty看看还有没有问题', 10),
			Choice('询问管理员', 0),
		], group1),
		Question('用PyCharm无法连接服务器，或出了一些毛病，你第一步应该', [
			Choice('加入PyCharm微信群去提问', 6),
			Choice('在项目主页提出issue', 5),
			Choice('因为项目主页wiki只使用Putty演示，所以改用Putty看看还有没有问题', 10),
			Choice('询问管理员', 0),
		], group1),
		Question('你用RaiDrive把远程服务器上的文件映射到Windows本地，你在Windows双击一个10GB的文本文件，用记事本打开，电脑似乎卡住了。以下哪项叙述是对的？', [
			Choice('文件太大了，不管在哪用什么打开都不好使。', 1),
			Choice('记事本太烂了，在Windows用Notepad++或VS Code会好一点', 1),
			Choice('RaiDrive正在把10GB的文件传输到本地，所以要等待久一点文件才能打开。', 10),
			Choice('在远程服务器上用不带插件的Vim可以瞬间打开该文件', 10),
		], group1),
		Question('你用RaiDrive把远程服务器上的文件映射到Windows本地，你在Windows双击一个压缩文件，用WinRAR解压缩，电脑似乎卡住了。以下哪项叙述是错的？', [
			Choice('通过该方法解压缩出来的文件里的x位（可执行位）不能被正确处理。', 0),
			Choice('WinRAR太烂了，用7zip或好压会好一点', 10),
			Choice('WinRAR需要远程读取该压缩文件，再把解压缩出来的文件远程写回服务器，所以慢。', 0),
			Choice('RaiDrive效率低，用SSHFS会好一点', 0),
		], group1),
		Question('在Windows上，Putty是唯一受mpi-server支持的SSH客户端。在Linux上，以下哪个是唯一受支持的SSH客户端？', [
			Choice('OpenSSH', 9),
			Choice('Putty', 0),
			Choice('没有', 10),
			Choice('Windows Terminal', 0),
		], group1),
	]

	return questions
