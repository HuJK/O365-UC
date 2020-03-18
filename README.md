# O365-UC
Office 365 Account Registration Portal

## Usage


#### Install

```bash
sudo apt install tmux python3 python3-pip
sudo pip3 install tornado


git clone https://github.com/HuJK/O365-UC.git
cd O365-UC/backend/
# Running in the backgroung
tmux new -d -s o365 python3 o365-creater_api.py
# Running in the foreground
python3 o365-creater_api.py
```

Then connect to [https://127.0.0.1:12536](https://127.0.0.1:12536) 

#### Create accounts by invite code:

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/14.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/12.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/13.PNG)

#### Edit invite code:

In the ```invite_code``` folder, each filename is a code and the content is the usage count.

Make sure these files only contain numbers. No any newline , or any characters other than [0-9]

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/15.PNG)

Or you can write your own invite code check algorithm. Just edit line 86 to line 103 at the ```backend/o365_creater_auth.py``` file:

If you change this:
```python
    def check(self,password):
        i_path = os.path.join(self.invite_code_path,password)
        if os.path.isfile(i_path):
            with open(i_path) as i_fileHendler:
                use_left = int(i_fileHendler.read())
            if use_left < 0:
                return True
            elif use_left == 0:
                os.remove(i_path)
                return False
            elif use_left == 1:
                os.remove(i_path)
                return True
            else:
                with open(i_path,"w") as i_fileHendler:
                    i_fileHendler.write(str(use_left - 1))
                return True
        return False
  ```
  
 to this:
 ```python
    def check(self,password):
        import math
        return 0== sum([ True if int(password)%factor == 0 else False for factor in ( [2] + list(range(3,int(math.sqrt(int(password))),2) )) ]) and int(password) > 1000000000
  ```
  , any prime number which > 1000000000 wil be considered to a valid invite code.
  
 ## Setup:
 
Default password: ```admin```
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/01.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/02.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/03.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/04.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/05.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/06.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/07.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/08.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/09.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/10.PNG)
