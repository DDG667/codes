def _init() -> None:
    try:
        from requests import get
        from colorama import Fore, init
    except ImportError:
        print("    检测到未安装依赖，正在自动安装中...")
        from os import system

        system("pip install --upgrade requests")
        system("pip install --upgrade colorama")
        system("clear")


_init()
from os import system
from json import loads
from requests import get
from colorama import Fore, Style

developer = """
   GitHub: Zackser
   E-mail: namddg667@gmail.com
   Telegram: DDG667
   """


class music163:
    @classmethod
    def search(self, name: str, showlen: int) -> dict:
        with get(
            f"http://music.163.com/api/search/get/?&s={name}&limit={showlen}&type=1&offset=0"
        ) as a:
            if a.status_code != 200:
                print(Fore.RED + "\t请检测网络环境后重试~")
                exit()
            print(Fore.BLUE + "\t请选择：")
            data = {}
            for num, i in zip(range(showlen), loads(a.text)["result"]["songs"]):
                id, name, artist = i["id"], i["name"], i["artists"][0]["name"]
                print(
                    f"\t{Fore.RED}{num+1} - {Fore.YELLOW}{name}  -  {Fore.BLUE}{artist}"
                )
                data[num] = [f"{name}.mp3", id]
            print(Fore.CYAN + "\t提示：使用空格多选\n")
            return data

    @classmethod
    def choose(self, data: dict):
        try:
            chooses = [int(i) for i in input("\t:  ").split()]
        except TypeError:
            print(Fore.RED + "\t请输入数字！")
            return self.choose(data)
        for choose in chooses:
            try:
                yield data[choose]
            except KeyError:
                print(Fore.RED + "\t无此id！")

    @classmethod
    def from_id_get_url(self, id: int) -> str:
        url = f"http://music.163.com/song/media/outer/url?id={id}.mp3"
        return url

    @classmethod
    def downloads(self, url: str, path: str, name: str = "") -> None:
        with open(path, "wb") as a:
            with get(url) as b:
                if b.status_code != 200:
                    print(Fore.RED + "  无法下载此音乐，请联系开发人员" + developer)
                    exit()
                a.write(b.content)
        if name != "":
            print(Fore.GREEN + f"    {name} done!")

    @classmethod
    def total(self) -> None:
        default_len = 16  # 搜索结果显示长度
        default_path = "/sdcard/Music/"  # 默认保存路径
        for naid in self.choose(
            self.search(input(Style.BRIGHT + Fore.GREEN + "  请输入音乐名称："), default_len)
        ):
            name, id = naid[0], naid[1]
            self.downloads(self.from_id_get_url(id), default_path + name, name)
        if input(Fore.GREEN + "    回车键继续，退出请输入“q”。\n    ") == "q":
            print(Fore.BLUE + "    欢迎下次使用~")
            exit()
        system("clear")
        self.total()


if __name__ == "__main__":
    try:
        music163.total()
    except Exception:
        print(f"{Fore.RED}未知错误！请联系开发人员解决：{developer}")
