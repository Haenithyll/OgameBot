import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# region Variables


driver = webdriver.Chrome()
action = webdriver.ActionChains(driver)
# Resources
Metal = 0
Crystal = 0
Deuterium = 0
Energy = 0
# Production
MetalProd = 0
CrystalProd = 0
DeuteriumProd = 0
# [time, metal, crystal, energy]
MetalMine = [0, 0, 0, 0]
CrystalMine = [0, 0, 0, 0]
DeuteriumMine = [0, 0, 0, 0]
Mines = [MetalMine, CrystalMine, DeuteriumMine]
MineIndexForUpgrade = 0
# [time, metal, crystal]
SolarPlant = [0, 0, 0]

# Buildings Paths
MetalMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[1]/span/button"
CrystalMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[2]/span/button"
DeuteriumMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[3]/span/button"
MinesUpgradePath= [MetalMineUpgradeXPATH, CrystalMineUpgradeXPATH, DeuteriumMineUpgradeXPATH]
SolarPlantUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[4]/span/button"


# endregion
# region Initialization


def init():
    driver.maximize_window()
    driver.get('https://lobby.ogame.gameforge.com/fr_FR/hub')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#loginRegisterTabs > ul > li:nth-child(1)').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#loginForm > div:nth-child(1) > div > input[type=email]').send_keys('paul_snauwaert@yahoo.fr')
    driver.find_element(By.CSS_SELECTOR, '#loginForm > div:nth-child(2) > div > input[type=password]').send_keys('MotDePasseDeTest123')
    driver.find_element(By.CSS_SELECTOR, '#loginForm > p > button.button.button-primary.button-lg').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(5) > div > div > span.cookiebanner4 > button:nth-child(2)').click()
    driver.find_element(By.CSS_SELECTOR, '#joinGame > button').click()


def switchTab():
    time.sleep(1.5)
    child = driver.window_handles[1]
    driver.close()
    driver.switch_to.window(child)


# endregion
# region Available Resources Retrieval


def retrieveResources():
    global Metal
    global Crystal
    global Deuterium
    global Energy
    Metal = int(driver.find_element(By.CSS_SELECTOR, '#resources_metal').text.replace('.', ''))
    Crystal = int(driver.find_element(By.CSS_SELECTOR, '#resources_crystal').text.replace('.', ''))
    Deuterium = int(driver.find_element(By.CSS_SELECTOR, '#resources_deuterium').text.replace('.', ''))
    Energy = int(driver.find_element(By.CSS_SELECTOR, '#resources_energy').text)


def goToResourcesTab():
    driver.find_element(By.CSS_SELECTOR, '#menuTable > li:nth-child(2) > a').click()
    time.sleep(1)


# endregion
# region Resources Production Retrieval


def goToProductionTab():
    driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[2]/div/ul/li[2]/span/a/div').click()
    time.sleep(1)


def retrieveProduction():
    global MetalProd
    global CrystalProd
    global DeuteriumProd
    MetalProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[20]/td[2]/span').text.replace('.', ''))
    CrystalProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[20]/td[3]/span').text.replace('.', ''))
    DeuteriumProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[20]/td[4]/span').text.replace('.', ''))


# endregion
# region Time Conversion


def convertTime(string):
    totalTime = 0
    index = 0
    if 'h' in string:
        totalTime += int(retrieveTimeValue(string, 0, 'h')[0]) * 3600
        index = retrieveTimeValue(string, 0, 'h')[1]
    if 'm' in string:
        totalTime += int(retrieveTimeValue(string, index, 'm')[0]) * 60
        index = retrieveTimeValue(string, index, 'm')[1]
    if 's' in string:
        totalTime += int(retrieveTimeValue(string, index, 's')[0])
    return totalTime


def retrieveTimeValue(string, index, char):
    buffer = ""
    c = string[index]
    while c != char:
        buffer += c
        index += 1
        c = string[index]
    index += 2
    return buffer, index


# endregion
# region Upgrades Cost Retrieval


