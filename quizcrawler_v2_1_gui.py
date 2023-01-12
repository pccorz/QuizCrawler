# from xml.sax import default_parser_list
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
# import maskpass
import tkinter as tk
import re as reg
import webbrowser
from tkinter import ttk

class Q:
    def __init__(self):
        self.title = 'UN'
        self.tpe = 'UN'
        self.ans = []

ansurl = 'https://docs.google.com/forms/d/e/1FAIpQLSdgq2S6PHajiJNZPIbgX3Jb8HRF2suLl4yphDnvl0xw6Imc5w/viewanalytics'
formurl = 'https://docs.google.com/forms/d/e/1FAIpQLSdgq2S6PHajiJNZPIbgX3Jb8HRF2suLl4yphDnvl0xw6Imc5w/viewform?hr_submission=ChkIvsOd5-YKEhAIgKD9n_EQEgcIhoa65-YKEAA'

email = 'ck1100ddd@gl.ck.tp.edu.tw'
password = 'testpwd'
titleclass = 'M7eMe'

#.replace(u'\n',u'').replace(u'\xa0',u'').replace(u' ',u'')
chrome = ''
def Login(number):
    global email, password, chrome
    if number == 1:
        chrome.get('https://accounts.google.com/v3/signin/identifier?dsh=S-972875933%3A1672013913036171&hl=zh-tw&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AeAAQh6IJsqhC3os63jQ9MkZ2jtQJNLUYO1qh5WOTOs-_ezdN_HpCqAcDI6UUqX-MjuTm_K5nvF7')
        usrname = chrome.find_element_by_id('identifierId')
        usrname.send_keys(email)
        usrname.send_keys(Keys.ENTER)
    elif number == 2:
    # input('press enter when at password page')
        psw = chrome.find_element_by_name('Passwd')
        psw.send_keys(password)
        psw.send_keys(Keys.ENTER)

def GetAns(url, number):
    global chrome
    if number == 1:
        chrome.get(url)
    #input('press enter when done')
    else:
        soup = BeautifulSoup(chrome.page_source,'html.parser')
        arr = []
        details = soup.find_all(class_ = 'Aovyg')
        dels = []
        for i in range(len(details)):
            if len(details[i].find_all('table')) == 0 and len(details[i].find_all(class_ = 'NC79P')) == 0:
                dels.append(i);
        dels.reverse()
        for i in dels:
            details.pop(i)
        # print(len(details))
        # for i in details:
        #     print(i.text)
        #     print('')
    
        for i in details:
            tmp = Q()
            tmp.title = i.find(class_ = 'myXFAc RjsPE').text.replace(u'\xa0',u'')
            tmp.title = tmp.title.replace(u'\n',u'').replace(u' ',u'')
            isbox = False
            if i.find('table') != None:
                for j in i.find('table').find('tbody').find_all('tr'):
                    tmp.ans.append([])
                    for k in j.find_all('td'):
                        tmp.ans[-1].append(k.text)
                    if len(tmp.ans[-1]) >2:
                        isbox = True
            else:
                tmp.tpe = 'long'
                tmp.ans = i.find(class_='NC79P').text+' ';
            if isbox:
                tmp.tpe = 'box'
                choices = []
                for j in i.find('table').find('thead').find_all('th'):
                    if len(j.text) == 0:
                        continue
                    choices.append(j.text)
                for j in range(len(tmp.ans)):
                    biggest = 1
                    for k in range(1,len(tmp.ans[j]),1):
                        if int(tmp.ans[j][k])>int(tmp.ans[j][biggest]):
                            biggest = k
                    tmp.ans[j] = [tmp.ans[j][0].replace(u'\xa0',u'').replace(u'\n',u'').replace(u' ',u''),biggest-1]
            arr.append(tmp);
        for i in arr:
            print(repr(i.title),end=":")
            if type(i.ans) == str:
                print(repr(i.ans))
            else:
                for j in i.ans:
                    print(repr(j),end=',')
            print('')
        return arr

def WaitForKey():
    input('press enter to continue')

    
def InfoTop():
    tk.messagebox.showinfo(title="Entering Personal Info", message='You can enter your email / Student ID # / Last 3 Digits of your ID No., e.g., ck11000890@gl.ck.tp.edu.tw / 11000890 / 890 are all acceptable')

def TogglePwd():
    global pwdHide
    pwdHide = 1 - pwdHide
    entryPwd.config(show="\u2022"*pwdHide)
    root.update_idletasks()

def webOpen(url):
    #ansurl = entryLink.get()[:formurl.find('viewform')]+= 'viewanalytics'
    #ansurl += 'viewanalytics'
    webbrowser.open(url)

def githubOpen():
    webbrowser.open('pccorz.github.io')

