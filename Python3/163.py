from sys import argv
from os import system
from json import loads
from threading import Thread
default_len = 16  # 搜索结果显示长度
default_path = ""  # 默认保存路径，留空即为执行目录，注意加/

if default_path!='' and default_path[-1]!='/':
    default_path+='/'

developer = """
    GitHub: Zackser
    E-mail: namddg667@gmail.com
    Telegram: DDG667
    """


def _init() -> None:
    try:
        import requests, colorama
    except ImportError:
        print("    检测到未安装依赖，正在自动安装中...")
        from os import system

        if system("pip install --upgrade requests") != 0:
            if (
                input(
                    "无法通过 pip install requests 安装requests，是否重试？\n y or n ? (default is n)\n\t"
                )
                == "y"
            ):
                _init()
            else:
                print("可联系开发人员：" + developer)
                exit()
        if system("pip install --upgrade colorama") != 0:
            if input("一个花里胡哨的配色无法安装，是否取消？\n y or n ? (default is y)\n\t") == "n":
                _init()
            else:
                with open("colorama.py", "w") as a:
                    a.write(
                        'class Fore:\n\tRED=BLUE=BRIGHT=CYAN=YELLOW=GREEN=""\nclass Style:\n\tBRIGHT=""'

                    )
                global o
                if input('默认下次启动重试安装\n y or n ? (default is y)\n\t')=='n':
                    o=1
                else:
                    o=0
        else:
            o=0
        system("clear")


_init()
from requests import get
from colorama import Fore, Style


class music163:
    @classmethod
    def search(self, name: str, showlen: int) -> dict:
        try:
            a = get(
                f"http://music.163.com/api/search/get/?&s={name}&limit={showlen}&type=1&offset=0"
            )
            a.close()
            data = {
                num + 1: [i["name"], i["id"], i["artists"][0]["name"]]
                for num, i in zip(range(showlen), loads(a.text)["result"]["songs"])
            }
            return data
        except KeyError:
            print(f"{Fore.RED}\t无此音乐！\n")
            self.total()
        except ConnectionError:
            print(f"{Fore.RED}\t请检测网络环境后重试~\n")
            exit()

    @classmethod
    def choose(self, data: dict):
        print(f"{Fore.BLUE}\n\t请选择：")
        for i in data:
            print(
                f"\t  {Fore.RED}{i} - {Fore.YELLOW}{data[i][0]} - {Fore.BLUE}{data[i][2]}"
            )
        print(f"{Fore.CYAN}\t提示：使用空格多选\n")
        try:
            for cho in [int(i) for i in input("\t:  ").split()]:
                yield data[cho]
        except ValueError:
            print(f"{Fore.RED}\t请输入数字！\n")
        except KeyError:
            print(f"{Fore.RED}\t无此id！\n")

    @classmethod
    def from_id_get_url(self, id: int) -> str:
        return f"http://music.163.com/song/media/outer/url?id={id}.mp3"

    @classmethod
    def downloads(self, url: str, path: str, name: str = "") -> None:
        with get(url) as b:
            if "audio/mpeg" not in b.headers["Content-Type"]:
                print(f"{Fore.RED}  无法下载 ”{name}“ ，请联系开发人员\n{developer}")
                return None
            with open(path, "wb") as a:
                a.write(b.content)
                b.close()
        if name != "":
            print(f"{Fore.GREEN}    {name} done!")

    @classmethod
    def total(self) -> None | int:
        for naid in self.choose(
            self.search(input(f"{Style.BRIGHT}{Fore.GREEN}   请输入音乐名称："), default_len)
        ):
            name, id = naid[0], naid[1]
            t = Thread(
                target=self.downloads,
                args=(self.from_id_get_url(id), f"{default_path}{name}.mp3", name),
            )
            t.start()
            t.join()
        if input(f"{Fore.GREEN}\n   回车键继续，退出请输入“q”\n\t") == "q":
            system("clear")
            print(f"{Fore.BLUE}  欢迎下次使用~\n")
            exit()
        if o:
            system("rm colorama.py")
        system("clear")
        self.total()


if __name__ == "__main__":
    if len(argv)!=1:
        if argv[-1]=='help':
            print(f'\t{Style.BRIGHT}{Fore.GREEN}开发：{developer}QQ群：686221881')
            exit()
    try:
        music163.total()
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}  欢迎下次使用~\n")
    except Exception:
        print(f"\t{Fore.RED}未知错误！请联系开发人员解决：{developer}")

"""
QQ群：686221881
"""
