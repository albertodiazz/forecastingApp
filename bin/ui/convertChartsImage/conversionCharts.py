from bin import pd,plt
from bin import constant as c

class conversionChartsImagenes:
    def __init__(self):
        return
        
    def saveImage(self,saveChart,name):
        path = c.UIINFORMES
        saveChart.savefig(path + name + '.png', bbox_inches='tight')
        plt.close()
        print('Save Image',name)
        return


