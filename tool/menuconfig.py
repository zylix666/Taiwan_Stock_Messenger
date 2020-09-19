import npyscreen
import os
import configparser
from ast import literal_eval

class MenuconfigForm(npyscreen.Form):

    def _compose_output(self):
        config_local = configparser.ConfigParser()
        config_local['stocks'] = {'stock_list': self.stocks.value.split(',')}
        fields = ['close', 'change', 'shares', 'amount', 'open', 'high', 'low']
        results = ['no', 'no', 'no', 'no', 'no', 'no', 'no']
        for idx in self.result_fileds.value:
            if isinstance(idx, int):
                results[idx]='yes'

        config_local['fields'] = {fields[i]: results[i] for i in range(len(fields))}
        ext_url = ['ext_url']
        if self.ext_url.value[0] == 0:
            config_local['url'] = {'ext_url': 'yes'}
        else:
            config_local['url'] = {'ext_url':'no'}

        with open(self.dir_path + "/defconfig.ini", 'w') as configfile:
            config_local.write(configfile)
        
    def _load_defconfig(self):
        defconfig = configparser.ConfigParser()
        defconfig.read(self.dir_path + "/defconfig.ini")
        self.def_stocks = ",".join([str(elem) for elem in literal_eval(defconfig['stocks']['stock_list'])])
        def_result_fields = defconfig['fields']
        self.def_r_f_value = []
        i = 0
        for key, value in def_result_fields.items():
            if def_result_fields.getboolean(key):
                self.def_r_f_value.append(i)
            i = i+1
        self.def_ext_url = []
        if defconfig['url'].getboolean('ext_url'):
            self.def_ext_url.append(0)
        else:
            self.def_ext_url.append(1)
        #print(self.def_stocks)
        #print(self.def_r_f_value)
        #print(self.def_ext_url)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
        self._compose_output()
        #print(self.stocks.value)
        #print(self.result_fileds.value)
        #print(self.ext_url.value)

    def create(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isfile(self.dir_path + "/defconfig.ini"):
            self.stocks = self.add(npyscreen.TitleText, name='Stocks to monitor, split with comma')
            self.result_fileds = self.add(npyscreen.TitleMultiSelect, scroll_exit=True, max_height=7,
                                          name='Fields to show', values=['close', 'change','shares','amount','open','high','low'], value=[0,1])
            self.ext_url = self.add(npyscreen.TitleSelectOne, name='Add external URL', max_height=4,
                                    values=["Yes", "No"], value=[1], scroll_exit=True)
        else:
            self._load_defconfig()
            self.stocks = self.add(npyscreen.TitleText, name = 'Stocks to monitor, split with comma', value=self.def_stocks)
            self.result_fileds = self.add(npyscreen.TitleMultiSelect, scroll_text=True, max_height=7,
                                          name='Field to show', values=['close', 'change', 'shares', 'amount', 'open',
                                                                        'high', 'low'], value=self.def_r_f_value)
            self.ext_url = self.add(npyscreen.TitleSelectOne, name='Add external URL', max_height=4,
                                    values=["yes", "No"], value=self.def_ext_url)

class Menuconfig(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MenuconfigForm, name='Configuration Form')
        # A real application might define more forms here.......


if __name__ == '__main__':
    TestApp = Menuconfig().run()
