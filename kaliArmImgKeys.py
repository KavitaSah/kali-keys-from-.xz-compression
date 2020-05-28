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

list_values=list(my_dictionary.values())
zip_list = list_values[0]
xz_img_list = list_values[1]
ova_list = list_values[2]
z7_list = list_values[3]

temp_list =[xz_img_list[17],xz_img_list[18]]

print(temp_list)  #prints 17th and 18th .img.xz files

#Removing .xz to add to the final_dict
img_files = list()  #removes .xz from the image name
for i in xz_img_list:
    a = i.split('/')
    b = a[-1].split('.xz')
    img_files.append(b[0])
print(img_files)    

#For testing, appending only two files
temp_img_files = list()
temp_img_files.append(img_files[15])
temp_img_files.append(img_files[17])
temp_img_files.append(img_files[18])
temp_img_files
print(temp_img_files)

#Downloading the zip files
block_size =1024
for i in temp_img_list:
    url = i
    filename = 'tempfile.img.xz'
    file = requests.get(url, stream=True)   #Stream =True avoids reading the content all at once into memory
    total_size = int(file.headers.get('content-length', 0))
    t = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as f:
        for data in file.iter_content(block_size):
            t.update(len(data))
            f.write(data)
            
    #extracting .img from .xz, mounting, extarcting the keys and unmounting it:
    #filename = 'kali-linux-2020.1-bananapro.img.xz'
    #a = 'kali-linux-2020.1-bananapro.img'
    decompress = 'unxz --keep '+ filename
    os.system(decompress)
    a = filename[:-3]
    print (a)
    os.system('losetup /dev/loop14 '+ a)  #mounts the image at loop5
    os.system('kpartx -a /dev/loop14')  #Creates device map from partition table
    os.system('mount /dev/mapper/loop14p1 SKO') #Mounts the image in the mentioned mountpoint
    os.system('cd SKO/etc/ssh')
    print(os.getcwd())
    b='/home/kavitas/SKO/etc/ssh'
    os.chdir(b)
    #os.system('ls')
    #print(os.getcwd())
    #b_files = list() #list of keys
    b_files = os.listdir() #list of files in SKO/etc/ssh
    print(f' Files in this dir are: {b_files}')
    host_files = list()
    for m in b_files:  #Loop to get only ssh_host* files
        if 'host' in m:
            host_files.append(m)
    print(host_files)
    actual_keys = list()
    for i in host_files:  #iterating over keys and reading them
        with open (i, 'r') as f:
            actual_keys.append(f.read()) #appending keys to c
    print(actual_keys)
    dict_ssh = dict(zip(host_files,actual_keys)) #zip actual keys and key filename
    print (dict_ssh)
    dict_final = dict()
    for r in temp_img_files:
        dict_final[r] = dict_ssh
print(dict_final)

#import pandas as pd
#df = pd.DataFrame(dict_final)
#df.to_csv("Kali_Img_Images.csv")

home_dir = '/home/kavitas'
os.chdir(home_dir)
print(os.getcwd())
print('unmounting files.....')
os.system('sudo umount SKO')
os.system('sudo kpartx -d /dev/loop14')
os.system('sudo losetup -d /dev/loop14')
print('unmounted files')


