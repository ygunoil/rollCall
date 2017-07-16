#!/usr/bin/python
# -*- coding: UTF-8 -*-
#运行环境 python2.7
#author：hx

from Tkinter import *
import tkMessageBox
import random
import datetime
import ttk

#共同变量或函数
create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#操作文本函数，用于读和写的操作
def operate_txt(name, type, content):
    if type == 'w'or type == 'a' or type == 'w+' or type == 'a+':
        with open('doc/' + name + '.txt', type)as f:
            f.write(content+'\n')

    elif type == 'r' or type == 'r+':
        with open('doc/'+name+'.txt', 'r+')as f:
            data = f.read().split('\n')
        return data
    else:
        print '输入正确的文件操作类型'


#验证函数，用于输入和选择数据验证
def validate_data(textname, data, typename):
    text = operate_txt(textname, 'r', '')[:-1]
    print '验证数据是否在文本中', type(text),text

    if typename == 'in':
        #选择验证
        if data in text:
            return True
        else:
            tkMessageBox.showinfo('这是一个坏消息', message='不存在')
            return False
    else:
        #输入验证
        if data in text:
            category_var.set('')
            student_var.set('')
            tkMessageBox.showinfo('这是一个坏消息', message='已经存在')
            return False
        else:
            category_var.set('')
            student_var.set('')
            return True


def select_category_func():
    global students_list, selected_students, selected_category

    selected_category = chose_category.get()
    print "选择的类型", type(selected_category),selected_category
    validate_rusult=validate_data('category', selected_category.encode('utf-8'), 'in')

    if validate_rusult == True:
        # 改变主窗口label
        labelvar.set('这是一个关于' + selected_category.encode('utf-8') + '的小程序')

        # 读取学员
        listbox.selection_clear(0, END)
        selected_students = operate_txt(selected_category, 'r', '')
        for selected_student in selected_students[1:-1]:
            index = students_list[:-1].index(selected_student)
            listbox.selection_set(index)

        #读取log日志
        text.delete(1.0, END)
        logs = operate_txt((selected_category.encode('utf-8')+'log').decode('utf-8'), 'r', '')[:-1]
        for log in logs:
            text.insert(1.0, log+'\n')
        child.withdraw()
        root.deiconify()


def delete_category_func():
    deleted_category = chose_category.get().encode('utf-8')
    categorys = operate_txt('category', 'r', '')
    print '删除的类',type(deleted_category),deleted_category
    print '类文本情况',categorys
    validate_rusult = validate_data('category', deleted_category, 'in')

    if validate_rusult==True:
        if len(categorys) != 2:
            categorys.remove(deleted_category)

            # 更新分类下拉框
            chose_category['values'] = categorys[:-1]
            chose_category.current(0)

            #更新文本信息
            with open('doc/category.txt', 'a+') as f:
                f.truncate()
                for category in categorys[:-1]:
                    f.write(category+'\n')
        else:
            tkMessageBox.showinfo(title="这是一个坏消息", message='彻底删除的行为是被禁止的')



def add_category_func():
    category = entry_category.get().encode('utf-8')
    print '添加的类',type(category), category
    validate_rusult = validate_data('category', category, 'not in')

    if validate_rusult==True:
        if category != '':
            #创建点名类,添加默认值(创建时间)
            operate_txt("category", 'a+', category)
            operate_txt(category.decode('utf-8'), 'w', '创建时间'+create_time)
            operate_txt((category+'log').decode('utf-8'),'w','创建时间:'+create_time)

            # 改变主窗口label
            labelvar.set('这是一个关于' + category + '的小程序')

            # 更新分类下拉列表
            categorys = operate_txt('category', 'r', '')[:-1]
            chose_category['values'] = categorys
            chose_category.current(0)
            print '所有的类', categorys

            # 读取学员信息
            listbox.selection_clear(0, END)
            selected_students = operate_txt(category.decode('utf-8'), 'r', '')
            for selected_student in selected_students[1:-1]:
                index = students_list[:-1].index(selected_student)
                listbox.selection_set(index)
        else:
            tkMessageBox.showinfo(title="这是一个坏消息", message='输入为空的行为是被禁止的')


# 创建窗口
root = Tk()

# 设置窗口的标题
root.title("我是一个点名器2.0")

# 设置窗口是否可以变化长/宽，
root.resizable(width=False, height=False)

