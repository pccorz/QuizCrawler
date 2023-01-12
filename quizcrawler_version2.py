from xml.sax import default_parser_list
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import maskpass

class Q:
    def __init__(self):
        self.title = 'UN'
        self.tpe = 'UN'
        self.ans = []
# ansurl = 'https://docs.google.com/forms/d/e/1FAIpQLSch4RRpXGUeCN4PArZg0b3KbSj4tZVCsiDX9j7n5bJ2Ggv3yA/viewanalytics'
# formurl = 'https://docs.google.com/forms/d/e/1FAIpQLSch4RRpXGUeCN4PArZg0b3KbSj4tZVCsiDX9j7n5bJ2Ggv3yA/viewform'
ansurl = 'https://docs.google.com/forms/d/e/1FAIpQLSdgq2S6PHajiJNZPIbgX3Jb8HRF2suLl4yphDnvl0xw6Imc5w/viewanalytics'
formurl = 'https://docs.google.com/forms/d/e/1FAIpQLSdgq2S6PHajiJNZPIbgX3Jb8HRF2suLl4yphDnvl0xw6Imc5w/viewform?hr_submission=ChkIvsOd5-YKEhAIgKD9n_EQEgcIhoa65-YKEAA'

email = 'ck1100890@gl.ck.tp.edu.tw'
password = 'hehehe'
titleclass = 'M7eMe'

#.replace(u'\n',u'').replace(u'\xa0',u'').replace(u' ',u'')
chrome = ''
def Login():
    global email,password
    chrome.get('https://accounts.google.com/v3/signin/identifier?dsh=S-972875933%3A1672013913036171&hl=zh-tw&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AeAAQh6IJsqhC3os63jQ9MkZ2jtQJNLUYO1qh5WOTOs-_ezdN_HpCqAcDI6UUqX-MjuTm_K5nvF7')
    usrname = chrome.find_element_by_id('identifierId')
    usrname.send_keys(email)
    usrname.send_keys(Keys.ENTER)
    input('press enter when at password page')
    psw = chrome.find_element_by_name('Passwd')
    psw.send_keys(password)
    psw.send_keys(Keys.ENTER)

def GetAns(url):
    global chrome
    chrome.get(url)
    input('press enter when done')
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
    return;

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
        
def FillAns(url,refer):
    global chrome
    chrome.get(url)
    WaitForKey()
    while True:
        all = chrome.find_elements_by_class_name('Qr7Oae')
        for now in all:
            tar = now.find_element_by_class_name(titleclass).text.replace(u'\xa0',u'')
            tar = tar.replace(u'\n',u'').replace(u' ',u'')
            print(repr(tar))
            for j in range(len(refer)):
                if refer[j].title[:min(len(refer[j].title),len(tar))] == tar[:min(len(refer[j].title),len(tar))]:
                    if FillIn(now,refer[j]):
                        print('in')
                        refer.pop(j)
                        break
        WaitForKey()
        nxt = chrome.find_elements_by_css_selector('#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div')[-1]#find next button
        nxt.click()
        time.sleep(1.5)
    return

def Ask():
    global ansurl,formurl,email,password
    email = input('enter email:\n')
    password = maskpass.advpass()
    formurl = input('enter form link\n')
    ansurl = formurl[:formurl.find('viewform')]
    ansurl += 'viewanalytics'
    print(ansurl)

if __name__ == '__main__':
    Ask()
    chrome = webdriver.Chrome('./chromedriver')
    Login()
    WaitForKey()
    arr = GetAns(ansurl)
    WaitForKey()
    FillAns(formurl,arr)
