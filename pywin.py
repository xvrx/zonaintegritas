from csv import excel
from inspect import getmodulename
from socket import timeout
import time
from pywinauto.application import Application
import os

# firefox = "excel.exe"

# app = Application(backend="uia").start(firefox)
# describe the window inside Notepad.exe process
# dlg_spec = app.NewTab
# wait till the window is really open
# actionable_dlg = dlg_spec.wait("visible")


# start() is used when the application is not running and you need to start it. Use it in the following way:
# excelApp = Application().start(r"c:\path\to\your\application -a -n -y --arguments")
# excelApp = Application().start(
#     r"C:/Users/Rustacean/Desktop/eform_laknatulloh/sample.xlsx -a -n -y --arguments"
# )


from subprocess import Popen
from pywinauto import Desktop

# run other than executable

# find pid
execFile = "C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\\AcroRd32.exe"
pdfFIle = "FORM_1770_78458215444815712000_2021_0.pdf"

# app.print_control_identifiers()
app = Application(backend="uia").start(f"{execFile} {pdfFIle}")
time.sleep(2)
mainWdw = app.connect(
    class_name="AcrobatSDIWindow", top_level_only=False
).wrapper_object()
mainWdw.print_control_identifiers()
