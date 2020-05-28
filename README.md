# kali-keys-from-.xz-compression
Kali linux images come in various formats and is supported on many platforms such as VMware, virtualbox, hyper-v, arm-devices, nethunter etc.
The SSH keys are different for each of the images in the below mentioned types.

This code extracts SSH keys from the following type of kali linux images:
1. Kali linux VMware images
2. Kali linux Virtualbox images
3. Kali linux Nethunter images (They have .zip compression)
4. Kali Linux Arm images (They have .img compression)

Each of the type has different mounting process in the OS for keys extraction. 
The code has divided into 6 parts:
1. Web scraping ( I used beautiful soup).
2. Downloading the links obtained.
3. Decompressing the images (They are either xz or zip compressed)
4. Mounting the images (Nethunter images didn't require mounting)
5. Extracting the keys
6. Unmount the image (You don't want to save all the images as they are almost 2-3 GB each)

I tried using "imagemounter" library to mount the images but i had hard time and eventually i had to drop that idea. I later used os library for mounting and unmounting of the images.

I followed https://dev.iachieved.it/iachievedit/exploring-img-files-on-linux/ for mountiung of .img images. 
