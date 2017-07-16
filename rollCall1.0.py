#!/usr/bin/python
# -*- coding: UTF-8 -*-
#运行环境 python2.7
#author：hx

from Tkinter import *
import tkMessageBox
import random
import datetime
import ttk


#学员
with open('doc/logstu.txt', 'r')as f:
    selected_students = f.read().split('&')


with open('doc/students.txt', 'r')as fd:
    students = fd.read().split('&')


students_list = students
stu_lens = len(students)





#创建窗口
root = Tk()

# 设置窗口的标题
root.title("")

#修改主窗口的logo
# root.iconbitmap('img\maizi.ico')  #ico生成网站：http://www.ico.la/

##设置窗口是否可以变化长/宽，
root.resizable(width=True, height=True) #False不可变，True可变，默认为True


name=Frame(root,bg='#c0d2e9')

#标签组件
labelname =Label(name, text = "这是一个点名小程序",height=2,width=50,font=("微软雅黑", 10, "bold"),fg='white',bg='orange')
labelname.pack(side=TOP)


#学员列表
listb = Listbox(name,selectmode = BROWSE,bg='yellow', height=12,width=15,font=('Arial',10))
listb.pack(side=LEFT)  # 将小部件放置到主窗口中
for item in students_list[1:]:
    listb.insert(END, item)


#列表中显示已选过的学员
for selected_student in selected_students[1:]:
    index = students_list[1:].index(selected_student)
    listb.selection_set(index)

#添加列表的滚动条
sl = Scrollbar(name)
sl.set(0, 0.5)
sl.pack(side=LEFT, fill=Y)
listb['yscrollcommand'] = sl.set
sl['command'] = listb.yview


# 文本框,显示已往的记录
v = StringVar()
text = Text(name, width='40', height='10', fg='blue')
text.pack()
with open('doc/loginfo.txt', 'a+')as fg:
    text.insert(1.0, fg.read())



#输入框，添加学学员
entry = Entry(name, text='添加学员', width=12)
entry.place(x=130, y=182)


# 创建一个下拉列表
stu_list = StringVar()
stu_Chosen = ttk.Combobox(root, width=10, textvariable=stu_list)
stu_Chosen['values'] = students_list[1:]    # 设置下拉列表的值
stu_Chosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
stu_Chosen.place(x=270, y=182)



#按钮组件
for selected_student in selected_students:
    students.remove(selected_student)

#抽选
def btn1_clicked():

    with open('doc/students.txt', 'r')as f:
        students = f.read().split('&')

    with open('doc/logstu.txt','r')as f:
        selected_students = f.read().split('&')

    if len(selected_students) == len(students):

        listb.selection_clear(0, stu_lens)
        with open('doc/logstu.txt', 'r+')as fd:
            fd.truncate()
        tkMessageBox.showinfo(title="恭喜你被选中咯", message='重新开始')
    else:

        # 列表中执行选中操作
        for selected_student in selected_students[1:]:
            print selected_student
            index = students[1:].index(selected_student)
            listb.selection_set(index)

        for selected_student in selected_students:
            students.remove(selected_student)

        c_name = random.choice(students)

        with open('doc/logstu.txt', 'a')as fd:
            fd.write('&'+c_name)

        #记录
        with open('doc/loginfo.txt', 'a+')as fg:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info = '时间：'+time+'\t'+'学员：'+c_name+'\n'
            fg.write(info)
            print info
            text.insert(1.0, info)



        with open('doc/students.txt', 'r')as f:
            new_students = f.read().split('&')
        index = new_students[1:].index(c_name)
        listb.selection_set(index)

        # 弹出选中的人
        tkMessageBox.showinfo(title="恭喜你被选中咯", message=c_name)
        students.remove(c_name)


#重置
def btn2_clicked():
    global students
    listb.selection_clear(0, stu_lens)
    with open('doc/logstu.txt','w')as f:
        f.truncate()
    with open('doc/students.txt', 'r')as f:
        students = f.read().split('&')
    text.delete(1.0,END)

#添加
def btn3_clicked():

    add_student = entry.get()
    if add_student != '':
        listb.insert(END, add_student)

        print type(add_student)

        # 向文本写入数据
        with open('doc/students.txt', 'a')as f:
            f.write('&' +add_student.encode('utf-8'))

        with open('doc/students.txt', 'r+')as f:
            add_student_lists = f.read().split('&')

        # 更新下拉框
        stu_Chosen['values'] = add_student_lists[1:]   # 设置下拉列表的值
        stu_Chosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值



#删除
def btn4_clicked():

    with open('doc/students.txt','r')as f:
        students_list = f.read().split('&')


    # 更新列表
    rm_stu = stu_Chosen.get()
    rm_stu = rm_stu.encode('utf-8')
    index = students_list[1:].index(rm_stu)
    listb.delete(index)

    #更新下拉框
    students_list.remove(rm_stu)
    stu_Chosen['values'] = students_list[1:] #设置下拉列表的值
    stu_Chosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


    with open('doc/students.txt', 'w')as f:
        for student in students_list[1:]:
            f.write('&'+student)

    #更新logstu信息
    with open('doc/logstu.txt', 'r+')as f:
        students_log = f.read().split('&')

        if rm_stu in students_log:
            students_log.remove(rm_stu)

            if len(students_log) != 1:
                for new_logstu in students_log[1:]:
                    with open('doc/logstu.txt', 'w+')as f:
                        f.write('&' + new_logstu)


but3 = Button(name, text = "添加", width=5,command = btn3_clicked)
but3.place(x=220,y=180)

but4 = Button(name, text = "删除", width=5,command = btn4_clicked)
but4.place(x=365,y=180)

but1 = Button(name, text = "选择", width=10,command = btn1_clicked)
but1.place(x=160,y=220)

but2 = Button(name, text = "重置", width=10,command = btn2_clicked)
but2.place(x=300,y=220)



#必须设置这个，才能将其他控件装进frame框中
name.pack()
root.mainloop()

