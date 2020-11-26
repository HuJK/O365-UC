# Office 365 Account Registration Portal
This panel can let you distribute Office 365 account via invite code or email

## requirement
```bash
sudo apt-get install tmux python3 python3-pip
sudo pip3 install tornado js2py
```

## Installation
```bash
git clone --depth 1 https://github.com/HuJK/O365-UC.git
cd O365-UC/backend/

# Running in the foreground
python3 o365-creater_api.py

# Running in the backgroung
# I am used to use tmux. You can use screen dtach & etc.
tmux new -d -s o365 python3 o365-creater_api.py
```

## Usage
Then connect to [https://127.0.0.1:12536](https://127.0.0.1:12536) 

If you want use different port, please edit the ```listen_port``` section in ```backend\config\config_pwd.json``` 

## Demo
Demo Site :

Guest page:
[https://ruvm.whojk.com:2053/](https://ruvm.whojk.com:2053/)

Admin page:
[https://ruvm.whojk.com:2053/admin](https://ruvm.whojk.com:2053/admin)

Demo site are just for demo, it will **not** create real users.

| | |
|-|-|
|invite code | anonymous|
|Admin password | adminn|

#### Enable Demo mode:
You can enable or disable demo mode only by directly edit config file.

Please edit 
```
backend\config\config_o365.json
backend\config\config_pwd.json
```
, and than set ```demo_mode``` to ```true```.


#### Create accounts by invite code:
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/14.PNG) ![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/14-2.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/12.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/13.PNG)

#### Configure invite code:

In the ```invite_code``` folder, there is a ```datas.db``` file. use any sqlite3 editor to edit the file.

In the ```invite_code``` table, each row is a invite_code, and the ```remains``` colume is the number of remains of the invite_code

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/15.PNG)

If you want to use mysql instead of sqlite3, or your own invite code check progress, please edit line 330 to line 367 at the ```backend/o365_creater_auth.py``` file:

Please return True or False

```python
    def check(self,password):
        conn = sqlite3.connect(self.invite_code_db_path)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM invite_code WHERE invite_code=?',[password]).fetchall()
        ret = False
        if len(result) > 0 and result[0]["remains"] > 0:
            cursor.execute('UPDATE invite_code SET remains = remains - 1 WHERE invite_code=?',[password])
            ret = True
        conn.commit()
        conn.close()
        return ret
```

The following function is check user redeemed or not. If user logout before they redeem, it will add ```use_left``` back. 

And it will be called when the user logout or other users login for all expired user.

```sid``` is the sesstion id. When user check pass, the system will generate one.

```self.loginUser``` is a dictionary, stored all login users. remember to ```del self.loginUser[sid]``` in the function.

```self.loginUser[sid]["invite_code"]``` is the invite_code that the user use.

```self.loginUser[sid]["redeemed"]``` is whether the user created an account or not. 

```python
    def logout(self,sid):
        conn = sqlite3.connect(self.invite_code_db_path)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        if "redeemed" in self.loginUser[sid] and self.loginUser[sid]["redeemed"] == False:
            invite_code = self.loginUser[sid]["invite_code"]
            cursor.execute('UPDATE invite_code SET remains = remains + 1 WHERE invite_code=?',[invite_code])
        else:
            user_info = defaultdict(lambda:None, self.loginUser[sid])
            del_record = cursor.execute('SELECT * FROM register_info WHERE userPrincipalName=?',[user_info["userPrincipalName"]]).fetchall()
            if len(del_record) > 0:
                cursor.execute('UPDATE register_info SET userPrincipalName=? WHERE id=?',[None,del_record[0]["id"]])
            reg_record = cursor.execute('SELECT * FROM register_info WHERE invite_code=? AND userPrincipalName IS NULL',[user_info["invite_code"]]).fetchall()
            if len(reg_record) > 0:
                cursor.execute('UPDATE register_info SET invite_code=? , userPrincipalName=? , displayName=? , infomation=? WHERE id=?',
    [user_info["invite_code"],user_info["userPrincipalName"],user_info["displayName"],json.dumps(user_info["infomation"],ensure_ascii=False,default=lambda x:str(x)),reg_record[0]["id"]])
            else:
                cursor.execute('INSERT INTO register_info (invite_code,userPrincipalName,displayName,infomation) VALUES (?,?,?,?)',[user_info["invite_code"],user_info["userPrincipalName"],user_info["displayName"],json.dumps(user_info["infomation"],indent=2, ensure_ascii=False,default=lambda x:str(x))])
        del self.loginUser[sid]
        remain_0_invite_codes = cursor.execute('SELECT * FROM invite_code WHERE remains=0').fetchall()
        login_user_used_codes = set([user["invite_code"] for user in self.loginUser.values()])
        no_user_used_codes = [code["invite_code"] for code in remain_0_invite_codes if code["invite_code"] not in login_user_used_codes]
        for invite_code in no_user_used_codes:
            cursor.execute('DELETE FROM invite_code WHERE invite_code=?',[invite_code]).fetchall()
        conn.commit()
        conn.close()
```


## Initial Setup:
 
##### Default password: ```admin```

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/01.PNG)
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/Setup.PNG)

Now, you can configure registration settings or CAPTCHA settings

#### Registration settings

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/09.PNG)

#### CAPTCHA:

It should be able to work at most of CAPTCHA services. 

Like google reCAPTCHA/hCAPTCHA/luosimao/腾讯云验证码. 

I only tested google reCAPTCHA v2 and hCAPTCHA.

###### google reCAPTCHA v2:

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/16.PNG)

###### hCAPTCHA:
![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/17.PNG)

#### Admin password

![alt text](https://raw.githubusercontent.com/HuJK/O365-UC/master/Screenshots/10.PNG)

## License

- The Html,CSS,JavaScript,and python files are licensed under the GNU General Public License v3:
  - http://www.gnu.org/licenses/gpl-3.0.html

## Author

**HuJK**, Released under the [GPL-3.0](./LICENSE) License.<br>

> GitHub [@HuJK](https://github.com/HuJK)
