from adb_helper import *
from tkinter import *
from tkinter import ttk,filedialog,messagebox
import qa_commander

instance = True
get_device = lambda: adb.adb_get_device() if adb.adb_get_device() else ""
master = Tk()
master.configure(bg='grey18')
listbox_count = 0

def adb_disconnect(ip=''):
    global listbox_count
    adb.set_one_device()
    if not ip:
        adb.adb_disconnect_all()
    else:
        adb.adb_disconnect_ip(ip)
    Lb1.insert(listbox_count,adb.get_status())
    listbox_count += 1
    load_tkiner_window('' if not ip else get_device(),0)

def adb_connect(ip):
    global listbox_count
    device = adb.adb_connect(ip)
    Lb1.insert(listbox_count,adb.get_status())
    listbox_count += 1
    load_tkiner_window(device if device else '', 0)

def start_qa_commander():
    global instance
    if instance:
        instance = False
        qa_commander.main()

def CurSelet(event):
    widget = event.widget
    selection=widget.curselection()
    if selection:
        picked = widget.get(selection)
        adb_disconnect(picked)

def load_tkiner_window(device,reset):
    global Lb1
    global listbox_count
    master.title("Adb Management")
    master.resizable(False, False)
    labelText = StringVar()
    labelText.set('' if not device else device[0])

    l1 = Label(master,width=50,bg='dim grey',text="Refresh Connect Device...")
    l1.bind("<Button-1>",lambda x:load_tkiner_window(get_device(),0))
    l1.grid(row=0, column=0)

    e1 = Entry(master,width=45,textvariable=labelText,state='disabled' if device else 'normal')
    e1.grid(row=1, column=0, pady=5,padx=30)

    connect = ttk.Button(master, text="Connect", width=25,state='normal' if not device else 'disabled',
                         command=lambda:adb_connect(e1.get()))
    connect.grid(row=4, column=0, pady=5, padx=5)

    submit = ttk.Button(master, text="Disconnect", width=25,state='normal' if device else 'disabled',
                        command=lambda:adb_disconnect())
    submit.grid(row=5,column=0,pady=15,padx=5)

    qa_com = ttk.Button(master, text="QA Commander", width=25, state='normal' if len(device)==1 else 'disabled',
                        command=lambda:start_qa_commander())
    qa_com.grid(row=6, column=0, pady=15, padx=5)

    device_listbox = Listbox(master, bg='grey60', height=2, width=45)
    device_listbox.grid(row=2, column=0, pady=5, padx=5)
    device_listbox.bind('<<ListboxSelect>>', CurSelet)

    i=0
    if device:
        for deviceid in adb.adb_get_device():
            device_listbox.insert(i,deviceid)
            i+=1

    if reset:
        Lb1 = Listbox(master, bg='grey60', height=5, width=45)
        Lb1.grid(row=3, column=0, pady=5, padx=5)
        Lb1.insert(listbox_count, adb.get_status())
        listbox_count += 1
        master.mainloop()

if __name__ == '__main__':

    adb = adb_helper()
    print(adb.get_status())
    load_tkiner_window(get_device(),1)