from time import time
import time
import paramiko 
from tkinter import *
import tkinter
from tkinter import scrolledtext
import requests
import logging
import datetime
from requests_ntlm import HttpNtlmAuth
from tkinter import messagebox
from bs4 import BeautifulSoup
import sys

requests.packages.urllib3.disable_warnings()

RDB_host = "rdb_host_address"

def make_menu(w):
    global the_menu
    the_menu = tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

window = Tk()
window.title("Jump server log viewer v1.4d")
make_menu(window)


login_lbl = Label(window, text="Логин абонента")
login_lbl.grid(column=2, row=2)
entry_login_abon = Entry(window,width=20,bg="#fafafa")
entry_login_abon.grid(column=3, row=2)
entry_login_abon.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

name_lbl = Label(window, text="Логин")
name_lbl.grid(column=4, row=0,sticky=W+E)
entry_name = Entry(window,width=20,bg="#fafafa")
entry_name.grid(column=5, row=0,sticky=W+E)
entry_name.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)


pass_lbl = Label(window, text="Пароль")
pass_lbl.grid(column=6, row=0,sticky=W+E)
entry_pass = Entry(window,width=20,show="*",bg="#fafafa")
entry_pass.grid(column=7, row=0,sticky=W+E)
entry_pass.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

commut_lbl = Label(window, text="Префикс коммутатора",font=('Arial', 11))
commut_lbl.grid(column=0, row=2,sticky=N+S+E+W)
entry_commutator_prefixix = Entry(window,width=20)
entry_commutator_prefixix.grid(column=1, row=2,sticky=N+S+E+W)
# entry_commutator_prefixix.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
entry_commutator_prefixix.config(state="readonly")

commut_ip_lbl = Label(window, text="IP адрес или ИМЯ коммутатора",font=('Arial', 11))
commut_ip_lbl.grid(column=0, row=3,sticky=N+S+E+W)
entry_commut_name_or_ip = Entry(window,width=20,bg="#fafafa")
entry_commut_name_or_ip.grid(column=1, row=3,sticky=N+S+E+W)
entry_commut_name_or_ip.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

port_lbl = Label(window, text="Порт абонента на коммутатора",font=('Arial', 11))
port_lbl.grid(column=0, row=4,sticky=N+S+E+W)
entry_commut_port = Entry(window,width=20,bg="#fafafa")
entry_commut_port.grid(column=1, row=4,sticky=N+S+E+W)
entry_commut_port.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)


txt = scrolledtext.ScrolledText(window, font=('Arial', 11), width=20,bg="#fafafa")
txt.grid(columnspan=9,column=0 ,row=1,sticky=N+S+E+W, pady=5, padx=5)
# txt.grid(row=0, column=5, columnspan=6, sticky=W + N + S + E, pady=5, padx=5)
txt.rowconfigure(2, weight=2)
txt.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)


user = ''
secret = ''
component_data = []

city_list = 'Minsk','Gomel',"Svetlogorsk",'Mogilev','RE',"Gatovo","Lesnoy","Borovlyany","Zhdanivichi","Brest","Bobruisk","DO","Vitebsk","VI","ZHLOBIN","ZHLOB7","ZHLOB","GO","Leskovka","NOVOPOLOTSK"
supported_commutator_list='IES','ZTEC300','OLT','OLT1','OLT2','OLT3','OLT4','OLT5','OLT6','S2995','Q3470','ZY3528','ZY3500','S2989','S2900','D5960','D5750','D4650','D4600','D3650','D3950','Z5250','Z5260','Z5900','Z5928','P2610','P2620','P2626','P2650','Z2900','D3000','D1210','A6224'
# fast_diagnostik_friendly = 'Q3470','S2995','S2989','D3950','S2900','D3650','D5750','D4650','D4600','D5960'
fast_diagnostik_friendly_code = 'DCN'