def FillIn(now,re):
    global chrome
    # print(re.tpe)
    if re.tpe == 'long':
        blank = now.find_elements_by_xpath('.//textarea')
        if len(blank) == 0:
            blank = now.find_elements_by_xpath('.//input')
        else:
            return False
        blank[0].send_keys(re.ans)
    elif re.tpe == 'box':
        # now = now.find_element_by_class_name()
        rows = now.find_elements_by_class_name('lLfZXe')
        # rows.pop(0)
        # rows.pop(0)
        print(len(rows))
        if len(rows) == 0:
            return False
        for i in rows:
            choices = i.find_elements_by_xpath('.//*[@jsaction]')
            choices = i.find_elements_by_class_name('Od2TWd')
            # choices.pop(0)
            print(len(choices))
            # for j in choices:
                # print(j.text)
                # j.click()
                # print('hi')
            print()
            choices[int(re.ans[0][1])].send_keys(Keys.SPACE)
            re.ans.pop(0)
    elif len(now.find_elements_by_class_name('Y6Myld')) > 0:
        re.tpe = 'multi';
        choices = []
        big = 0;
        for i in re.ans:
            big = max(big,int(i[1]))
        for i in re.ans:
            if int(i[1])>big*0.8:
                choices.append(i[0].replace(u'\n',u'').replace(u'\xa0',u'').replace(u' ',u''))
        selections = now.find_elements_by_xpath('.//*[@role="list"]//label')
        for i in selections:
            if i.find_element_by_class_name('ulDsOb').text.replace(u'\xa0',u'').replace(u'\n',u'').replace(u' ',u'') in choices:
                button = i.find_element_by_xpath('.//*[@id]')
                button.click()
    elif len(now.find_elements_by_class_name('SG0AAe')) > 0:
        re.tpe = 'choice'
        big = re.ans[0];
        for i in re.ans:
            if int(big[1])<int(i[1]):
                big = i
        # print('choice in')
        selections = now.find_elements_by_xpath('.//span//label')
        for i in selections:
            # print(k.find_element_by_class_name('ulDsOb').text)
            if i.find_element_by_class_name('ulDsOb').text.replace(u'\xa0',u'').replace(u'\n',u'').replace(u' ',u'') == big[0].replace(u'\n',u'').replace(u'\xa0',u'').replace(u' ',u''):
                button = i.find_element_by_xpath('.//*[@id]')
                button.click()        
    elif len(now.find_elements_by_class_name('jgvuAb')) > 0:
        re.tpe = 'list'
        big = re.ans[0]
        for i in re.ans:
            if int(big[1])<int(i[1]):
                big = i;
        # print('list in')
        first_one = now.find_element_by_xpath('.//*[@class = "MocG8c HZ3kWc mhLiyf LMgvRb KKjvXb DEh1R"]')
        first_one.send_keys(Keys.ENTER)
        time.sleep(0.3)
        # choices = i.find_elements_by_xpath('.//*[@class = "MocG8c HZ3kWc mhLiyf LMgvRb"]')
        choices = now.find_elements_by_xpath('.//*[@class = "MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
        for c in choices:
            # print(c.find_element_by_xpath('.//span').text)
            if c.find_element_by_xpath('.//span').text == big[0].replace(u'\n',u'').replace(u'\xa0',u'').replace(u' ',u''):
                c.send_keys(Keys.ENTER)
                time.sleep(0.3)
                break
    elif len(now.find_elements_by_class_name('whsOnd')) > 0:
        re.tpe = 'cloze'
        big =re.ans[0];
        for i in re.ans:
            if int(big[1])<int(i[1]):
                big = i
        blank = now.find_element_by_xpath('.//input')
        blank.send_keys(Keys.BACK_SPACE)
        blank.send_keys(big[0])
        blank.send_keys(Keys.ENTER)
    else:
        print("ERROR")
        return False
    print(re.tpe)
    return True
        
def FillAns(url, refer, formSection):
    global chrome
    # print(taskSection)
    if formSection == 1:
        chrome.get(url)
    # WaitForKey()
    #while True:
    else:
        if formSection >= 3:
            nxt = chrome.find_elements_by_css_selector('#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div')[-1]#find next button
            nxt.click()
            time.sleep(1.5)
        all_ = chrome.find_elements_by_class_name('Qr7Oae')
        for now in all_:
            tar = now.find_element_by_class_name(titleclass).text.replace(u'\xa0', u'')
            tar = tar.replace(u'\n',u'').replace(u' ',u'')
            print(str(tar))
            for j in range(len(refer)):
                if refer[j].title[:min(len(refer[j].title),len(tar))] == tar[:min(len(refer[j].title),len(tar))]:
                    if FillIn(now,refer[j]):
                        print('in')
                        refer.pop(j)
                        break
    return

def Ask():
    global ansurl, formurl, email, password
    email = entryEmail.get()
    if reg.match(r'ck1100\d{3}@gl.ck.tp.edu.tw', email):
        pass
    elif reg.match(r'\d{3}', email):
        email = f"ck1100{email}@gl.ck.tp.edu.tw"
    elif reg.match(r'\d{7}', email):
        email = f"ck{email}@gl.ck.tp.edu.tw"
    elif reg.match(r'\d{8}', email):
        email = email[:4] + email[5:]
        email = f"ck{email}@gl.ck.tp.edu.tw"
    else:
        email = 'error'
    password = entryPwd.get()
    formurl = entryLink.get()
    ansurl = formurl[:formurl.find('viewform')]
    ansurl += 'viewanalytics'
    
    '''email = input('enter email:\n')
    password = maskpass.advpass()
    formurl = input('enter form link\n')
    ansurl = formurl[:formurl.find('viewform')]
    ansurl += 'viewanalytics'
    print(ansurl)'''
    

def Continue():
    global ansurl, formurl, email, password, chrome, taskSection, arr, formSection
    taskSection += 1
    if taskSection == 1:
        statusVar.set("Press Continue when at password page")
        Ask()
        isLink = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        if email== 'error' or (not reg.match(isLink, formurl)):
            taskSection = 0
            return
        else:
            chrome = webdriver.Chrome('./chromedriver')
            Login(1)
    elif taskSection == 2:
        statusVar.set("Press Continue when page finish loading...")
        Login(2)
    elif taskSection == 3:
        statusVar.set("Press Continue again when page finish loading...")
        GetAns(ansurl, 1)
    elif taskSection == 4:
        statusVar.set("")
        root.update_idletasks()
        statusVar.set("Please wait patiently while loading... Fetching answers...")
        root.update_idletasks()
        arr = GetAns(ansurl, 2)
        statusVar.set("Done! Press Continue...")
    elif taskSection >= 5:
        if taskSection==5: statusVar.set("Make sure the form is empty!...")
        else: statusVar.set('Entering the answers...') 
        formSection += 1
        # statusVar.set("Entering the answers...")
        root.update_idletasks()
        FillAns(formurl,arr, formSection)
        if taskSection>=6: statusVar.set("Press Continue...")


arr = []
taskSection = 0
formSection = 0
pwdHide = 1

root = tk.Tk()
win = tk.Frame(root)
root.title("Quiz Crawler")
root.resizable(False, False)
statusVar = tk.StringVar()
statusVar.set('Press the button to continue') 

title = tk.Label(root, text="Quiz Crawler", font=("Helvetica", 15))
title.grid(column=0,row=0, padx=10, pady=10, columnspan=3)
separator = ttk.Separator(root, orient='horizontal')
separator.grid(column=0,row=1,columnspan=3,sticky="ew", pady=5)

labelEmail = tk.Label(root, text="Enter Prsn Info:")
labelEmail.grid(column=0,row=2,sticky='e', padx=10, pady=4)
entryEmail = tk.Entry(root, width=25)
entryEmail.grid(column=1,row=2,sticky='w', pady=4)
btnEmailNote = tk.Button(root, text='?', command=InfoTop, width=2,relief='groove')
btnEmailNote.grid(column=2,row=2, padx=5)

labelPwd = tk.Label(root, text="Enter password:")
labelPwd.grid(column=0,row=3,sticky='e', padx=10, pady=4)
entryPwd = tk.Entry(root, width=25, show="\u2022"*pwdHide)
entryPwd.grid(column=1,row=3,sticky='w', pady=4)
btnShowPwd = tk.Button(root, text='\uD83D\uDC41', width=2, command=TogglePwd,relief='groove')
btnShowPwd.grid(column=2,row=3, padx=5)

labelLink = tk.Label(root, text="Enter form link:")
labelLink.grid(column=0,row=4,sticky='e', padx=10, pady=4)
entryLink = tk.Entry(root, width=25)
entryLink.grid(column=1,row=4,columnspan=3,sticky='w', pady=4)
btnToLink = tk.Button(root, text='\u29C9', width=2, command=lambda:webOpen(entryLink.get()[:formurl.find('viewform')]+ 'viewanalytics'),relief='groove')
btnToLink.grid(column=2,row=4, padx=5)

statuslbl = tk.Label(root, textvariable=statusVar, fg='green')
statuslbl.grid(column=0,row=5,columnspan=3)
btnContinue = tk.Button(root, text="Continue", command=Continue)
btnContinue.grid(column=0,row=6,columnspan=3,pady=4)
separator = ttk.Separator(root, orient='horizontal')
separator.grid(column=0,row=7,columnspan=3,sticky="ew")
footnotelbl = tk.Label(root, text='pccorz.github.io   |   ver. 2.1', fg='gray')
footnotelbl.bind("<Button-1>", lambda e:webOpen('https://pccorz.github.io/'))
footnotelbl.grid(column=0,row=8,columnspan=3, pady=3)

root.mainloop()
