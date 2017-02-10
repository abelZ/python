import random, sys, time, socket, os
from termcolor import colored
import colorama
import threading
from multiprocessing import freeze_support
import winsound, ctypes
import win32gui

import abel_window, abel_xiu, abel_wild, abel_nao

xiu_task = abel_xiu.xy2_xiu()
wild_task = abel_wild.xy2_wild()
nao_task = abel_nao.xy2_nao(number=5)
def xiu_thread():
    global xiu_task
    xiu_task.run_task()

def wild_thread():
    global wild_task
    wild_task.run_task()

def nao_thead():
    global nao_task
    nao_task.run_task()

def server_thread(task_type, ip):
    global wild_task
    global xiu_task
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 10088
    serversocket.bind((str(ip), port))
    serversocket.listen(5)
    while True:
        clientsocket,addr = serversocket.accept()
        if task_type == '-wild':
            clientsocket.send(wild_task.role_status.encode('ascii'))
        elif task_type == '-xiu':
            clientsocket.send(xiu_task.role_status.encode('ascii'))
        clientsocket.close()
    serversocket.close()

def client_thread(task_type):
    while True:
        role_status = None
        if task_type == '-wild':
            role_status = wild_task.role_status
        elif task_type == '-xiu':
            role_status = xiu_task.role_status
        elif task_type == '-nao':
            role_status = nao_task.role_status
        else:
            role_status = ''
        if role_status == abel_window.s_not_in_team:
            winsound.PlaySound('.\\resource\\leader_leave.wav', winsound.SND_FILENAME)
            print 'your leader has been leaved the team, please find another one'
        elif role_status == abel_window.s_not_moved:
            winsound.PlaySound('.\\resource\\not_moved.wav', winsound.SND_FILENAME)
            print 'your leader has been not moved more than two minutes, please check'
        time.sleep(10)

def check_status(status, value, i):
    if status != value:
        if status != -1:
            print ''
        return 1
    else:
        return i + 1

def monitor_thead(ip):
    i = 1
    status = -1
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 10088
            s.connect((str(ip), port))
            tm = s.recv(1024)
            if tm.decode('ascii') == abel_window.s_not_in_team:
                winsound.PlaySound('.\\resource\\leader_leave.wav', winsound.SND_FILENAME)
                i = check_status(status, 0, i)
                text = '\rleaving%d...' % i
                sys.stdout.write(text)
                sys.stdout.flush()
                status = 0
            elif tm.decode('ascii') == abel_window.s_not_moved:
                winsound.PlaySound('.\\resource\\not_moved.wav', winsound.SND_FILENAME)
                i = check_status(status, 1, i)
                text = '\rstilling%d...' % i
                sys.stdout.write(text)
                sys.stdout.flush()
                status = 1
            else:
                i = check_status(status, 2, i)
                text = colored('\rnormaling...', 'green')
                sys.stdout.write(text)
                sys.stdout.flush()
                status = 2
                s.close()
        except:
            i = check_status(status, 100, i)
            text = colored('\rconnect to %s fail' % sys.argv[2], 'red')
            sys.stdout.write(text)
            sys.stdout.flush()
            status = 100
        time.sleep(10)

def waiting():
    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            print "\nCtrl+C exit"
            break
        except:
            pass

if __name__ == '__main__':
    freeze_support()
    colorama.init()
    if len(sys.argv) >= 2 and sys.argv[1] == '-server':
        if len(sys.argv) >= 3 and sys.argv[2] == '-xiu':
            t = threading.Thread(target=xiu_thread)
            t.daemon = True
            t.start()
            if len(sys.argv) >= 4:
                ts = threading.Thread(target=server_thread, args=('-xiu', sys.argv[3],))
                ts.daemon = True
                ts.start()
            else:
                tc = threading.Thread(target=client_thread, args=('-xiu',))
                tc.daemon = True
                tc.start()
            waiting()
        elif len(sys.argv) >= 3 and sys.argv[2] == '-wild':
            t = threading.Thread(target=wild_thread)
            t.daemon = True
            t.start()
            if len(sys.argv) >= 4:
                ts = threading.Thread(target=server_thread, args=('-wild', sys.argv[3],))
                ts.daemon = True
                ts.start()
            else:
                tc = threading.Thread(target=client_thread, args=('-wild',))
                tc.daemon = True
                tc.start()
            waiting()
        elif len(sys.argv) >= 3 and sys.argv[2] == '-nao':
            t = threading.Thread(target=nao_thead)
            t.daemon = True
            t.start()
            tc = threading.Thread(target=client_thread, args=('-nao',))
            tc.daemon = True
            tc.start()
            waiting()
        elif len(sys.argv) >= 3 and sys.argv[2] == '-pos':
            w = abel_window.WindowMgr()
            w.find_window_wildcard(".*Revision.*ID.*")
            if w._find:
                rect = win32gui.GetWindowRect(w._handle)
                x_offset = rect[0]
                y_offset = rect[1]
                cursor = win32gui.GetCursorPos()
                print cursor[0] - x_offset, cursor[1] - y_offset
        elif len(sys.argv) >= 3:
            tm = threading.Thread(target=monitor_thead, args=(sys.argv[2],))
            tm.daemon = True
            tm.start()
            waiting()
        else:
            print 'please use abel.py -server'
    else:
        print 'please use abel.py -server'
