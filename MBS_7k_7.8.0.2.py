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

while True:
    try:
        io = driver.find_element_by_xpath(".//div[@class='arcGaugeContainer']//div[@id='aspen_pods_ArcGauge_0']//div[@class='evoGaugeLabel']//span").text
        read_s = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        write_s = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[2]//span//span[@class='perfValue']").text
        read_l = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[3]//span//span[@class='perfValue']").text
        write_l = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[4]//span//span[@class='perfValue']").text

        md_read_s = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        md_write_s = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[2]//span//span[@class='perfValue']").text
        md_read_l = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[3]//span//span[@class='perfValue']").text
        md_write_l = driver.find_element_by_xpath(".//div[@class='columns2 right']//div[@id='evo_perf_MultiSeriesPerf_1']//div[@class='perfModule']//div[@class='legendPerf']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[4]//span//span[@class='perfValue']").text

        fc = driver.find_element_by_xpath(".//div[@class='columns2 left']//div[@id='aspen_home_viewport_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf multiSeries']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td//span//span[@class='perfValue']").text
        sas = driver.find_element_by_xpath(".//div[@class='columns2 left']//div[@id='aspen_home_viewport_MultiSeriesPerf_0']//div[@class='perfModule']//div[@class='legendPerf multiSeries']//table[@role='presentation']//tr[@data-dojo-attach-point='legendTR']//td[3]//span//span[@class='perfValue']").text

        packet = [
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.iops.total', io),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.int.fcfix', fc),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.read', md_read_s),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.read.latency', md_read_l),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.write', md_write_s),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.mdisk.write.latency', md_write_l),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.int.sasfix', sas),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.r.latency', read_l),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.r.speed', read_s),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.w.speed', write_s),
            ZabbixMetric('REPLACE WITH U ZBX HOST DUDE', 'ibm.volumes.w.latency', write_l)
        ]
        result = ZabbixSender(use_config=True).send(packet)
        print(result)
    except Exception as e:
        print(e)
    time.sleep(4)
