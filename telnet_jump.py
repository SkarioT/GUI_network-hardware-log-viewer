import os
import sys
import telnetlib
import time
import datetime
import socket

comand_index=""

commutator_list='S2995','Q3470','ZY3528','ZY3500','S2989','S2900','D5960','D5750','D4650','D4600','D3650','D3950','Z5250','Z5260','Z5900','Z5928','P2610','P2620','P2626','P2650','Z2900','D3000','D1210','A6224'
DNC_commutator_list='Q3470','D5960','D5750','D4650','D4600','D3650','D3950'




def commutator_show(commutator_name,port_name,menu_id):
    
    commutator_prefix=commutator_name[0]
    commutator_name=commutator_name[1]

    first_clear=commutator_name.replace(' ','',10)
    commutator_name=first_clear.replace('\t','',10)
    USER='username\n'
    PSWD='drowssap'

    #'D3950','Z5260','Z2900','Z5900','A6224','P2610','P2626'
    if ('DCN' in commutator_prefix) or ('Q3470' in commutator_prefix) or ('S2995' in commutator_prefix)or ('S2989' in commutator_prefix) or ('D3950' in commutator_prefix) or ('S2900' in commutator_prefix) or ('D3650' in commutator_prefix) or ('D5750' in commutator_prefix) or ('D4650' in commutator_prefix) or ('D4600' in commutator_prefix) or ('D5960' in commutator_prefix):
        print('Connection to DCN device {} / {}'.format(commutator_prefix,commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                ss= t.read_until(b'login:',timeout=10.0)
                # print("ждали логин,пошли дальше")
                t.write(USER.encode())
                time.sleep(0.1)
                # t.write(b'\n')
                # print("логин введен,ждём строку Password ")
                cdt_now = datetime.datetime.now()
                ss=t.read_until(b'Password:',3.1)
                time.sleep(0.1)
                # print("Строка Password найдена, вводим пароль")
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                time.sleep(0.1)
                cdt_next =datetime.datetime.now()
                td=cdt_next-cdt_now
                td_int_rez = td.seconds
                if td_int_rez >= 3:
                    print(f"Password feedback timeout: {td_int_rez} second")
                    t.close()
                    return f"Error, telnet connection failed to {commutator_name}"
                    
                # print("Дошли до момента когда логин и пароль типо введены")
                #блок команд
                SHOW_LOGG='sh logg b l w'
                SHOW_LOG='show log'

                SHOW_PORT='sh int ether 1/{}'.format(port_name)
                SHOW_PORT_CONF='sh run in e 1/{}'.format(port_name)

                SHOW_PORT48='sh int ether 0/0/{}'.format(port_name)
                SHOW_PORT48_CONF='sh run in e 0/0/{}'.format(port_name)

                SHOW_PORT_D57='sh int ether 1/0/{}'.format(port_name)
                SHOW_PORT_D57_CONF='sh run in e 1/0/{}'.format(port_name)

                VCT='virtual-cable-test interface ethernet 1/{}'.format(port_name)
                VCT48='virtual-cable-test interface ethernet 0/0/{}'.format(port_name)
                VCT_D57='virtual-cable-test interface ethernet 1/0/{}'.format(port_name)
                LOOP='show loopback-detection'
                IGMP='sh ip igmp snooping'
                DHCP='sh ip dhcp snooping binding all'
                MAC_PORT='sh mac-address-table int eth 1/{}'.format(port_name)
                MAC_PORT48='sh mac-address-table int eth 0/0/{}'.format(port_name)
                MAC_D57='sh mac-address-table int eth 1/0/{}'.format(port_name)
                SH_MAC='sh mac-address-table add {}'.format(port_name)
                ALL_PORT='sh interface ethernet status'
                #11) быстрая диагностика
                if menu_id=='11':
                    #состоянии порта
                    time.sleep(0.5)
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(SHOW_PORT_CONF.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    res_state = t.read_very_eager().decode('ascii')
                    if 'error!' in res_state:
                        time.sleep(0.5)
                        t.write(SHOW_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.3)
                        t.write(b' ')
                        time.sleep(0.3)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(SHOW_PORT48_CONF.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(1)
                        res_state = t.read_very_eager().decode('ascii')
                        if 'error!' in res_state:
                            time.sleep(1)
                            t.write(SHOW_PORT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(SHOW_PORT_D57_CONF.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            res_state = t.read_very_eager().decode('ascii')
                            
                    time.sleep(1)
                    t.write(VCT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res_vct = t.read_very_eager().decode('ascii')
                    if 'error!' in res_vct:
                        time.sleep(1)
                        t.write(VCT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(4)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        res = t.read_very_eager().decode('ascii')
                        if 'error!' in res_vct:
                            time.sleep(1)
                            t.write(VCT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            res_vct = t.read_very_eager().decode('ascii')
                    
                    #igmp
                    time.sleep(1)
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    readd = t.read_very_eager().decode('ascii')
                    split_list=readd.split()
                    len_split=len(split_list)-2
                    vlan=split_list[len_split]

                    igmp='sh ip igmp snoop vlan {}'.format(vlan)

                    time.sleep(1)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    res_igmp = t.read_very_eager().decode('ascii')
                   
                    #DHCP
                    t.write(b' ')
                    time.sleep(1)
                    t.write(DHCP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res_dhcp = t.read_very_eager().decode('ascii')
                    res_dhcp = res_dhcp.replace("-",":")
                    
                    return res_state+"\n"+res_vct+"\n"+res_igmp+"\n"+res_dhcp
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    time.sleep(1)
                    t.write(SHOW_LOGG.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.5)
                   
                    res=t.read_very_eager().decode('ascii')
                    if 'Invalid input detected' in res:
                        time.sleep(1)
                        t.write(SHOW_LOG.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        res=t.read_very_eager().decode('ascii')
                    return res
                #2)просмотр порта
                if menu_id=='2':
                    time.sleep(0.5)
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(SHOW_PORT_CONF.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(3)
                    res = t.read_very_eager().decode('ascii')
                    if 'error!' in res:
                        time.sleep(0.5)
                        t.write(SHOW_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(SHOW_PORT48_CONF.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(3)
                        res = t.read_very_eager().decode('ascii')
                        if 'error!' in res:
                            time.sleep(1)
                            t.write(SHOW_PORT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(SHOW_PORT_D57_CONF.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(3)
                            res = t.read_very_eager().decode('ascii')
                    return res.replace("--More--","")
                #3)прозвон порта
                if menu_id=='3':
                    time.sleep(1)
                    t.write(VCT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    if 'error!' in res:
                        time.sleep(1)
                        t.write(VCT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        res = t.read_very_eager().decode('ascii')
                        if 'error!' in res:
                            time.sleep(1)
                            t.write(VCT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            res = t.read_very_eager().decode('ascii')
                    return res
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    time.sleep(1)
                    t.write(DHCP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res.replace("-",":")
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    time.sleep(1)
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    readd = t.read_very_eager().decode('ascii')
                    split_list=readd.split()
                    len_split=len(split_list)-2
                    vlan=split_list[len_split]

                    igmp='sh ip igmp snoop vlan {}'.format(vlan)

                    time.sleep(1)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    res=t.read_very_eager().decode('ascii')
                    return res
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    time.sleep(1)
                    t.write(LOOP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res.replace(" --More-- ","")
                #7)Просмотр мака на порту
                if menu_id=='7':
                    time.sleep(1)
                    t.write(MAC_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    if 'error!' in res:
                        time.sleep(1)
                        t.write(MAC_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        res = t.read_very_eager().decode('ascii')
                        if 'error!' in res:
                            time.sleep(1)
                            t.write(MAC_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            res = t.read_very_eager().decode('ascii')
                    return res.replace("-",":").replace(" --More--          ","")
                #8)
                if menu_id=='8':
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res.replace(" --More-- ","")
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    res = t.read_very_eager().decode('ascii')
                    return res
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('ZTE5928' in commutator_prefix) or ('Z5250' in commutator_prefix) or ('Z5260' in commutator_prefix) or ('Z5900' in commutator_prefix) or ('Z5928' in commutator_prefix):
        print('Connection to ZTE 5-series  device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:

                ss= t.read_until(b'Username:')
                #input login
                t.write(USER.encode())
                t.read_until(b'Password:')
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                SHOW_LOGG='show logging alarm\n'
                SHOW_PORT='show interface gei-0/1/1/{}\n'.format(port_name)
                VCT='show vct interface gei-0/1/1/{}\n'.format(port_name)
                #LOOP='show loopback-detection\n'
                IGMP='show ip igmp snooping\n'
                DHCP='show ip dhcp snooping database\n'
                MAC_PORT='show mac table interface gei-0/1/1/{}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b'')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    res = t.read_very_eager().decode('ascii')
                    #new_module
                    j=1
                    index_index=0
                    index_mac=0
                    index_interface=0
                    index_vlan=0
                    index_ip=0
                    index_exp=0
                    index_op82=0
                    index_gw=0
                    all_port_str=""
                    temp_str=""
                    if len(res) < 100 :
                        res_str="IP don`t find!!!"
                        return res+"\n"+res_str
                    split_res=res.split("\n")
                    count_target_line=split_res[2]
                    split_count_target_line=count_target_line.split(":")
                    count_iter=split_count_target_line[1]
                    
                    str_find_index_start=""
                    find_all_port=""
                    new_str=""
                    d_index = dict()
                    d_all_port=dict()

                    #полуаю индексы начал инфрмации по порту. набиваю словарь с началми индексов
                    while j < int(count_iter)+1:
                        find_index_start=res.find("Index   : {}".format(j))
                        d_index[j]=find_index_start
                        find_mac=res.find("MAC addr: ")
                        find_vlan=res.find("VLAN    :")
                        j+=1
                    j=1
                    #выбираю по индекс конкртные порты [ j(k) : j+1]. набиваю словарь фул инфой по порту
                    while j < int(count_iter)+1:
                        k=j
                        j+=1

                        if k==int(count_iter):
                                d_all_port[k]=res[ d_index[k]: ].replace("\n","").replace("\x08","").replace("\r","").replace("\t","").replace("--More--","")
                        elif j>int(count_iter):
                                pass
                        else:
                                d_all_port[k]=res[ d_index[k]:d_index[j] ].replace("\n","").replace("\x08","").replace("\r","").replace("\t","").replace("--More--","")

                    j=1
                    
                    # print("d_all_port : ",d_all_port)
                    while j < int(count_iter)+1:
                        # print("j = ",j)
                        all_port_str=d_all_port[j]
                        #полуаю индексы всех параметров, по каждому порту
                        index_index=all_port_str.find("Index   :")
                        index_mac=all_port_str.find("MAC addr:")
                        index_vlan=all_port_str.find("VLAN    :")
                        index_layer=all_port_str.find("Layer        : ")
                        index_interface =all_port_str.find("Interface    :")
                        index_op82=all_port_str.find(" Option82     :")
                        index_ip=all_port_str.find("IP addr      :")
                        index_exp=all_port_str.find("Expiration :")
                        index_gw=all_port_str.find(" Gateway IP :")
                        #получаю конечно значение параметра
                        index_=(all_port_str[index_index : index_mac ]).replace("Index   : ","")
                        # print("index:",index_)
                        mac_=(all_port_str[index_mac : index_vlan ]).replace("MAC addr: ","")
                        # print("mac:",mac_)
                        vlan_=(all_port_str[index_vlan : index_layer ]).replace("VLAN    : ","")
                        # print("vlan",vlan_)
                        interface_=(all_port_str[index_interface : index_op82]).replace("Interface    : ","").replace("\t","")
                        # print("interface_",interface_)
                        ip_=(all_port_str[index_ip : index_exp]).replace("IP addr      : ","")
                        # print("ip_",ip_)
                        expir_=(all_port_str[index_exp : index_gw]).replace("Expiration : ","")
                        # print("exp:",expir_)
                        temp_str= index_ +"\t"+ interface_ +"\t"+ mac_ +"\t"+ ip_ +"\t"+ expir_ +"\t"+ vlan_ 
                        # print("temp_str!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:",temp_str)
                        j+=1
                        new_str+=temp_str+"\n"
                        temp_str=""
                        # print(new_str)

                    res_str="Index\tInterface\tMAC\t\tIP\t\t\tExpiration\tVLAN\n"+new_str
                    
                    return res+"\n"+res_str
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    res=t.read_very_eager().decode('ascii')
                    return res.replace("--More--","")
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    res='ZTE commutator don`t supporting LOOPDETECT'
                    return res
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('PROCURVE' in commutator_prefix) or ('P2650' in commutator_prefix) or ('P2620' in commutator_prefix) or ('P2610' in commutator_prefix) or ('P2626' in commutator_prefix):
        print('Connection to PROCURVE device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(b'\n')
                time.sleep(0.5)
                t.write(b' supportscript\n')
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                SHOW_LOGG='show log por -r'
                SHOW_PORT='show int {}\n'.format(port_name)
                SHOW_CONF='show config\n'
                #VCT='show vct interface gei-0/1/1/{}\n'.format(port_name)
                LOOP='show loop-protect\n'
                IGMP='show ip igmp\n'
                DHCP='show dhcp-snooping binding\n'
                MAC_PORT='show mac-address ethernet {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    time.sleep(1)
                    t.write(SHOW_LOGG.encode())
                    time.sleep(0.5)
                    t.write(b'\n')
                    time.sleep(1.5)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res= t.read_very_eager().decode('ascii')
                    t.close()
                    log_poz_start = res.find("Keys")
                    res = res[log_poz_start:]
                    return res
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    time.sleep(2)
                    res1 = t.read_very_eager().decode('ascii')
                    time.sleep(2)
                    t.write(b' ')
                    t.write(SHOW_CONF.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    res2 = t.read_very_eager().decode('ascii')
                    port_poz_start=res2.find("interface {}".format(port_name))
                    res_start=res2[port_poz_start:]
                    port_poz_fin_id=res_start.find("exit")
                    port_poz_fin=port_poz_start+port_poz_fin_id
                    res2=res2[port_poz_start:port_poz_fin]
                    res2=res2.replace("interface","port")
                    resault = res1+"\n"+res2
                    os.system('clear')
                    try:
                        comand_index = resault.index("Status and Counters")
                        return resault[comand_index:]
                    except:
                        return resault
                    # print("index SHOW_PORT",comand_index)
                #3)прозвон порта
                if menu_id=='3':
                    res='Procurve - don`t suport VCT'
                    return res
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    t.close()
                    return res
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    resault =t.read_very_eager().decode('ascii')
                    # print("print resault:\n",resault)
                    t.close()
                    comand_index1 = resault.index("VLAN ID : 17")
                    res = resault[comand_index1:]
                    return res
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    t.close()
                    return res
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    t.close()
                    return res
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('ZTE' in commutator_prefix) or ('Z2900' in commutator_prefix):
        # if menu_id=='1':
        #     upd_c_n=commutator_name.lower()
        #     res=os.system('cat /var/log/remote/{}.log'.format(upd_c_n))
        #     return res
        print('Connection to ZTE device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show terminal log\n'
                SHOW_PORT='show port {}\n'.format(port_name)
                SHOW_PORT2='show port {} statistics\n'.format(port_name)
                SHOW_PORT_IGMP='show igmp snooping port {}\n'.format(port_name)
                #show iptv rule port 17 package
                VCT='show vct port {}\n'.format(port_name)
                LOOP='show loopdetect\n'
                IGMP='show igmp snooping\n'
                DHCP='show dhcp snooping binding\n'
                MAC_PORT='show fdb port {} detail\n'.format(port_name)
                port_name=str(port_name).replace(':','.')
                MAC_FIND='show fdb mac {}\n'.format(port_name)
                ALL_PORT='show port 1-20 brief\n'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    res = t.read_very_eager().decode('ascii')
                    return res[150:]
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(SHOW_PORT2.encode())
                    t.write(b' ')
                    time.sleep(1)
                    t.write(SHOW_PORT_IGMP.encode())
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[140:]
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(10)
                    res = t.read_very_eager().decode('ascii')
                    return res[140:]
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[150:]
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.5)
                    res1=t.read_very_eager().decode('ascii')
                    res_1=res1[150:].split(' ')
                    ss=res_1[63].split(',')
                    vlan=ss[1]
                    time.sleep(0.5)
                    igmp_vlan='show igmp snooping vlan {}\n'.format(vlan)

                    t.write(igmp_vlan.encode())
                    time.sleep(0.5)
                    res2=t.read_very_eager().decode('ascii')
                    res = str(res1)+'\n'+res2
                    return res
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[140:]
                #8) за ZTE нет лупдетекта
                if menu_id=='8':
                    t.write(MAC_FIND.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    res = t.read_very_eager().decode('ascii')
                    return res[140:]             
                if menu_id=='9':
                    t.write(ALL_PORT.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    res = t.read_very_eager().decode('ascii')
                    return res[140:]                
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('D3000' in commutator_prefix):

        print('Connection to D-link device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show log\n'
                SHOW_PORT='show error ports {}\n'.format(port_name)
                VCT='cable_diag ports {}\n'.format(port_name)
                LOOP='show loopdetect ports 1-13\n'
                LOOP2='show loopdetect ports 14-28\n'
                IGMP='show igmp_snooping group\n'
                DHCP='show address_binding ip_mac all\n'
                DHCP2='show address_binding dhcp_snoop binding_entry\n'
                MAC_PORT='show fdb port {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP2.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[380:]              
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    return res[380:] 
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    res1=t.read_very_eager().decode('ascii')
                    time.sleep(1)
                    t.write(b'q')
                    t.write(LOOP2.encode())
                    time.sleep(1)
                    res2 = t.read_very_eager().decode('ascii')
                    res=res1+res2
                    return res1[370:1480]+res2[200:]  
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('DLINK' in commutator_prefix) or ('D1210' in commutator_prefix):

        print('Connection to D-link device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show log\n'
                SHOW_PORT='show error ports {}\n'.format(port_name)
                VCT='cable diagnostic port {}\n'.format(port_name)
                LOOP='show loopdetect ports 1-13\n'
                LOOP2='show loopdetect ports 14-28\n'
                IGMP='show igmp_snooping group\n'
                DHCP='show address_binding ip_mac all\n'
                MAC_PORT='show fdb port {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1.5)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    return res[370:990]            
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]
                #4)просмотр DHCP таблицы
                if menu_id=='4':
    
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    res=res[370:]
                    return res
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    return res[370:1105]
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    res1=t.read_very_eager().decode('ascii')
                    time.sleep(1)
                    t.write(b'q')
                    t.write(LOOP2.encode())
                    time.sleep(1)
                    res2 = t.read_very_eager().decode('ascii')
                    res=res1[370:1480]+res2[165:1450]
                    return res
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[370:]         
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('ALCATEL_BC' in commutator_prefix) or ('ALCATEL' in commutator_prefix) or ('A6224' in commutator_prefix):
        print('Connection to Alcatel device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                ####логи коммутатора. ГОТОВО.
                SHOW_LOGG='show logging\n'
                ####состояние порта. ГОТОВО.
                SHOW_PORT_2='show interfaces status ethernet e{}\n'.format(port_name)
                SHOW_PORT='show interfaces configuration ethernet e{}\n'.format(port_name)
                SHOW_PORT_3='show interfaces counters ethernet e{}\n'.format(port_name)
                SHOW_PORT_4='show interfaces access-lists ethernet e{}\n'.format(port_name)
                ####прозвон. ГОТОВО.
                VCT='test copper-port tdr e{}\n'.format(port_name)
                ####проверка на кольцо. ГОТОВО,но нужны тесты
                LOOP='show loopback-detection\n'
                #с IGMP сложно, тут необxодимо знать влан. show vlan можно посмотреть все вланы, нас интерсует последний тот что начинается на 400-X
                getVLAN='show vlan\n' 
                #get all VLAN
                ####HCP. ГОТОВО
                DHCP='show ip dhcp snooping binding\n'
                #мак на порту ГОТОВО!!!
                MAC_PORT='show ip source-guard status ethernet e{}\n'.format(port_name)
                #поиск по маку
                SH_MAC=' show ip source-guard status mac-address {}'.format(port_name)
                ALL_PORT='show interfaces status'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1.5)
                    res1 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_2.encode())
                    time.sleep(1.5)
                    res2 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_3.encode())
                    time.sleep(1.5)
                    res3 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_4.encode())
                    time.sleep(1.5)
                    res4 = t.read_very_eager().decode('ascii')
                    #'\033[31m'+ input_comman_ip_or_mac + '\033[0m'
                    res="Port config:\n"+res1[112:]+"\nState port:\n"+res2[42:]+"\nReal-time traffic & Error:\n"+res3[37:]+"\nIPTV parametrs:\n"+res4[41:]
                    return res
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(5)
                    res = t.read_very_eager().decode('ascii')
                    return res+'\n'
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(getVLAN.encode())
                    time.sleep(1.5)
                    res = t.read_very_eager().decode('ascii')
                    #из полученного результат всех вланов, нахожу тот который нужен.
                    split_list=res.split()
                    len_split=len(split_list)-5
                    vlan=split_list[len_split]
                    print("vlan:",vlan)
                    time.sleep(0.5)
                    igmp='show ip igmp snooping groups vlan {}'.format(vlan)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    time.sleep(1.5)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    return res
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res=t.read_very_eager().decode('ascii')
                    return res
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                if menu_id=='8':
                    print(port_name)
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    if ('ZYXEL' in commutator_prefix) or ('ZY3500' in commutator_prefix) or ('ZY3528' in commutator_prefix):
        print('Connection to ZyXel device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,5) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                ####логи коммутатора. ГОТОВО.
                SHOW_LOGG='show logging\n'
                ####состояние порта. ГОТОВО.
                SHOW_PORT='show interfaces {}\n'.format(port_name)
                ####прозвон. ГОТОВО.
                VCT='cable-diagnostics {}\n'.format(port_name)
                ####проверка на кольцо. ГОТОВО,но нужны тесты
                LOOP='show loopguard\n'
                #igmp
                IGMP='show igmp-snooping group client all\n'
                IGMP28='show igmp-snooping group all\n'
                ####HCP. ГОТОВО
                DHCP='show dhcp snooping binding\n'
                #мак на порту ГОТОВО!!!
                MAC_PORT='show mac address-table port {}\n'.format(port_name)
                #поиск по маку
                SH_MAC='show mac address-table mac {}'.format(port_name)
                ALL_PORT='show interfaces status'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1.5)
                    t.write(b' ')
                    time.sleep(1.5)
                    res = t.read_very_eager().decode('ascii')#.decode('utf-8')
                    #'\033[31m'+ input_comman_ip_or_mac + '\033[0m'
                    return res[50:]
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(5)
                    res = t.read_very_eager().decode('ascii')
                    res=res[50:]
                    return res
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1.5)
                    t.write(b' ')
                    time.sleep(1.5)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    if 'Invalid' in res:
                        t.write(IGMP28.encode())
                        t.write(b'\n')
                        time.sleep(1.5)
                        t.write(b' ')
                        time.sleep(1.5)
                        res = t.read_very_eager().decode('ascii')
                    return res[50:]
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res1=t.read_very_eager().decode('ascii')
                    return res1[50:]
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                if menu_id=='8':
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
        except BrokenPipeError or EOFError :
            print("Error. Unable to establish telnet connection")
            return "Error. Unable to establish telnet connection"
    else:
        return "Do not success !\n Skript popitalsya nayti swith i menu kuda zayti no ne smog =("


def menu():
    all_sysargv = sys.argv
    commutator_name = ['','']
    commutator_name[0] = all_sysargv[2].upper()
    commutator_name[1] = all_sysargv[3]
    menu_id = sys.argv[4]
    port_name = sys.argv[5]
    comm_name_or_ip = commutator_name[1]

    
    def get_com_ip(comm_name_or_ip):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            
            s.connect((f"{comm_name_or_ip}", 23))
            ip_commut = s.getpeername()[0]
           
            s.close()
        except:
            ip_commut = 0
            print(f"\nError, it is not possible to get the IP of the switch from the given name: {comm_name_or_ip}")
        return str(ip_commut)

    if commutator_name[1].startswith("1"):
        res_commut_name = "true"
        res=commutator_show(commutator_name,port_name,menu_id)
        
    else:
        res_commut_name = get_com_ip(comm_name_or_ip)
        if res_commut_name == '0':
            res = ""
        else:
            comname = commutator_name[1]
            commutator_name[0]=comname.split("-")[0].upper()
            commutator_name[1]=res_commut_name
            
            res=commutator_show(commutator_name,port_name,menu_id)
            if "D3000" in commutator_name[0]:
                res = res.replace("[7mCTRL+C[0m [7mESC[0m [7mq[0m Quit [7mSPACE[0m [7mn[0m Next Page [7mENTER[0m Next Entry [7ma[0m All","")
                res = res.replace("[1A[80C","")  
    # print(res.replace("",'').replace("----- more ----- Press Q or Ctrl+C to break ----- ",""))



# скрипт запускается с параметрами "{3} {commutator_prefix} {commutator_name_or_ip} {num_menu} {commut_port} "
menu()