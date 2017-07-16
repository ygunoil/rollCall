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
with open('logstu.txt', 'r')as f:
    selected_students = f.read().split('&')

with open('students.txt', 'r')as fd:
    students = fd.read().split('&')


students_list=students
stu_lens=len(students)





#创建窗口
root = Tk()

# 设置窗口的标题
root.title("麦子学院专用点名程序")

#修改主窗口的logo
root.iconbitmap('img\maizi.ico')  #ico生成网站：http://www.ico.la/

##设置窗口是否可以变化长/宽，
root.resizable(width=True, height=True) #False不可变，True可变，默认为True


name=Frame(root,bg='#c0d2e9')

#标签组件
labelname =Label(name, text = "这是一个点名小程序",height=2,width=35,font=("Arial", 10, "bold"),fg='blue',bg='orange')
labelname.pack(side=TOP)


#学员列表
listb = Listbox(name,selectmode = BROWSE,bg='yellow', height=12,width=15,font=('Arial',10))
listb.pack(side=LEFT)  # 将小部件放置到主窗口中
for item in students_list:
    listb.insert(END, item)


#显示已选的学员
for selected_student in selected_students:
    index = students.index(selected_student)
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
with open('loginfo.txt','a+')as fg:
    text.insert(END, fg.read())



#输入框，添加学学员
entry=Entry(name,text='添加学员')
entry.place(x=130,y=182)

# 创建一个下拉列表
stu_list = StringVar()
stu_Chosen = ttk.Combobox(root, width=10, textvariable=stu_list)
stu_Chosen['values'] = students    # 设置下拉列表的值
# stu_Chosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
stu_Chosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
stu_Chosen.place(x=270,y=220)



#按钮组件
for selected_student in selected_students:
    students.remove(selected_student)


def btn1_clicked():
    global students
    if len(students) != 0:
        c_name = random.choice(students)


        #记录被选中的学生的信息
        with open('logstu.txt', 'r')as f:
            s= f.read().split('&')
            if len(s)==stu_lens-1:
                with open('logstu.txt', 'r+')as fd:
                    fd.truncate()
            else:
                with open('logstu.txt', 'a')as fd:
                    fd.write('&'+c_name)

        #记录
        with open('loginfo.txt', 'a+')as fg:
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info='时间：'+time+'\t'+'学员：'+c_name+'\n'
            fg.write(info)
            print info
            text.insert(1.0, info)
            # text.insert(END, ' ')


            # 列表中执行选中操作
        with open('students.txt', 'r')as f:
            new_students = f.read().split('&')

        name_list = new_students
        index = name_list.index(c_name)
        listb.selection_set(index)



        # 弹出选中的人
        tkMessageBox.showinfo(title="恭喜你被选中咯", message=c_name)

        students.remove(c_name)

    else:

        listb.selection_clear(0, stu_lens)
        tkMessageBox.showinfo(title="恭喜你被选中咯", message='重新开始')

        with open('students.txt', 'r')as f:
            students = f.read().split('&')



def btn2_clicked():
    global students
    listb.selection_clear(0, stu_lens)
    with open('logstu.txt','w')as f:
        f.truncate()
    with open('students.txt', 'r')as f:
        students = f.read().split('&')
    text.delete(1.0,END)

def btn3_clicked():
    add_student=entry.get()
    listb.insert(END, add_student)
    with open('students.txt','a')as f:
        f.write('&'+add_student.encode('utf-8'))
def btn4_clicked():
    global students_list
    rm_stu=stu_Chosen.get()
    rm_stu=rm_stu.encode('utf-8')
    print rm_stu
    index = students_list.index(rm_stu)


    students_list.remove(rm_stu)
    # listb.selection_set(index)
    listb.delete(index)


    with open('students.txt', 'w')as f:
        for student in students:
            f.write('&'+student)


but3 = Button(name, text = "添加", width=5,command = btn3_clicked)
but3.place(x=280,y=180)

but4 = Button(name, text = "删除", width=5,command = btn4_clicked)
but4.place(x=340,y=180)

but1 = Button(name, text = "选择", width=5,command = btn1_clicked)
but1.place(x=180,y=220)

but2 = Button(name, text = "重置", width=5,command = btn2_clicked)
but2.place(x=240,y=220)



#必须设置这个，才能将其他控件装进frame框中
name.pack()
root.mainloop()