#-----------选择事件子窗口---------------------------
child = Toplevel(bg='#15dbe7')

child.resizable(width=False, height=False)
# child.geometry('200x150')
Label(child, text='请输入或选择点名事件类型', height=2,fg='white',width='25',bg='orange',font=("微软雅黑", 10, "bold")).pack()

#输入框，添加分类
category_var = StringVar()
entry_category = Entry(child, textvariable=category_var, width=20)


# 创建一个分类下拉列表
categorys = operate_txt('category', 'r', '')
category_list = StringVar()
chose_category = ttk.Combobox(child, width=17, textvariable=category_list)
chose_category['values'] = categorys[:-1]    # 设置下拉列表的值
chose_category.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


# 控件布局
chose_category.pack()

but1 = Button(child, text="选择", width=5, command=select_category_func)
but1.pack()

but2 = Button(child, text="删除", width=5, command=delete_category_func)
but2.pack()

entry_category.pack()

but3 = Button(child,  text="添加", width=5, command=add_category_func)
but3.pack()



#-------------学员添加子窗口---------------
son = Toplevel(bg='#15dbe7')

son.resizable(width=False, height=False)
# son.geometry('200x150')

Label(son, text='增加或删除学员', height=2, width='25', fg='white', bg='orange',font=("微软雅黑", 10, "bold")).pack()

# 添加学员输入框
student_var =StringVar()
entry_student = Entry(son, textvariable=student_var, width=20)


# 创建一个学员下拉列表
students_list = operate_txt('students', 'r', '')
stu_list = StringVar()
chose_student = ttk.Combobox(son, width=17, textvariable=stu_list)
chose_student['values'] = students_list[:-1]    # 设置下拉列表的值
chose_student.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值



def add_student_func():
    global selected_category
    add_student = entry_student.get().encode('utf-8')
    print '添加的学员',type(add_student),add_student
    validate_rusult = validate_data('students', add_student, 'not in')

    if validate_rusult==True:
        if add_student != '':
            #更新学员列表
            listbox.insert(END, add_student)

            # 向文本写入数据
            operate_txt('students', 'a+', add_student)

            # 更新学员下拉列表
            students = operate_txt('students', 'r', '')
            chose_student['values'] = students[:-1]
        else:
            # tkMessageBox.showinfo(title="这是一个坏消息", message='输入为空的行为是被禁止的')
            son.withdraw()

def delete_student_func():
    global students_list, selected_category

    students_list = operate_txt('students', 'r', '')
    deleted_student = chose_student.get().encode('utf-8')
    print '被删除的学员',type(deleted_student),deleted_student
    print '剩余的学员',students_list
    validate_rusult = validate_data('students', deleted_student, 'in')


    if validate_rusult==True:
        if len(students_list) != 2:
            # 更新学员列表
            index = students_list[:-1].index(deleted_student)
            listbox.delete(index)

            # 更新下拉框
            students_list.remove(deleted_student)
            chose_student['values'] = students_list[:-1]  # 设置下拉列表的值
            chose_student.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

            # 更新学员文本信息
            with open('doc/students.txt', 'a+')as f:
                f.truncate()
                for student in students_list[:-1]:
                    f.write(student+'\n')

            #删除所有类文本里面的被删除的学员
            categorys = operate_txt('category', 'r', '')[:-1]
            for category in categorys:
                print '更新所有类',type(category), category
                selected = operate_txt(category.decode('utf-8'), 'r', '')
                if deleted_student in selected:
                    selected.remove(deleted_student)
                    with open('doc/' + category.decode('utf-8')+'.txt', 'a+')as f:
                        f.truncate()
                        for selected_student in selected[:-1]:
                            f.write(selected_student+'\n')

            # 重新执行选中操作
            selected_students = operate_txt(selected_category, 'r', '')
            for selected_student in selected_students[1:-1]:
                index = students_list[:-1].index(selected_student)
                listbox.selection_set(index)
        else:
            tkMessageBox.showinfo('这是一个坏消息',message='彻底删除的行为是不被允许的')
            son.withdraw()



#学员增删控件布局
entry_student.pack()

but4 = Button(son,  text="添加", width=5, command=add_student_func)
but4.pack()


chose_student.pack()

but5 = Button(son, text="删除", width=5, command=delete_student_func)
but5.pack()





