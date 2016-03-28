from subprocess import Popen  
import os
Popen(u'cmd /k %s/cmdgui/tmp.cmd' % os.getcwd(), universal_newlines=True,shell=True)