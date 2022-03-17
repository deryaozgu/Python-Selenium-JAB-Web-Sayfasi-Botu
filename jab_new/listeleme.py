import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from Ekleme import EEkleme

class Listeleme:

    def __init__(self):
        self.urun_ve_alturun_list=[]
        self.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())  
        self.ana_url_list=[]
        self.UrunDetayList=[]
    def SayfalariGez(self):
        self.browser.get("https://www.jab.de/tr/en/productadvancedsearch?searchTerm=&page=1")
        i = 0
        for i in range(2):
            rest = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/main/div[2]/section[3]/div/div/div[1]/form/div/div[2]/section[4]/span")))
            self.browser.execute_script("arguments[0].click();", rest)
        for j in range(2):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        time.sleep(5)

    def AnaUrunLinkleriniKaydet(self):
        u = self.browser.find_element_by_class_name("teaser-produkte")
        urunler = u.find_elements_by_class_name("product-teaser")
        for i in urunler:
            self.ana_url_list.append(i.find_element_by_class_name("teaser-wrap").find_element_by_tag_name("a").get_attribute("href"))
            print("AnaUrunLinkleriniKaydet=",i.find_element_by_class_name("teaser-wrap").find_element_by_tag_name("a").get_attribute("href"))
            #breaki sil
            break
    def AltUrunLinkleriniKaydet(self):
        for i in self.ana_url_list:
            self.UrunveAltUrunleriniListeyeEkle(i)
    
    def UrunveAltUrunleriniListeyeEkle(self,ana_urun):
        itemler=[]
        self.browser.get(ana_urun)
        self.urun_ve_alturun_list.append(ana_urun)
        tab_zero=self.browser.find_element_by_id("tab-0")
        tab_one = self.browser.find_element_by_id("tab-1")
        tab_two = self.browser.find_element_by_id("tab-2")
        itemler.append(tab_zero)
        itemler.append(tab_one)
        itemler.append(tab_two)
        if "Bitte entschuldigen Sie" in self.browser.page_source:
          print("alt ürün yok")
        else:
          for item in itemler:
              i=item.find_elements_by_class_name("item")
              for x in i:
                  self.urun_ve_alturun_list.append(x.find_element_by_tag_name("a").get_attribute("href"))
                  print("UrunveAltUrunleriniListeyeEkle:",x.find_element_by_tag_name("a").get_attribute("href"))
    def UrunveAltUrunleriKaydet(self):
        for alt_urun in self.urun_ve_alturun_list:
            artikel,marke,nummer,farb,qualitat,material,hinweise,eigen,breite,rapport,martindale,design,images,transparenz=self.UrunDetails( alt_urun)
            self.UrunDetayList.append(EEkleme(artikel,marke,nummer,farb,qualitat,material,hinweise,eigen,breite,rapport,martindale,design,images,transparenz))
    def UrunDetails(self,urun):
        artikel=""
        transparenz=""
        rapport=""
        eigen=""
        marke=""
        nummer=""
        farb=""
        martindale=""
        qualitat=""
        material=""
        hinweise=""
        breite=""
        design=""
        images=[]
        self.browser.get(urun)
        images.clear()
        time.sleep(2)
        tr_list=self.browser.find_element_by_xpath("//*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody")
        tr_list_sayisi=tr_list.find_elements_by_tag_name("tr")
        tr_sayisi =0
        for i in tr_list_sayisi:
            tr_sayisi+=1
        for tr in range(1,tr_sayisi+1):
            texti = self.browser.find_element_by_xpath("//*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr["+str(tr)+"]/td[1]").text
            if texti=="Artikel:":
                artikel = self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti=="Marke:":
                marke = self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Nummer:":
                nummer=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Farbvarianten:":
                farb=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Qualität:":
                qualitat=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Material:":
                material=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Hinweise:":
                hinweise=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Eigenschaften:":
                eigen=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Breite/Höhe:":
                breite=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Rapportlänge:":
                rapport = self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Martindale:":
                martindale = self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Design:":
                design=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
            elif texti == "Transparenz:":
                transparenz=self.browser.find_element_by_xpath(" //*[@id='top']/main/div[2]/section[5]/div[1]/article/section/table/tbody/tr[" + str(tr) + "]/td[2]").text
        gorsel = self.browser.find_element_by_class_name("lSGallery")
        gorseller = gorsel.find_elements_by_tag_name("li")
        for i in gorseller:
            text = i.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
            new_text = text[0:22] + "hd" + text[29:]
            images.append(new_text)
            print(new_text)
        return artikel,marke,nummer,farb,qualitat,material,hinweise,eigen,breite,rapport,martindale,design,images,transparenz

    def TumUrunBilgileriniYaz(self):
        for urun in self.UrunDetayList:
            print(urun.printDetay())