#启动时，就隐藏主窗口和学员增删窗口。
# child.withdraw()
son.withdraw()
root.withdraw()

#-------------------主窗口-----------------------
# 创建容器
frame = Frame(root, bg='#15dbe7')

#初始数据
selected_students = ['何喜']
# students_list = ['何喜','夏微波','何喜','夏微波','何喜','夏微波','何喜','夏微波','何喜','夏微波']

#标签组件
labelvar=StringVar()
labelname = Label(frame, textvariable=labelvar, text="这是一个点名小程序",height=2,width='52',font=("微软雅黑", 10, "bold"),fg='white', bg='orange')
labelvar.set("这是一个点名小程序")
labelname.pack()



#学员列表
students_list = operate_txt('students', 'r', '')
listbox = Listbox(frame,  selectmode=MULTIPLE,  bg='#15dbe7', height=15, width=15, font=('Arial', 10))
listbox.pack(side=LEFT)  # 将小部件放置到主窗口中
for item in students_list[:-1]:
    listbox.insert(END, item)

#列表上的鼠标点击对选择框的影响
def click_list(event):
    global selected_students
    for selected_student in selected_students[1:-1]:
        index = students_list[1:-1].index(selected_student)
        listbox.selection_set(index)

listbox.bind('<Button-1>', click_list)

#列表中显示已选过的学员
for selected_student in selected_students[1:]:
    index = students_list[1:].index(selected_student)
    listbox.selection_set(index)

#添加列表的滚动条
sl = Scrollbar(frame)
sl.set(0, 0.5)
sl.pack(side=LEFT, fill=Y)
listbox['yscrollcommand'] = sl.set
sl['command'] = listbox.yview


# 文本框,显示已往的记录
v = StringVar()
text = Text(frame, width='40', height='15', fg='blue')
text.pack()


def category_func():
    try:
        child.deiconify()
    except TclError:
        tkMessageBox.showinfo('这是一个坏消息',message='你已经彻底关闭了窗口，暂时无法打开，我们正在努力开发过程中。')


def add_or_delete_func():
    try:
        son.deiconify()
    except TclError:
        tkMessageBox.showinfo('这是一个坏消息',message='你已经彻底关闭了窗口，暂时无法打开，我们正在努力开发过程中。')


def choose_func():
    global students_list, selected_category
    students = operate_txt('students', 'r', '')
    students_list = operate_txt('students', 'r', '')
    selected_students = operate_txt(selected_category, 'r', '')

    if len(selected_students[1:]) == len(students):
        listbox.selection_clear(0, END)
        with open('doc/'+selected_category+'.txt', 'w+')as f:
            f.truncate()
            f.write(create_time+'\n')
        tkMessageBox.showinfo(title="你是一个幸运宝宝", message='从头再来')
    else:
        #从未选中的学员中随机选者
        for selected_student in selected_students[1:]:
            students.remove(selected_student)
        c_name = random.choice(students)
        print '幸运宝宝', c_name

        #更新类文本
        operate_txt(selected_category, 'a+', c_name)

        #更新列表
        index = students_list[:-1].index(c_name)
        listbox.selection_set(index)

        #更新log记录
        info = '时间:'+create_time+'\t'+selected_category.encode('utf-8')+'\t'+c_name
        operate_txt((selected_category.encode('utf-8')+'log').decode('utf-8'), 'a+', info)
        text.insert(1.0, info+'\n')

        # 弹出选中的人
        tkMessageBox.showinfo(title="你是一个幸运宝宝", message=c_name)

def reset_func():
    global selected_category

    #清空被选学员的信息
    listbox.selection_clear(0, END)
    with open('doc/' + selected_category + '.txt', 'w+')as f:
        f.truncate()
        f.write(create_time + '\n')

    # 清空所有日志信息
    text.delete(1.0, END)
    with open('doc/'+selected_category+'log.txt', 'w')as f:
        f.truncate()




but5 = Button(frame, text="点名类型", width=10, command=category_func)
but5.pack(side=LEFT, padx=5)

but6 = Button(frame, text="学员增删", width=10, command=add_or_delete_func)
but6.pack(side=LEFT, padx=5)

but7 = Button(frame, text="选择", width=5, command=choose_func)
but7.pack(side=LEFT, padx=5)

but8 = Button(frame, text="重置", width=5, command=reset_func)
but8.pack(side=LEFT, padx=5)

frame.pack()
root.mainloop()