def set_data(num_menu=1):
    cdt=datetime.datetime.now()
    focus_txt = 0
    resault = ''
    resault_sup_tools = ''
    txt.insert(INSERT,'')
    host='Jump_server'
    port=22
    global user,secret
    try:
        all_sysargv = sys.argv
        user = all_sysargv[1]
        secret = all_sysargv[2]
        if len(entry_name.get())<1:
            entry_name.insert(0,f"{user}")
            entry_pass.insert(0,f"{secret}")
            
    except:
        user = entry_name.get()
        secret = entry_pass.get()

    creds = f'domain\\{user}',f'{secret}'
    aut_=HttpNtlmAuth(creds[0],creds[1])
    commut_port =  entry_commut_port.get()
    abonent_login = entry_login_abon.get()
    abonent_login = abonent_login.replace(" ","").replace("\t","").replace("\n","")
    if len(user)<1 or len(secret)<1 :
        messagebox.showerror(title="Error",message="Мб введём СВОЙ логин и пароль а потом уже будем жмякать?")
        return
    #тестовый коннект в РДБ и проверка есть ли коннект. 
    print(datetime.datetime.now(),"Выполняется тестовое подключение в RDB +")
    try:
        req_test_connect = requests.get(f"rdb_host_address:8070/",auth=aut_)
        if req_test_connect.status_code !=200:
            print(datetime.datetime.now(),"Тестовое соединение - FAIL!",req_test_connect)
            messagebox.showerror(title="Error",message="Ошибка. Невозможно авторизоваться в RDB.Проверте введенные данные (логин и пароль).")
            req_test_connect.close()
            return
        else:
            print(datetime.datetime.now(),"Тестовое соединение - успешно!",req_test_connect)
    except:
        messagebox.showerror(title="Error",message=f"Проверьте соединение с корп. сетью, отсутствует соединение с RDB")
        req_test_connect=""
        print(datetime.datetime.now(),"Тестовое соединение - неуспешно",req_test_connect)
    # #если  коннекта нет - выдаст ошибк и прекратит дальнейшеее выполнение

        return
    
    #1 этапом проверяю введен ли логин, если введен - беру информацию из логина или выдаю ошибку что таокго лоигна нет.
    if len(abonent_login)!=0:
        # print(datetime.datetime.now(),"Успешное подключение к RDB +")
        req_ServiceEquipment = requests.get(f"rdb_host_address:8070/Service/ServiceEquipment?service={abonent_login}",auth=aut_)
        resault_Login_Equipment = req_ServiceEquipment.json()#json.loads(req_ServiceEquipment.text)
        # print(datetime.datetime.now(),"resault_Login_Equipment",resault_Login_Equipment)
        print(datetime.datetime.now(),"Получение данных по логину из RDB +")
        if len(resault_Login_Equipment)<1:
            print(f"\nПо логину {abonent_login} в RDB не найдено информации, проверь корректность ввода")
            messagebox.showerror(title="Error",message=f"\nПо логину {abonent_login} в RDB не найдено информации, проверь корректность ввода и/или добавь из билнга информацию по порту в RDB\n")
            entry_commut_name_or_ip.delete(0,END)
            entry_commutator_prefixix.config(state="normal")
            entry_commutator_prefixix.delete(0,END)
            entry_commutator_prefixix.config(state="readonly")
            entry_commut_port.delete(0,END)
            return
        commut_port = resault_Login_Equipment[0].get("port")
        number_slot_on_olt = resault_Login_Equipment[0].get("number_slot_on_olt")
        port_number_in_slot = resault_Login_Equipment[0].get("port_number_in_slot")
        abon_ip = ['','']
        # print("resault_Login_Equipment[i].get(\"ip\")",resault_Login_Equipment[0].get("ip"))
        # print("resault_Login_Equipment[i].get(\"ip\")",resault_Login_Equipment[1].get("ip"))
        for i in range(len(resault_Login_Equipment)):
            abon_ip[i] = resault_Login_Equipment[i].get("ip")
        device_id = resault_Login_Equipment[0].get("device")
    
        req_Device_Parameters = requests.get(f"rdb_host_address:8070/Catalogs/Device/Parameters/{device_id}",auth=aut_)

        resault_Device_Parameters = req_Device_Parameters.json()#json.loads(req_Device_Parameters.text)
        commutator_name_or_ip = resault_Device_Parameters[0].get("ip")
        commutator_name = resault_Device_Parameters[0].get("description")
        #commutator_prefix = resault_Device_Parameters[0].get("description").split("-")[0].upper()
        #новый способ получения префикса
        commutator_prefix_list = resault_Device_Parameters[0].get("description").replace(" ","").replace("\t","").replace("\n","").upper().split("-")
        j=1
        for i in commutator_prefix_list:
            if i in supported_commutator_list:
                commutator_prefix=i
                print(datetime.datetime.now(),"Из данных получен префикс",commutator_prefix)
                break
            else:
                commutator_prefix = "not respons"
                if j == len(commutator_prefix_list):
                    print(datetime.datetime.now(),"commutator_prefix",commutator_prefix_list)
                    print(f"\nИз частей имени коммтутатора\"{commutator_prefix_list}\" не удалось получить/найти поддерживаемый префикс.\nПоддерживаемые префиксы {supported_commutator_list}")
                    messagebox.showerror(title="Error",message=f"\nИз частей имени коммтутатора\"{commutator_prefix_list}\" не удалось получить/найти поддерживаемый префикс.\nПоддерживаемые префиксы {supported_commutator_list}")
            j+=1
        if commutator_prefix == "D3000":
            #доп проверка. т.к. бывает что в имени d3000 а по факту это DCN
            if resault_Device_Parameters[0].get("code") == 'DCN':
                commutator_prefix = resault_Device_Parameters[0].get("code")
            else:
                commutator_prefix=commutator_prefix
        else:
            commutator_prefix = resault_Device_Parameters[0].get("code")
        commutator_city = resault_Device_Parameters[0].get("city")
        print(datetime.datetime.now(),"commutator_prefix полученный новым способом",commutator_prefix)
        #
        if ("unknown" in commutator_city ) or ("Unknown" in commutator_city):
            commutator_city = resault_Device_Parameters[0].get("description").split("-")[1].upper()
            #добавить префиксы городов!!
        #если город не указан в РДБ - то получать город на основании 2 слова в дескрипшине
        #
        resault+=f"\nИнформация по логину: {abonent_login}\n"
        resault+=f"Коммутатор префикс: {commutator_prefix}\n"
        
        print(datetime.datetime.now(),"На основании введеных данных commutator_name =",commutator_name)

        #проверка стоит ли отображать из рдб информацию по карду и вирутально порту
        if ("olt" in commutator_name) or ("OLT" in commutator_name):
            print(datetime.datetime.now(),"Это OLT")
            resault+=f"OLT IP: {commutator_name_or_ip}\n"
            resault+=f"Кард OLT: {number_slot_on_olt}\n"
            resault+=f"Физический порт OLT: {port_number_in_slot}\n"
            resault+=f"Виртуальный порт OLT: {commut_port}\n"
            commut_portV = commut_port
            commut_port = str(number_slot_on_olt)+'/'+str(port_number_in_slot)+'/'+str(commut_port)
        else:
            resault+=f"Коммутатор IP: {commutator_name_or_ip}\n"
            resault+=f"Порт абонента: {commut_port}\n"
            # print(datetime.datetime.now(),"Это не олт")
        resault+=f"Абонент IP (ДЛЯ СТАРОЙ СХЕМЫ!!! НЕ L2_IPOE): {abon_ip}\n"
        resault+=f"Город коммутатора: {commutator_city}\n"
        resault+="--------------------------------------------------------------------------------\n"
        if len(entry_commut_name_or_ip.get())>0 and len(entry_commutator_prefixix.get())>0 and len(entry_commut_port.get())>0:
            entry_commut_name_or_ip.delete(0,END)
            entry_commutator_prefixix.config(state="normal")
            entry_commutator_prefixix.delete(0,END)
            entry_commutator_prefixix.config(state="readonly")
            entry_commut_port.delete(0,END)
        entry_commut_port.insert(0,f"{commut_port}")
        entry_commutator_prefixix.config(state="normal")
        entry_commutator_prefixix.insert(0,f"{commutator_prefix}")
        entry_commutator_prefixix.config(state="readonly")
        if len(entry_commutator_prefixix.get()) >0:
            entry_commut_name_or_ip.delete(0,END)
        entry_commut_name_or_ip.insert(0,f"{commutator_name_or_ip}")
        txt.insert("end",resault)
    else:
        #если лоигин не введен, переходим ко 2 этапу - получаем из формы IP или имя железки
        commutator_name_or_ip = entry_commut_name_or_ip.get()
        commutator_name_or_ip = commutator_name_or_ip.replace(" ","").replace("\t","").replace("\n","")
        if (len(abonent_login)<1) and (len(commutator_name_or_ip)<1) :
            messagebox.showerror(title="Error",message="Для работы программы, необходимо ввести логин абонента или имя/IP коммутатора (+ порт)")
            return
        #если введное значение начинается с 10. - значит введен IP
        if commutator_name_or_ip.startswith("1"):
            #делаю запрос в RDB для получения из IP адреса имя/префикс/город
            respons_commutator_name_and_ip_via_IP = requests.post(f"rdb_host_address:8070/Catalogs/Device/List",auth=aut_,data={'ip': f'{commutator_name_or_ip}'})
            # print(respons_commutator_name_and_ip_via_IP.text)
            try:
                resault_Device_Parameters = respons_commutator_name_and_ip_via_IP.json()
                #старый способ получения префикс
                # commutator_prefix = ((resault_Device_Parameters[0].get("description")).upper()).split("-")[0]
                #новый способ получения префикса
                commutator_prefix_list = resault_Device_Parameters[0].get("description").replace(" ","").replace("\t","").replace("\n","").upper().split("-")
                j=1
                for i in commutator_prefix_list:
                    if i in supported_commutator_list:
                        commutator_prefix=i
                        print(datetime.datetime.now(),"commutator_prefix",commutator_prefix)
                        break
                    else:
                        if j == len(commutator_prefix_list):
                            print(datetime.datetime.now(),"commutator_prefix_list",commutator_prefix_list)
                            messagebox.showerror(title="Error",message=f"\nИз частей имени коммтутатора\"{commutator_prefix_list}\" не удалось получить/найти поддерживаемый префикс.\nПоддерживаемые префиксы {supported_commutator_list}")
                    j+=1
                if commutator_prefix == "D3000":
                    commutator_prefix=commutator_prefix
                else:
                    commutator_prefix = resault_Device_Parameters[0].get("code")
                commutator_city = resault_Device_Parameters[0].get("city")
                print(datetime.datetime.now(),"commutator_prefix полученный новым способом",commutator_prefix)
                commut_ip = resault_Device_Parameters[0].get("ip")
                commutator_city = resault_Device_Parameters[0].get("city")
                print(datetime.datetime.now(),"вывод когда введен только IP:",commutator_prefix,commut_ip)
            except:
                print(f"Проверьте что вы ввели. IP {commutator_name_or_ip} отсутствует в RDB")
                messagebox.showerror(title="Error",message=f"Проверьте что Вы ввели.\n IP {commutator_name_or_ip} отсутствует в RDB")
                return
        #в противном случае - вместо IP должне быть введено доменно ИМЯ железки
        else:
            respons_commutator_name_and_ip_via_domain = requests.post(f"rdb_host_address:8070/Catalogs/Device/List",auth=aut_,data={'description': f'{commutator_name_or_ip}'})
            try:
                resault_Device_Parameters = respons_commutator_name_and_ip_via_domain.json()
                #old get_commutator_prefix
                # commutator_prefix = ((resault_Device_Parameters[0].get("description")).upper()).split("-")[0]
                #new get_commutator_prefix
                commutator_prefix_list = resault_Device_Parameters[0].get("description").replace(" ","").replace("\t","").replace("\n","").upper().split("-")
                j=1
                for i in commutator_prefix_list:
                    if i in supported_commutator_list:
                        commutator_prefix=i
                        print(datetime.datetime.now(),"commutator_prefix",commutator_prefix)
                        break
                    else:
                        if j == len(commutator_prefix_list):
                            print(datetime.datetime.now(),"commutator_prefix",commutator_prefix_list)
                            messagebox.showerror(title="Error",message=f"\nИз частей имени коммтутатора\"{commutator_prefix_list}\" не удалось получить/найти поддерживаемый префикс.\nПоддерживаемые префиксы {supported_commutator_list}")
                    j+=1
                if commutator_prefix == "D3000":
                    commutator_prefix=commutator_prefix
                else:
                    commutator_prefix = resault_Device_Parameters[0].get("code")
                commutator_city = resault_Device_Parameters[0].get("city")
                print(datetime.datetime.now(),"commutator_prefix полученный новым способом",commutator_prefix)
                commut_ip = resault_Device_Parameters[0].get("ip")
                commutator_city = resault_Device_Parameters[0].get("city")
                print(datetime.datetime.now(),"вывод когда введен только домен:",commutator_prefix,commut_ip)
            except:
                print(f"Проверьте что Вы ввели. ИМЯ  {commutator_name_or_ip} отсутствует в RDB")
                messagebox.showerror(title="Error",message=f"Проверьте что Вы ввели.\n ИМЯ {commutator_name_or_ip} отсутствует в RDB")
                return
        commutator_name_or_ip = commut_ip
        commutator_name = resault_Device_Parameters[0].get("description").replace(" ","").replace("\t","").replace("\n","")
        commutator_prefix = commutator_prefix
        if ("unknown" in commutator_city ) or ("Unknown" in commutator_city):
            commutator_city = resault_Device_Parameters[0].get("description").split("-")[1].upper()
    if len(str(commutator_name_or_ip))<7 : #проверка на то, введено ли что-то в commutator_name_or_ip
        messagebox.showerror(title="Error",message=f"Проверте введен ли IP коммутатора\nВы ввели: \"{commutator_name_or_ip}\"")
        return
    else:

        if num_menu == 11:
            commutator_prefix = (commutator_prefix.upper()).split("-")[0].replace(" ","").replace("\t","").replace("\n","")
            if commutator_prefix not in fast_diagnostik_friendly_code:
                messagebox.showerror(title="Error",message=f"Быстрая диагностика доступна только для коммутаторов DCN\n У нас же {commutator_prefix}")
                txt.insert("end",f"Быстрая диагностика доступна только для коммутаторов DCN\n У нас же {commutator_prefix}") 
                return
        if num_menu == 12:
            if len(str(commut_port))<1 :#and len(abonent_login)<1:
                commut_port=""
            print(datetime.datetime.now(),"Menu: L2_IPOE_log_view,commutator_city=",commutator_city)
            # print("abon_ip[0]=",type(abon_ip[0]))
            if len(abonent_login)!=0:
                abon_login = f"-e \'\[{str(abonent_login)}\'"
                if abon_ip[0]!=None or abon_ip[1]!="":
                    abonip = f"-e \'{abon_ip[0]}\' -e \'{abon_ip[1]}\'"
                else:
                    abonip =""
            else:
                abon_login=""
                abonip =""
            print("abonip=",abonip)
            
            if ("Minsk" in str(commutator_city)) or ("Leskovka"in str(commutator_city)) or ("Bobruisk" in str(commutator_city)) or ("Brest" in str(commutator_city)) or ("Zhdanivichi" in str(commutator_city)) or ("Mogilev" in str(commutator_city)) or ("Gatovo" in str(commutator_city)) or ("Lesnoy" in str(commutator_city)) or ("Borovlyany" in str(commutator_city)):
                print(datetime.datetime.now(),"num_menu == 12 city = Minsk or Mogilev +")
                if "olt" in commutator_name or "OLT" in commutator_name:
                    # print("commutator_name:",commutator_name)
                    run_parametrs =f'cat /var/log/remote/10.10.10.10.log | grep -i {abon_login} -e \''+str(commutator_name)+' port '+str(commut_portV)+':'+str(number_slot_on_olt)+':'+str(port_number_in_slot)+'\' | cut -f 1-4,7-100 -d \' \''
                else:
                    run_parametrs =f'cat /var/log/remote/10.10.10.10.log | grep -i {abon_login} -e \''+str(commutator_name)+' port '+str(commut_port)+'\' | cut -f 1-4,7-100 -d \' \''
                txt.insert("end",f"\nНа стороне Jump_servera выполняется команда:\n{run_parametrs}\n\n\n")
            if "Gomel" in str(commutator_city) or ("GO" in str(commutator_city)) or ("Svetlogorsk" in str(commutator_city)) or ("RE" in str(commutator_city)) or ("DO" in str(commutator_city)) or ("ZHLO" in str(commutator_city)):
                print(datetime.datetime.now(),"num_menu == 12 city = Gomel  +")
                if "olt" in commutator_name or "OLT" in commutator_name:
                    print("commutator_name:",commutator_name)
                    run_parametrs =f'cat /var/log/remote/radius* | grep -i {abonip} {abon_login} -e \''+str(commutator_name)+' port '+str(commut_portV)+':'+str(number_slot_on_olt)+':'+str(port_number_in_slot)+'\' | cut -f 1-4,7-100 -d \' \''
                else:
                    run_parametrs =f'cat /var/log/remote/radius* | grep -i {abonip} {abon_login} -e \''+commutator_name+' port '+str(commut_port)+'\' | cut -f 1-4,5,6-100 -d \' \''
                txt.insert("end",f"\nНа стороне Jump_servera выполняется команда:\n {run_parametrs}\n\n\n")
            if "Vitebsk" in str(commutator_city) or ("VI" in str(commutator_city)) or ("NOVOPOLOTSK" in str(commutator_city)) :
                print(datetime.datetime.now(),"num_menu == 12 city = Vitebsk  +")
                run_parametrs =f'cat /var/log/remote/radius-vitebsk* | grep -i {abonip} {abon_login} -e \''+commutator_name+' port '+str(commut_port)+'\' | cut -f 1-4,5,6-100 -d \' \''
                txt.insert("end",f"\nНа стороне Jump_servera выполняется команда:\n {run_parametrs}\n\n\n")
            if commutator_city not in city_list:
                txt.insert("end","\nНе удалось определить город \n\n\n")
                print(datetime.datetime.now(),"не удалось определить город")
                return
            
            print(datetime.datetime.now(),"Команда отправляющаяся на jump_server за логами:",run_parametrs)
            # return
        else:
            print(datetime.datetime.now(),"Все параметры собраны и подготовлены для отправки")
            #если выбраны пункты меню 2 или 3 (состояние и прозвон)
            if len(str(commut_port))<1 :#and len(abonent_login)<1:
                commut_port=1
            if num_menu==2 or num_menu==3 or num_menu==7:
                print(datetime.datetime.now(),"Выбран просмотр состояния порта или прозвон или mac-адрес на порту")
                #вызываю функцию получающую инфу из sup_tools по сотонию порта и прозвону
                if commutator_prefix =="PROCURVE" and num_menu==3:      
                    #доп проверка
                    resault_sup_tools+=f"Информация по прозвону порта {commut_port} коммутатора {commutator_name}  - недоступната.\n{commutator_prefix} не поддерживает прозвон кабеля\n"
                    print(datetime.datetime.now(),resault_sup_tools)  
                    resault_sup_tools+="--------------------------------------------------------------------------------\n"
                    txt.insert("end",resault_sup_tools)
                    txt.see(END)
                    return
                else:
                    #вызываю функцию получающую инфу из sup_tools
                    res_port_info = get_sup_tools_info(num_menu,commutator_name,commut_port)
                
                #если в результате ошибка соединения с sup_tools  = забиваю на sup_tools и иду дальше
                if "Connection failed http://addres_sup_tools/" in res_port_info:
                    messagebox.showerror(title="Error",message=f"Не удалось устновить соединение с sup_tools")
                else:
                    #если в результате ошибка  = прекращаю дальнейшее выполнение
                    if "No response from remote host" in res_port_info:
                        resault_sup_tools+=f"Коммутатор {commutator_name} недоступен.\nКод ошибки: No response from remote host {commutator_name_or_ip}\n"
                        resault_sup_tools+="--------------------------------------------------------------------------------\n"
                        txt.insert("end",resault_sup_tools)
                        messagebox.showerror(title="Error",message=f"Коммутатор {commutator_name} недоступен.\nКод ошибки: No response from remote host {commutator_name_or_ip}")
                        return
                    else:
                        if num_menu==2:
                            print(datetime.datetime.now(),"Вывод информации по состоянию порта")
                            resault_sup_tools+=f"Информация по порту {commut_port} коммутатора {commutator_name} из sup_tools:\n{res_port_info}\n"
                            resault_sup_tools+="--------------------------------------------------------------------------------\n"
                            # text_in_txt =txt.get("1.0",END)
                            # len_text_in_txt = len(text_in_txt)
                        if num_menu==3:
                            print(datetime.datetime.now(),"Вывод информации по прозвону порта")
                            resault_sup_tools+=f"Информация по прозвону порта {commut_port} коммутатора {commutator_name} из sup_tools:\n{res_port_info}\n"
                            resault_sup_tools+="--------------------------------------------------------------------------------\n"

                        if num_menu==7:
                            print(datetime.datetime.now(),"Вывод информации по MAC-адресу и IP на порту")
                            resault_sup_tools+=f"Информации по MAC-адресу и IP на порту {commut_port} коммутатора {commutator_name} из sup_tools:\n{res_port_info}\n"
                            resault_sup_tools+="--------------------------------------------------------------------------------\n"
                txt.insert("end",resault_sup_tools)
                txt.see(END)
                focus_txt = 1
                cdt2=datetime.datetime.now()
                td=cdt2-cdt
                td_str_rez = f"Complete in {str(td.seconds)} seconds"
                td_lbl = Label(window,text=td_str_rez)
                td_lbl.grid(column=7, row=2)
                # print("commutator_prefix != PROCURVE or commutator_prefix !=DLINK, commutator_prefix=",commutator_prefix)
                #прозвон делаем только из билинга, из альбатрсоа скриптомне трогаем
                # if num_menu==3:
                    # print("commutator_prefix !=DLINK ???")
                    # return

               
            run_parametrs = f"python3 /home/vladislav_ga/telnet_jump.py 3 {commutator_prefix} {commutator_name_or_ip} {num_menu} {commut_port}"
            print(datetime.datetime.now(),f"Данные подготовленные для отправки на jump_server: {commutator_prefix} {commutator_name_or_ip} {num_menu} {commut_port}")
        try:
            #если пытаемся для олт сделать,что-либо кhоме состояния порта, мака и прозвона  - выдаём что на сервер не идём и выходим
            if ("/" in str(commut_port) or "IES" in commutator_prefix) and (num_menu==1 or num_menu==4 or num_menu==5 or num_menu==6 or num_menu==11):
                print(datetime.datetime.now(),"На jump_server не идём, это ОЛТ/IES")
                txt.insert("end",f"Это {commutator_name}, на jump_server не идём, там нечего смотреть для данного оборудования")
                cdt2=datetime.datetime.now()
                td=cdt2-cdt
                td_str_rez = f"Complete in {str(td.seconds)} seconds"
                td_lbl = Label(window,text=td_str_rez)
                td_lbl.grid(column=7, row=2)
                return
            else:
                print(datetime.datetime.now(),"Выполняется коннект на jump_server и выполнение команд на стороне jump_serverа")
                resault = get_jump_server_info(host,user,secret,port,run_parametrs)  
            print(datetime.datetime.now(),"Получены данные с jump_serverа:")
            resault=resault.decode('ascii')
            # print("resault=",resault)
            #если после коннекта к альбтросы и попытке сриптом зайти на его, получаем = No route to host" - значит железка лежит.
            if "No route to host" in resault:
                resault = f"Ошибка, коммутатор {commutator_name_or_ip} недоступен!!!\n"
                messagebox.showerror(title="Error",message=f"Коммутатор {commutator_name} недоступен.\nКод ошибки: No response from remote host {commutator_name_or_ip}")
                resault+="--------------------------------------------------------------------------------\n"
            # print(datetime.datetime.now(),"len resault = 0",len(resault.decode('ascii')))
            if "telnet connection closed" in resault:
                resault = f"Не удалось устновить telnet соединение с коммутатором {commutator_name}"
            if len(resault)==0:
                abonip +=" или"
                resault = f"Для {abonip} {abonent_login} и/или \'{commutator_name} port {str(commut_port)}\' в логах jump_serverы инфы не найдено"
        except Exception as e:
            # e=""
            print('\n')
            try:
                status_code = e.response.status_code
            except:
                status_code = 0
                print(datetime.datetime.now(),"\nОшибка\nДетальный код ошибки смотрите в консоли")
            # logging.error(e)
            # print(type(status_code),status_code)
            if status_code == 401:
                resault+="Пользователь не авторизован.\nПовторите попытку ввода данных УЗ\n"
                logging.error(e)
            elif status_code == 403:
                resault+="Доступ запрещен. Возможно введены не коректные логин и пароль\n"
                logging.error(e)
            elif status_code == 0:
                resault+=f"\nОшибка!\nДетальный код ошибки смотрите в консоли\n"+"_"*170
                logging.error(e)
            else:
                resault+=f"\nОшибка!\nДетальный код ошибки смотрите в консоли\n"+"_"*170
                # \nЗначение даты «{start_time}» для поля «created» недействительно. Действительные форматы:\n«гггг/ММ/дд ЧЧ:мм»\n«гггг-ММ-дд ЧЧ:мм»\n«гггг/ММ/дд»\n«гггг-ММ-дд» \nили формат периода, например, «-5д», «4н 2д».\n"+"_"*169
                logging.error(e)
            print(status_code)
    #txt.grid(column = 0, pady = 10, padx = 10)
    txt.config(state="normal")
    cdt2=datetime.datetime.now()
    td=cdt2-cdt
    td_str_rez = f"Complete in {str(td.seconds)} seconds"
    
    #очищаю притявый в битах ответ от jump_server от всего лишнего
    resault = resault.replace("          Eth","Eth")
    resault = resault.replace("[24;1H[24;23H[24;1H[?25h[24;23H[24;0HE[24;1H[24;23H[24;1H[2K[24;1H[?25h[24;1H[1;24r[24;1","")
    resault = resault.replace("[24;1H[24;23H[24;1H[?25h[24;23H","")
    resault = resault.replace("[24;1H[24;24H[24;1H[?25h[24;24H","")
    resault = resault.replace("[7mCTRL+C[0m [7mESC[0m [7mq[0m Quit [7mSPACE[0m [7mn[0m Next Page [7mp[0m Previous Page [7mr[0m Refresh","")
    resault = resault.replace("[7mCTRL+C[0m [7mESC[0m [7mq[0m Quit [7mSPACE[0m [7mn[0m Next Page [7mENTER[0m Next Entry [7ma[0m All","")
    resault = resault.replace("7",'')
    resault = resault.replace(" --More--           ","")
    resault = resault.replace("-- more --, next page: Space, continue: c, quit: ESC                                                      Error Packet	RX CRC			:0","")
    resault = resault.replace("-- more --, next page: Space, continue: c, quit: ESC                                                        ","")
    resault = resault.replace("[1;24r[24;1H[24;1H[2K[24;1H[?25h[24;1H[24;1H","")
    resault = resault.replace("[24;1H[24;22H[24;1H[?25h[24;22H[24;0HE[24;1H[24;22H[24;1H[2K[24;1H[?25h[24;1H[1;24r[24;1H[1;24r[24;1H[24;1H[2K[24;1H[?25h[24;1H[24;1H","")
    resault = resault.replace("[24;1H[24;22H[24;1H[?25h[24;22H","")
    resault = resault.replace("[H[2J","")
    resault = resault.replace("# [24;22H [24;22H[?25h[24;23H[24;23H [24;23H[?25h[24;24H","")
    resault = resault.replace("[1;24r[24;1H[24;1H[2K[24;1H[?25h[24;1H[24;1H","")
    resault = resault.replace("[24;1H[2K-- MORE --, next page: Space, next line: Enter, quit: Control-C[24;1H[24;1H[2K[24;1H[1;24r[24;1HI","")
    txt.insert("end",resault)
    #отрисовываю лэйбл с временем выполнения
    td_lbl = Label(window,text=td_str_rez)
    td_lbl.grid(column=7, row=2)
    # if "Error, it is not possible to get the IP of the switch from the given name" in resault:
    #     msg_res = f"Не удалось получить IP из введенного имени коммутатора {commutator_name_or_ip}\nДля продолжения работы с данным оборудованием, введите префикс коммутатора и его IP"
    #     txt.insert("end",msg_res)
    print(datetime.datetime.now(),"Все данные получены и отображены на форме")
    if focus_txt==1:
        pass
    else:
        txt.see(END)




