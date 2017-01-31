from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='CloudMesh',
                                 moduleName='cloudmeshgui',
                                 functionName='run_gui()',
                                 author='Damian Holuj',
                                 description='#1 Attemps')