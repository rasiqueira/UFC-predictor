# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:36:50 2020

@author: Rodrigo
"""

from selenium import webdriver
from time import sleep
import sqlite3


driver = webdriver.Chrome('chromedriver.exe')

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for letter in letters:
    driver.get('http://ufcstats.com/statistics/fighters?char='+letter+'&page=all')
    sleep(2)
    linhas = driver.find_elements_by_class_name('b-statistics__table-row')
    tamanho = len(linhas)
    for i in range (2,tamanho):
        fname = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[1]/a').text)
        lname = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[2]/a').text)
        ht = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[4]').text)
        wt = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[5]').text)
        reach = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[6]').text)
        wins = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[8]').text)
        loses = (driver.find_element_by_xpath('/html/body/section/div/div/div/table/tbody/tr['+str(i)+']/td[9]').text)
        try:
            h = int(ht.split("'")[0])*30.48
            p = int(ht.split("'")[1].split('"')[0])*2.54
            ht = h + p
        except:
            ht = ''
        try:
            reach = int(reach.split(".")[0])*2.54
        except:
            reach = ''
        try:
            wt = int(wt.split(" ")[0])
        except:
            wt = ''
        try:
            if wt <= 115:
                category = 'Peso Palha'
            elif wt <= 125:
                category = 'Peso Mosca'
            elif wt <= 135:
                category= 'Peso Galo'
            elif wt <= 145:
                category = 'Peso Pena'
            elif wt <= 155:
                category = 'Peso Leve'
            elif wt <= 170:
                category = 'Peso Meio-Médio'
            elif wt <= 185:
                category = 'Peso Médio'
            elif wt <= 205:
                category = 'Peso Meio-Pesado'
            else:
                category = 'Peso Pesado'
        except:
            category = ''
        name = fname+' '+lname
        print(fname, lname, ht, wt, reach, wins, loses, category)
        try:
            conn = sqlite3.connect('ufc.db')
            cursor = conn.cursor()
            cursor.execute("""
                                   INSERT INTO fighters (name, ht, wt, reach, w, l, category)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)
                               """, (name, ht, wt, reach, wins, loses, category))
            conn.commit()
            conn.close()
        except:
            pass
driver.close()
    
    