def retrieveMinesCosts():
    global Mines
    for i in range(3):
        driver.find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[{i + 1}]/span").click()
        time.sleep(1)
        Mines[i][0] = convertTime(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li[1]/time").text)
        Mines[i][1] = int(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[1]").text.replace('.', ''))
        Mines[i][2] = int(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[2]").text.replace('.', ''))
        Mines[i][3] = int(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li[2]/span").text.replace('.', ''))


def retrieveSolarPlantCost():
    global SolarPlant
    driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[4]/span").click()
    time.sleep(1)
    SolarPlant[0] = convertTime(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li[1]/time").text)
    SolarPlant[1] = int(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[1]").text.replace('.', ''))
    SolarPlant[2] = int(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[2]").text.replace('.', ''))


# endregion
# region Debug Values


def printValues():
    print("Métal : " + str(Metal) + " | Cristal : " + str(Crystal) + " | Deutérium : " + str(Deuterium) + " | Énergie : " + str(Energy))
    print("\nCout pour augmenter la mine de métal : " + str(MetalMine[0]) + " Métal | " + str(MetalMine[1]) + " Cristal | " + str(MetalMine[2]) + " Énergie")
    print("Cout pour augmenter la mine de cristal : " + str(CrystalMine[0]) + " Métal | " + str(CrystalMine[1]) + " Cristal | " + str(CrystalMine[2]) + " Énergie")
    print("Cout pour augmenter la mine de deutérium : " + str(DeuteriumMine[0]) + " Métal | " + str(DeuteriumMine[1]) + " Cristal | " + str(DeuteriumMine[2]) + " Énergie")
    print("Cout pour augmenter la centrale électrique solaire: " + str(SolarPlant[0]) + " Métal | " + str(SolarPlant[1]) + " Cristal")
    print("\nProductions - Métal : " + str(MetalProd) + " | Cristal : " + str(CrystalProd) + " | Deutérium : " + str(DeuteriumProd))


# endregion
# region Upgrade Process


def tryUpgrade():
    computeCheapestUpgrade()
    if Energy > Mines[MineIndexForUpgrade][3]:
        if Metal > Mines[MineIndexForUpgrade][1] and Crystal > Mines[MineIndexForUpgrade][2]:
            driver.find_element(By.XPATH, MinesUpgradePath[MineIndexForUpgrade]).click()
            time.sleep(Mines[MineIndexForUpgrade][0] + 5)
            Update()
        else:
            goToProductionTab()
            retrieveProduction()
            WaitForUpgrade(Mines[MineIndexForUpgrade][1], Mines[MineIndexForUpgrade][2])
            goToResourcesTab()
    else:
        if Metal > SolarPlant[1] and Crystal > SolarPlant[2]:
            driver.find_element(By.XPATH, SolarPlantUpgradeXPATH).click()
            time.sleep(SolarPlant[0] + 5)
            Update()
        else:
            goToProductionTab()
            retrieveProduction()
            WaitForUpgrade(SolarPlant[1], SolarPlant[2])
            goToResourcesTab()


def WaitForUpgrade(metalNeeded, crystalNeeded):
    timeToGetMetal = 0
    timeToGetCrystal = 0
    if not Metal > metalNeeded:
        timeToGetMetal = (metalNeeded - Metal)/MetalProd*3600
    if not Crystal > crystalNeeded:
        timeToGetCrystal = (crystalNeeded - Crystal)/CrystalProd*3600
    time.sleep(max(timeToGetMetal, timeToGetCrystal))
    tryUpgrade()


def computeCheapestUpgrade():
    global MineIndexForUpgrade
    cheapest = 0
    index = 0
    for i in range(3):
        cost = Mines[i][1] + Mines[i][2]
        if cost < cheapest or cheapest == 0:
            cheapest = cost
            index = i
    MineIndexForUpgrade = index


# endregion
# region Update Method


def Update():
    goToResourcesTab()
    retrieveResources()
    retrieveMinesCosts()
    retrieveSolarPlantCost()
    tryUpgrade()


# endregion
init()
switchTab()
Update()
# printValues()
# Upgrade()