def click_show_log():
    set_data(num_menu=1)

def click_show_port():
    set_data(num_menu=2)

def click_show_vct():
    set_data(num_menu=3)

def click_show_dhcp():
    set_data(num_menu=4)

def click_show_igmp():
    set_data(num_menu=5)

def click_show_loop():
    set_data(num_menu=6)

def click_show_mac():
    set_data(num_menu=7)

def click_show_fast_dcn():
    set_data(num_menu=11)

def click_radius_dhcp_log_view():
    set_data(num_menu=12)


#функция осуществляет подключение к jump_server
def get_jump_server_info(host,user,secret,port,run_parametrs):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command(run_parametrs)
    data = stdout.read() + stderr.read()
    client.close()
    return data

#получение диагностической информации от sup_tools
def get_sup_tools_info(num_menu=2,commutator_name='',commut_port=''):
    # print("get_sup_tools_info_parametr",num_menu,commutator_name,commut_port)
    url_auth = "http://addres_sup_tools/?auth"
    url_diag = 'http://addres_sup_tools/?action=diag'
    # print("num_menu=",type(num_menu))
    if num_menu==2:
        action = 'all'
    if num_menu==3:
        action = 'selt'
    if num_menu==7:
        action = 'mac'

    data_auth = { 'login': f'{user}','password': f'{secret}'}
    data_diagn = {'devname':f'{commutator_name}','devport':f'{commut_port}','action':f'{action}'}

    # пробую получить данные post запросом у sup_tools
    try:
        respons_auth = requests.post(url=url_auth, data=data_auth)
    except:
        res_port_info = "Connection failed http://addres_sup_tools/"
    r_a_c = respons_auth.cookies

    respons_diag = requests.post(url=url_diag,cookies=r_a_c,data=data_diagn)
    respons_diag_text = respons_diag.text
    respons_diag.close()

    src = respons_diag_text
    soup = BeautifulSoup(src, "lxml")
    #получаю pre со страницы
    res_port_info= soup.find("pre")#.text
    if "rror" in respons_diag_text:
        return "Ошибка, sup_tools не смог обработать запрос\n"+res_port_info.text
    addres = soup.find(class_ ="alert alert-success mt-1")
    # print("res_port_info",res_port_info)
    # print("addres",addres)
    if (res_port_info == None) or (addres == None):
        try:
            res = soup.find(class_ ="alert alert-danger mt-4 alert-dismissible fade show").text
        except:
            res=""
        return "Нет информации по маку/прозвону на порту"+"\n"+res
    else:
        res_port_info = res_port_info.text
        addres = addres.find_all(class_="row")[2].find(class_="col-6 col-md-7").text
    print("addres=",addres)
    if num_menu==7:
        coun_str = res_port_info.count("\n")
        print(datetime.datetime.now(),"coun_str:",coun_str)
        q = 1
        res_ip_mac_str = ""
        macs_on_port = []
        mac_company = ""
        while q <= coun_str:
            fidn_n = res_port_info.find("\n")
            find_str = res_port_info[:fidn_n]
            print(datetime.datetime.now(),"find_str=",find_str)
            
            #вычленяю мак адреса 
            
            macs_on_port.append(find_str[5:13])
            if find_str[5:13].startswith("14:4F:D7"):
                mac_company = "---->>> RED BOX"
            else:
            # пробую по API, на основании МАК  адреса получить информацию о вендоре
                try:
                    print(datetime.datetime.now(),"Попытка получить информацию по вендору утройства на порту, по MAC через api.macvendors.com")
                    url_macvendorscom = f"https://api.macvendors.com/{macs_on_port[q-1]}"
                    res_macvendorscom = requests.get(url_macvendorscom)
                    mac_company =res_macvendorscom.text
                except:
                    print(datetime.datetime.now(),"Попытка получить информацию по вендору утройства на порту, по MAC через api.macvendors.com - FAILED")
                    
                    mac_company =" "+"Не удалось получить вендона."
            
            res_port_info = res_port_info[fidn_n+1:]
            res_ip_mac_str += find_str+"  "+mac_company+"\n"
            time.sleep(0.76)
            q+=1
        return f"Заменка по железке: {addres}\n\n" +res_ip_mac_str
    else:
        return f"Заменка по железке: {addres}\n\n" +res_port_info



