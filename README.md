# IBM-Storwize-V7000-Performance-monitoring

Download jre-8u261, just google it

Download Selenium https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar

Setup new\or not windows\linux with gui server, install Google Chrome v84 and download https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_win32.zip

Download NSSM https://nssm.cc/release/nssm-2.24.zip

Place chrome driver and nssm in somewhere dir, like C:\distr

Run cmd command for install selenim server service: C:\distr\nssm\win64\nssm.exe install selenium-server java -Dwebdriver.chrome.driver="C:\distr\chromedriver.exe"  -jar "C:\distr\selenium-server-standalone-3.141.59.jar"

Now start it: C:\distr\nssm\win64\nssm.exe start selenium-server

Lets go next

Install python3 on you zabbix server

Place IOPS_*.py, MBS_*.py and run_as_service.sh somewhere like /opt/ibm

Create service vi /etc/systemd/system/ibm-mb-svc.service, and copy paste text in ibm-svc-mb.service

Import zabbix template zbx_ibm_sw7k.xml

Open *.py file and edit some fields, replace with you IP, user\password

Time to run MUHAHA

systemctl enable ibm-mb-svc

systemctl start ibm-mb-svc

Open u zabbix and go out

thx for me.
just dude.




