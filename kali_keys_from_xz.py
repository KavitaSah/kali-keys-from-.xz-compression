import requests
import csv
from bs4 import BeautifulSoup
import re
from multiprocessing.pool import ThreadPool
import webbrowser    #to convert links to hyperlink
import os
import urllib.request
import imagemounter
import tqdm
from zipfile import ZipFile
import os
import tarfile


urls= ('https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/' ,'https://www.offensive-security.com/kali-linux-arm-images/', 'https://www.offensive-security.com/kali-linux-nethunter-download/')

extensions = ['zip','xz','ova','7z']
def Convert(string):
    li = list(string.split(" "))
    return li

def add_extensions(url_t):
    #lists_namelist=list()
    list_name=list()    #to store "list of zip" etc as keys in dictionary
    temp_extensions=list()
    for i in extensions:
        temp_name = "list_of_"+i
        list_name.append(temp_name)
        temp_extensions.append(i+"$")    #adds $ to the extension name to be accessed by href to access the string that ends with $
    myDictionary = {}
    for i in range(len(extensions)):
        lists_links = list()   #to store list of URLs
        for link in url_t:
            page = requests.get(link, allow_redirects=True)  #create HTTP response object
            soup = BeautifulSoup(page.text, 'html.parser')
            for b in soup.find_all('a', href = re.compile(temp_extensions[i])):    #similar to re.compile("zip$")
                lists_links.append(b['href'])
                #print (b)
            myDictionary[list_name[i]]=lists_links

    return myDictionary

#print(add_extensions(url))
my_dictionary=add_extensions(urls)
#my_dictionary.keys()
#my_dictionary
#print (v[0])

list_values=list(my_dictionary.values())
zip_list = list_values[0]
xz_list = list_values[1]
ova_list = list_values[2]
z7_list = list_values[3]

#Taking actual kali images name
name_of_files = list()
for i in zip_list:
    a = i.split('/')
    b = a[-1].split('.zip')
    name_of_files.append(b[0])

from zipfile import ZipFile
import os
import tarfile
b = os.getcwd()
b = b + '/' + 'KALI_FINAL_TAR'
print(b)
os.mkdir(b)
os.chdir(b)

#Downloading the zip files
block_size =1024
for i in zip_list:
    url = i
    filename = 'tempfile_new.zip'
    file = requests.get(url, stream=True)   #Stream =True avoids reading the content all at once into memory
    total_size = int(file.headers.get('content-length', 0))
    t = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as f:
        for data in file.iter_content(block_size):
            t.update(len(data))
            f.write(data)


    #Extract from zip file, extract just etc folder from tar.xz file

    with ZipFile(filename, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            if fileName.endswith('.xz'):
                a = os.path.abspath(fileName)
                print(a)
                #print(os.path.abspath(fileName))  #
                zipObj.extract(fileName)
                a = a.split('/')
                print(a[-1])
                tarto_1 = '"kali-armhf/etc/ssh/ssh_host_*"'
                tarto_2 = '"kali-arm64/etc/ssh/ssh_host_*"'
                tarfrom = 'tar xvzf '+a[-1]
                print(tarfrom)
                if '64' in tarfrom:
                    tarto = tarto_2
                else:
                    tarto = tarto_1
                command = tarfrom + ' ' + tarto
                print(command)
                os.system(command)
                print(os.getcwd)
                b = os.getcwd()
                temp = a[-1].split('-')
                temp_new = 'kali' + '-' + temp[1]
                b = b + '/' + temp_new + '/' + 'etc' + '/' +'ssh'
                os.chdir(b)
                print(os.getcwd())
                b_files=list()
                b_files = os.listdir()
                c = list()
                for i in b_files:
                    with open (i, 'r') as f:
                        c.append(f.read())
                # creating dictionary of ssh file name with ssh key
                dict_ssh_val = dict(zip(b_files,c))  #zips two lists to form a dictionary
                dict_final = dict()
                for i in name_of_files:
                    dict_final[i] = dict_ssh_val
print(dict_final)
import pandas as pd
df = pd.DataFrame(dict_final)
df.to_csv("zipall.csv")

