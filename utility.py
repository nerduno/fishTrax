from PyQt4 import QtGui
import datatime

def obtainDate(prompt):
    isValid=False
    while not isValid:
        userIn, ok = QtGui.QInputDialog.getText(None, 'Enter date', prompt+'(format mm/dd/yy)')
        if not ok: return None
        try: # strptime throws an exception if the input doesn't match the pattern
            userIn = str(userIn);
            userDate = datetime.datetime.strptime(userIn, "%m/%d/%y")
            isValid=True
        except:
            pass
    return userDate.date()  
