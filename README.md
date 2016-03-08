## API of the ilmnuri.com
* This is the source code of api ilmnuri.com for its android mobile app.
* Android app url: [ilm nuri](https://play.google.com/store/apps/details?id=com.ilmnuri.com)
* Website: www.ilmnuri.com
* Temporary api url: [api.azimov.xyz](http://api.azimov.xyz/api/v1.0/albums)
* Android app name: "ilm nuri" in playstore

### System Requirements
We are running Nginx + Flask for the API on EC2 instance. 
We will need to install some system packages first and start them.

```bash
# RHEL based system VM, if you do not have repo do below.
## RHEL/CentOS 6 64-Bit ##
# wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
# rpm -ivh epel-release-6-8.noarch.rpm
## RHEL/CentOS 7 64-Bit ##
# wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
# rpm -ivh epel-release-7-5.noarch.rpm
sudo yum install -y nginx memcached python-devel python-pip gcc 
sudo pip install flask uwsgi python-memcached 
sudo systemctl enable memcached && sudo systemctl start memcached
sudo systemctl enable nginx && sudo systemctl start nginx
# enable and start for other services needed. Once you create system file in /etc/systemd/system/<somename>.service
# sudo systemctl enable somename && sudo systemctl start somename
```
### Installation

Here is the guide: [link](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-centos-7)

Systemd file is located in the repo's system directory. 
All other files are as well included. 

### Troubleshooting
* make sure memcached, nginx, serviceFile up and running
* after code change or anything make sure restarting the serviceFile and reload nginx
* check nginx logs or try running the flask app in debug mode. 
