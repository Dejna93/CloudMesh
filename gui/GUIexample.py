from Tkinter import *
from abaqus import *
from abaqusConstants import *
import matplotlib

def testFunction():
     def close_window():
         master.destroy()

     def steel():
         pass
         mdb.models['Model-1'].Material('AISI 1005 Steel')
         mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872,),))
         mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29),))

     def titanium():
         pass
         mdb.models['Model-1'].Material('Titanium')
         mdb.models['Model-1'].materials['Titanium'].Density(table=((4500,),))
         mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3),))

     master = Tk()

     v = IntVar()

     Radiobutton(master, text="steel", variable=v, value=1, command=steel).pack(anchor=W)

     Radiobutton(master, text="titanium", variable=v, value=2, command=titanium).pack(anchor=W)

     frame = Frame(master)
     frame.pack()
     button = Button(frame, text="test-close", command=close_window)
     button.pack()

     mainloop()