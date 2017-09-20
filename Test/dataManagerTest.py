from DataManagement.dataManager import dataManager

class dataManagerTest():
    def __init__(self):
        dt = dataManager()
        dt.loadData('..\\pre_kc_house_data.csv', 'price', 70)
        print 'DataFrame\n'
        print dt.dataFrame

        print '\nOutData\n'
        print dt.outputData

        print '\nInputData\n'
        print dt.inputData

if __name__ == '__main__':
    dt = dataManagerTest()