btn_show_log = Button(window, text="Просмотр логов коммутатора", bg="#B0E0E6", fg="#0a0a0a", command=click_show_log)
btn_show_log.grid(column=4, row=4,sticky=N+S+E+W)

btn_show_port = Button(window, text="Информация по состоянию порта", bg="#7FFFD4", fg="black", command=click_show_port)
btn_show_port.grid(column=5, row=3,sticky=N+S+E+W)

btn_show_vct = Button(window, text="Проверка длинны кабеля", bg="#FFEFD5", fg="black", command=click_show_vct)
btn_show_vct.grid(column=5, row=4,sticky=N+S+E+W)

btn_show_dhcp = Button(window, text="Получение DHCP таблицы", bg="#F0E68C", fg="black", command=click_show_dhcp)
btn_show_dhcp.grid(column=7, row=4,sticky=N+S+E+W)

btn_show_igmp = Button(window, text="Получение IGMP таблицы", bg="#00CED1", fg="black", command=click_show_igmp)
btn_show_igmp.grid(column=7, row=3,sticky=N+S+E+W)

btn_show_loop = Button(window, text="Проверка на кольцо (Loopdetect)", bg="#FFDAB9", fg="black", command=click_show_loop)
btn_show_loop.grid(column=6, row=3,sticky=N+S+E+W)

btn_show_mac = Button(window, text="МАК и IP на порту", bg="#40E0D0", fg="black", command=click_show_mac)
btn_show_mac.grid(column=6, row=4,sticky=N+S+E+W)

btn_show_mac = Button(window, text="Быстрая диагностика (только DCN подобные)", bg="#FF6347", fg="white", command=click_show_fast_dcn)
btn_show_mac.grid(column=4, row=3,sticky=N+S+E+W)

btn_radius_dhcp_log_view = Button(window, text="DHCP / Radius logs", bg="white", fg="red", command=click_radius_dhcp_log_view)
btn_radius_dhcp_log_view.grid(column=2, row=3,sticky=N+S+E+W)


def form_cleaning():
    txt.delete('1.0',END)

btn_form_cleaning = Button(window, text="Form cleaning", bg="red", fg="white", command=form_cleaning)
btn_form_cleaning.grid(column=0, row=0,sticky=N+S+E+W)


window.mainloop()

