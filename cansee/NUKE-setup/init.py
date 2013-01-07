from GhClient import * 
global syspath
syspath=CGEnukePluginPath()
import sys
sys.path.append(syspath)

print '==========================='
import sys
for p in sys.path:
	print p
print '==========================='
print 'CGEsyspath:',syspath

nuke.pluginAddPath(syspath)
