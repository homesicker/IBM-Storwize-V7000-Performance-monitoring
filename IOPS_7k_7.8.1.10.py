import time

from pyzabbix.api import ZabbixAPI
from pyzabbix import ZabbixMetric, ZabbixSender

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

zapi = ZabbixAPI(url='https://REPLACE WITH U ZBX IP\DNS DUDE', user='REPLACE WITH U ZBX API USER DUDE', password='REPLACE WITH U ZBX API USER PASS DUDE')

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Remote(
   command_executor='http://REPLACE WITH U IP DUDE:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME,
   options=options)

driver.get("https://REPLACE WITH U IP DUDE/login")

username = driver.find_element_by_id('user')
username.clear()
username.send_keys('REPLACE WITH U USER DUDE')

password = driver.find_element_by_id('password')
password.clear()
password.send_keys('REPLACE WITH U PASS DUDE')

time.sleep(1)
driver.find_element_by_id('submitBtn').click()
time.sleep(2)
driver.get("https://REPLACE WITH U IP DUDE/gui#monitor-perf")
time.sleep(6)
selector = driver.find_element_by_xpath(".//div[@id='dijit_Toolbar_0']//table[@id='dijit_form_Select_0']")
selector.click()
time.sleep(0.5)
selector2 = driver.find_element_by_xpath(".//table[@id='dijit_form_Select_0_menu']//tbody[@class='dijitReset']//tr[2]")
time.sleep(1)
selector2.click()
#s = driver.find_element_by_xpath(".//div[@class='arcGaugeContainer']//div[@id='aspen_pods_ArcGauge_0']//div[@class='evoGaugeLabel']//span").text
#print(s)
while True:
    try:
        space = driver.find_element_by_xpath(".//div[@class='podContainer']//div[@class='pod']//div[@id='evo_pods_StatusBarMultiLabel_0']//div[@class='barText']").text
        space_pre = space.replace('Allocated: ', '').replace('TiB', '').replace('(', '/').replace(')', '').replace(' ', '').replace('%', '')
        space_fin = space_pre.split('/')

        read_iops = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        write_iops = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[2]//span//span[@class='perfValue']").text

        md_read_iops = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        md_write_iops = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[2]//span//span[@class='perfValue']").text

        fc_iops = driver.find_element_by_xpath(".//div[@class='columns2 left']//div[@id='aspen_home_viewport_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf multiSeries']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        sas_iops = driver.find_element_by_xpath(".//div[@class='columns2 left']//div[@id='aspen_home_viewport_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf multiSeries']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[3]//span//span[@class='perfValue']").text

        packet = [
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.r.iops', read_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.w.iops', write_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.read.iops', md_read_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.write.iops', md_write_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.w.iops', md_write_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.int.fc.iops', fc_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.int.sas.iops', sas_iops.replace(',', '')),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.space.used', space_fin[0]),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.space.total', space_fin[1]),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.space.used.perc', space_fin[2]),
        ]
        result = ZabbixSender(use_config=True).send(packet)
        print(result)
    except Exception as e:
        print(e)
    time.sleep(4)
