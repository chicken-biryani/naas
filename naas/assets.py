from .types import t_static
from .manager import Manager
import os


class Assets:
    naas = None
    role = t_static

    def __init__(self):
        self.manager = Manager()

    def current_raw(self):
        json_data = self.manager.get_naas()
        for item in json_data:
            if item["type"] == self.role:
                print(item)

    def currents(self):
        json_data = self.manager.get_naas()
        for item in json_data:
            kind = None
            if item["type"] == self.role:
                kind = f"publicly gettable with this url {self.manager.proxy_url('static', item['value'])}"
                print(f"File ==> {item['path']} is {kind}")

    def get(self, path=None):
        if not self.manager.notebook_path():
            print("No get done you are in already in naas folder\n")
            return
        current_file = self.manager.get_path(path)
        self.manager.get_prod(current_file)

    def get_history(self, histo, path=None):
        if not self.manager.notebook_path():
            print("No get history done you are in already in naas folder\n")
            return
        current_file = self.manager.get_path(path)
        self.manager.get_history(current_file, histo)

    def list_history(self, path=None):
        current_file = self.manager.get_path(path)
        self.manager.list_history(current_file)

    def clear_history(self, path=None, histo=None):
        if not self.manager.notebook_path():
            print("No clear history done you are in already in naas folder\n")
            return
        current_file = self.manager.get_path(path)
        self.manager.clear_history(current_file, histo)

    def add(self, path=None, params={}, debug=False, Force=False):
        current_file = self.manager.get_path(path)
        if current_file is None:
            print("Missing file path in prod mode")
            return
        prod_path = self.manager.get_prod_path(current_file)
        token = self.manager.get_value(prod_path, self.role)
        if token is None or Force is True:
            token = os.urandom(30).hex()
        url = self.manager.proxy_url("assets", token)
        if not self.manager.notebook_path() and Force is False:
            print("No add done you are in already in naas folder\n")
            return url
        print("👌 Well done! Your Assets has been sent to production folder.\n")
        print(f"🔗 You can access this assets remotely with: {url} \n")
        self.manager.copy_url(url)
        print(
            'PS: to remove the "Notebook as API" feature, just replace .add by .delete'
        )
        self.manager.add_prod(
            {"type": self.role, "path": current_file, "params": params, "value": token},
            not debug,
        )
        return url

    def delete(self, path=None, all=False, debug=False):
        if not self.manager.notebook_path():
            print("No delete done you are in already in naas folder\n")
            return
        current_file = self.manager.get_path(path)
        self.manager.del_prod({"type": self.role, "path": current_file}, not debug)
        if all is True:
            self.manager.clear_history(current_file)
            self.manager.clear_output(current_file)

    def help(self):
        print(f"=== {type(self).__name__} === \n")
        print(
            f".add(path, params) => add path to the prod {type(self).__name__} server\n"
        )
        print(
            f".delete(path) => delete path to the prod {type(self).__name__} server\n"
        )
        print(
            ".clear_history(path, histonumber) => clear history, history number and path are optionel, \
                if you don't provide them it will erase full history of current file \n"
        )
        print(
            ".list_history(path) => list history, of a path or if not provided the current file \n"
        )
        print(
            ".get_history(path, histonumber) => get history file, of a path or if not provided the current file \n"
        )
        print(
            ".get(path) => get current prod file of a path, or if not provided the current file \n"
        )
        print(f".currents() => get current list of {type(self).__name__} prod file\n")
        print(
            f".current_raw() => get json current list of {type(self).__name__} prod file\n"
        )
