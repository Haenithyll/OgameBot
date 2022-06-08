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
# Capacity
MaxMetal = 0
MaxCrystal = 0
MaxDeuterium = 0
StoragesCapacity = [MaxMetal, MaxCrystal, MaxDeuterium]
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
MetalStorage = [0, 0, 0]
CrystalStorage = [0, 0, 0]
DeuteriumStorage = [0, 0, 0]
StoragesCost = [MetalStorage, CrystalStorage, DeuteriumStorage]

# Buildings Paths
MetalMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[1]/span/button"
CrystalMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[2]/span/button"
DeuteriumMineUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[3]/span/button"
MinesUpgradePath = [MetalMineUpgradeXPATH, CrystalMineUpgradeXPATH, DeuteriumMineUpgradeXPATH]
SolarPlantUpgradeXPATH = "/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[4]/span/button"


# Requirements [[Buildings], [Techs]]

# Technologies
# Fundamentals
EnergyTech = [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
LaserTech = [[0, 0, 1], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
IonTech = [[0, 0, 4], [4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
HyperspaceTech = [[0, 0, 7], [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0]]
PlasmaTech = [[0, 0, 4], [8, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# Propulsion
CombustionTech = [[0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
ImpulsionTech = [[0, 0, 2], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
HyperspacePropulsionTech = [[0, 0, 7], [5, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0]]
# Advanced
SpyTech = [[0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
ComputerTech = [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
AstrophysicsTech = [[0, 0, 3], [0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 0, 0]]
IRNTech = [[0, 0, 10], [5, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 5, 0]]
GravitonTech = [[0, 0, 12], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# Combat
WeaponTech = [[0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
ShieldTech = [[0, 0, 6], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
ArmorTech = [[0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Ships
# Combat
LightFighter = [[2, 1, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
HeavyFighter = [[2, 3, 2], [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
Cruiser = [[2, 5, 2], [4, 5, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
BattleShip = [[2, 7, 7], [5, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 5, 0]]
Hunter = [[2, 8, 7], [5, 12, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0]]
Bomber = [[2, 8, 4], [8, 10, 5, 0, 5, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
Destroyer = [[2, 9, 7], [5, 0, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 5, 0]]
DeathStar = [[2, 12, 12], [5, 0, 0, 6, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 5, 0]]
# Civil
LightCarrier = [[2, 2, 1], [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
HeavyCarrier = [[2, 4, 1], [1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
ColonisationShip = [[2, 4, 2], [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
Recycler = [[2, 4, 6], [3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]
SpyingProbe = [[2, 3, 3], [1, 0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]]
Satellite = [[2, 2, 0], [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Defenses
MissileLauncher = [[2, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
LightLaserArtillery = [[2, 2, 1], [2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
HeavyLaserArtillery = [[2, 4, 1], [3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
GaussCanon = [[2, 6, 6], [6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0]]
IonArtillery = [[2, 4, 4], [4, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0]]
PlasmaLauncher = [[2, 8, 4], [8, 10, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0]]
SmallShield = [[2, 1, 6], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]
BigShield = [[2, 6, 6], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0]]

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
    driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(5) > div > div > span.cookiebanner4 > button:nth-child(2)').click()
    driver.find_element(By.CSS_SELECTOR, '#joinGame > button').click()


def switchTab():
    time.sleep(1.5)
    child = driver.window_handles[1]
    driver.close()
    driver.switch_to.window(child)


# endregion
# region Available Resources Retrieval


def goToResourcesTab():
    driver.find_element(By.CSS_SELECTOR, '#menuTable > li:nth-child(2) > a').click()
    time.sleep(1)


def retrieveResources():
    global Metal
    global Crystal
    global Deuterium
    global Energy
    goToResourcesTab()
    Metal = int(driver.find_element(By.CSS_SELECTOR, '#resources_metal').text.replace('.', ''))
    Crystal = int(driver.find_element(By.CSS_SELECTOR, '#resources_crystal').text.replace('.', ''))
    Deuterium = int(driver.find_element(By.CSS_SELECTOR, '#resources_deuterium').text.replace('.', ''))
    Energy = int(driver.find_element(By.CSS_SELECTOR, '#resources_energy').text)


# endregion
# region Resources Production Retrieval


def goToProductionTab():
    driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[2]/div/ul/li[2]/span/a/div').click()
    time.sleep(1)


def retrieveProduction():
    goToProductionTab()
    global MetalProd
    global CrystalProd
    global DeuteriumProd
    MetalProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[2]/span').text.replace('.', ''))
    CrystalProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[3]/span').text.replace('.', ''))
    DeuteriumProd = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[4]/span').text.replace('.', ''))


def retrieveCapacity():
    goToProductionTab()
    global StoragesCapacity
    for i in range(3):
        StoragesCapacity[i] = int(driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[18]/td[{i + 2}]/span").text.replace('.', ''))


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


def retrieveStorageCost():
    global StoragesCost
    for i in range(3):
        driver.find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[2]/div/div[2]/ul/li[{i + 8}]/span").click()
        time.sleep(1)
        StoragesCost[i][0] = convertTime(driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li/time").text)
        children = driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li")
        for j in range(len(children)):
            if retrieveResourceType(children[j].get_attribute("aria-label")) == "Métal" :
                StoragesCost[i][1] = int(children[j].text.replace('.', ''))
            if retrieveResourceType(children[j].get_attribute("aria-label")) == "Cristal" :
                StoragesCost[i][2] = int(children[j].text.replace('.', ''))


def retrieveResourceType(string):
    newString = string.replace('.', '')
    newString = newString.replace(' ', '')
    for i in range(10):
        newString = newString.replace(f"{ i }", '')
    return newString

# endregion
# region Debug Values


def printValues():
    print("Métal : " + str(Metal) + " | Cristal : " + str(Crystal) + " | Deutérium : " + str(Deuterium) + " | Énergie : " + str(Energy))
    print("\nCout pour augmenter la mine de métal : " + str(MetalMine[0]) + " Métal | " + str(MetalMine[1]) + " Cristal | " + str(MetalMine[2]) + " Énergie")
    print("Cout pour augmenter la mine de cristal : " + str(CrystalMine[0]) + " Métal | " + str(CrystalMine[1]) + " Cristal | " + str(CrystalMine[2]) + " Énergie")
    print("Cout pour augmenter la mine de deutérium : " + str(DeuteriumMine[0]) + " Métal | " + str(DeuteriumMine[1]) + " Cristal | " + str(DeuteriumMine[2]) + " Énergie")
    print("Cout pour augmenter la centrale électrique solaire: " + str(SolarPlant[1]) + " Métal | " + str(SolarPlant[2]) + " Cristal")
    print("\nProductions - Métal : " + str(MetalProd) + " | Cristal : " + str(CrystalProd) + " | Deutérium : " + str(DeuteriumProd))


# endregion
# region Upgrade Process


# def QueueUpgrade(XPATH):

def tryUpgrade():
    print("TryUpgrade")
    goToResourcesTab()
    computeCheapestUpgrade()
    if Energy > Mines[MineIndexForUpgrade][3]:
        if Metal > Mines[MineIndexForUpgrade][1] and Crystal > Mines[MineIndexForUpgrade][2]:
            driver.find_element(By.XPATH, MinesUpgradePath[MineIndexForUpgrade]).click()
            time.sleep(Mines[MineIndexForUpgrade][0] + 5)
            Update()
        else:
            retrieveProduction()
            WaitForUpgrade(Mines[MineIndexForUpgrade][1], Mines[MineIndexForUpgrade][2])
    else:
        if Metal > SolarPlant[1] and Crystal > SolarPlant[2]:
            driver.find_element(By.XPATH, SolarPlantUpgradeXPATH).click()
            time.sleep(SolarPlant[0] + 5)
            Update()
        else:
            retrieveProduction()
            WaitForUpgrade(SolarPlant[1], SolarPlant[2])


def WaitForUpgrade(metalNeeded, crystalNeeded):
    print("WaitForUpgrade")
    timeToGetMetal = 0
    timeToGetCrystal = 0
    if not Metal > metalNeeded:
        timeToGetMetal = (metalNeeded - Metal)/MetalProd*3600
    if not Crystal > crystalNeeded:
        timeToGetCrystal = (crystalNeeded - Crystal)/CrystalProd*3600
    timetoWait = max(timeToGetMetal, timeToGetCrystal)
    print(timetoWait)
    time.sleep(timetoWait)
    goToResourcesTab()
    Update()


def computeCheapestUpgrade():
    print("ComputeCheapestUpgrade")
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
# region Storage Management


# def CheckStorage():
# if Metal == MetalStorage


# endregion
# region Update Method


def Update():
    retrieveResources()
    retrieveMinesCosts()
    retrieveSolarPlantCost()
    retrieveStorageCost()
    retrieveCapacity()
    # CheckStorage()
    tryUpgrade()


# endregion
init()
switchTab()
Update()
# goToProductionTab()
# retrieveProduction()
# printValues()
# Upgrade()
