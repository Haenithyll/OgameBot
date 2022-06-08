using System;
using System.Threading;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

namespace Ogame_Bot
{
    public enum Tab
    {
        Overview,
        Resources,
        Facilities,
        Production,
        Research,
        Shipyard,
        Defense,
        Fleet,
        Galaxy
    }

    public enum UpgradeType
    {
        Mine,
        Storage,
        EnergyPlant,
        Facility,
        Research
    }

    class Program
    {
        public static string emailAdress = "paul_snauwaert@yahoo.fr";
        public static string passWord = "MotDePasseDeTest123";

        public static WebDriver driver;
        public static Tab currentTab;

        public static int Metal;
        public static int Crystal;
        public static int Deuterium;
        public static int Energy;

        public static int MetalProduction;
        public static int CrystalProduction;
        public static int DeuteriumProduction;

        public static int MetalCapacity;
        public static int CrystalCapacity;
        public static int DeuteriumCapacity;

        public static List<Upgrade> Mines = new List<Upgrade>();
        public static List<Upgrade> Storage = new List<Upgrade>();
        public static List<Upgrade> EnergyPlant = new List<Upgrade>();
        public static List<Upgrade> Facilities = new List<Upgrade>();
        public static List<Upgrade> Research = new List<Upgrade>();

        public static List<List<Upgrade>> PrimaryUpgrades = new List<List<Upgrade>>()
        {
            Mines,
            Facilities
        };
        public static Upgrade QueuedUpgrade;

        static void Main(string[] args)
        {
            driver = Initialization();
            RetrieveResources();
            RetrieveAllCosts();
            RetrieveStorageCapacity();
            RetrieveProduction();
            DetermineCheapestUpgrade(PrimaryUpgrades);
        }
        #region Scraping
        /// <summary>Launches driver, connects to Ogame</summary>
        public static WebDriver Initialization()
        {
            ChromeOptions options = new ChromeOptions();
            options.AddArgument("--start-maximized");

            WebDriver driver = new ChromeDriver("C:\\Webdrivers", options);
            driver.Url = "https://lobby.ogame.gameforge.com/fr_FR/hub";
            Thread.Sleep(500);
            driver.FindElement(By.XPath("/html/body/div[3]/div/div/span[2]/button[2]")).Click();
            driver.FindElement(By.XPath("/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/ul/li[1]")).Click(); //Login Tab
            Thread.Sleep(500);
            driver.FindElement(By.XPath("/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/form/div[1]/div/input")).SendKeys(emailAdress);
            driver.FindElement(By.XPath("/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/form/div[2]/div/input")).SendKeys(passWord);
            Thread.Sleep(500);
            driver.FindElement(By.XPath("/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/form/p/button[1]/span")).Click();
            Thread.Sleep(2000);
            driver.FindElement(By.XPath("/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/button/span[1]")).Click();
            Thread.Sleep(2000);

            driver.Close();
            driver.SwitchTo().Window(driver.WindowHandles[0]);

            return driver;
        }
        public static void GoToTab(Tab desiredTab)
        {
            if (currentTab != Tab.Production)
            {
                if (desiredTab != Tab.Production)
                    driver.FindElement(By.XPath($"/html/body/div[6]/div[2]/div[2]/div/ul/li[{(int)desiredTab + 1}]/a")).Click();
                else
                    driver.FindElement(By.XPath("/html/body/div[6]/div[2]/div[2]/div/ul/li[2]/span/a/div")).Click();
            }
            else
                driver.FindElement(By.XPath($"/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[{(int)desiredTab + 1}]/a")).Click();
            currentTab = desiredTab;
            Thread.Sleep(2000);
        }  
        public static void RetrieveResources()
        {
            Metal = int.Parse(driver.FindElement(By.XPath("/html/body/div[6]/div[1]/div[2]/ul/li[1]/span/span")).Text.Replace(".", string.Empty));
            Crystal = int.Parse(driver.FindElement(By.XPath("/html/body/div[6]/div[1]/div[2]/ul/li[2]/span/span")).Text.Replace(".", string.Empty));
            Deuterium = int.Parse(driver.FindElement(By.XPath("/html/body/div[6]/div[1]/div[2]/ul/li[3]/span/span")).Text.Replace(".", string.Empty));
            Energy = int.Parse(driver.FindElement(By.XPath("/html/body/div[6]/div[1]/div[2]/ul/li[4]/span/span")).Text.Replace(".", string.Empty));
        }
        public static void RetrieveStorageCapacity()
        {
            if (currentTab != Tab.Production)
                GoToTab(Tab.Production);

            MetalCapacity = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[18]/td[2]/span")).Text.Replace(".", string.Empty));
            CrystalCapacity = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[18]/td[3]/span")).Text.Replace(".", string.Empty));
            DeuteriumCapacity = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[18]/td[4]/span")).Text.Replace(".", string.Empty));
        }
        public static void RetrieveProduction()
        {
            if (currentTab != Tab.Production)
                GoToTab(Tab.Production);

            MetalProduction = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[2]/span")).Text.Replace(".", string.Empty));
            CrystalProduction = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[3]/span")).Text.Replace(".", string.Empty));
            DeuteriumProduction = int.Parse(driver.FindElement(By.XPath("/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/table/tbody/tr[19]/td[4]/span")).Text.Replace(".", string.Empty));
        }
        public static void RetrieveAllCosts()
        {
            RetrieveMinesCosts();
            RetrievePlantCosts();
            RetrieveStorageCost();
            RetrieveFacilitiesCost();
        }
        public static void RetrieveMinesCosts()
        {
            if (currentTab != Tab.Resources)
                GoToTab(Tab.Resources);

            RetrieveCost(Mines, UpgradeType.Mine, Tab.Resources, 1, 3);
        }
        public static void RetrievePlantCosts()
        {
            if (currentTab != Tab.Resources)
                GoToTab(Tab.Resources);

            RetrieveCost(EnergyPlant, UpgradeType.EnergyPlant, Tab.Resources, 4, 5);
        }
        public static void RetrieveStorageCost()
        {
            if (currentTab != Tab.Resources)
                GoToTab(Tab.Resources);

            RetrieveCost(Storage, UpgradeType.Storage, Tab.Resources, 8, 10);
        }
        public static void RetrieveFacilitiesCost()
        {
            if (currentTab != Tab.Facilities)
                GoToTab(Tab.Facilities);

            RetrieveCost(Facilities, UpgradeType.Facility, Tab.Facilities, 1, 3);
        }
        public static void RetrieveCost(List<Upgrade> UpgradeList, UpgradeType type, Tab tab, int startIndex, int endIndex)
        {
            string pathToUpgrade = string.Empty;

            for (int i = startIndex; i <= endIndex; i++)
            {
                driver.FindElement(By.XPath($"/html/body/div[6]/div[3]/div[2]/div/div[{(tab == Tab.Resources ? 2 : 4)}]/ul/li[{i}]/span")).Click();
                Thread.Sleep(1000);

                List<int> costs = new List<int>() { 0, 0, 0, 0, 0 };
                ReadOnlyCollection<IWebElement> resourcesCosts;
                int index = 0;
                pathToUpgrade = $"/html/body/div[6]/div[3]/div[2]/div/div[{(tab == Tab.Resources ? 2 : 4)}]/ul/li[{i}]/span/button";
                costs[0] = ConvertTime(driver.FindElement(By.XPath($"/html/body/div[6]/div[3]/div[2]/div/div[{(tab == Tab.Resources ? 1 : 3)}]/div/div[2]/div[2]/div/ul/li/time")).Text);

                resourcesCosts = driver.FindElements(By.XPath($"/html/body/div[6]/div[3]/div[2]/div/div[{(tab == Tab.Resources ? 1 : 3)}]/div/div[2]/div[2]/div/div[1]/ul/li"));
                foreach (IWebElement cost in resourcesCosts)
                {
                    if (RetrieveResourceType(cost.GetAttribute("aria-label")) == "Métal")
                        costs[1] = int.Parse(resourcesCosts[index].Text.Replace(".", string.Empty));
                    else if (RetrieveResourceType(cost.GetAttribute("aria-label")) == "Cristal")
                        costs[2] = int.Parse(resourcesCosts[index].Text.Replace(".", string.Empty));
                    else if (RetrieveResourceType(cost.GetAttribute("aria-label")) == "Deutérium")
                        costs[3] = int.Parse(resourcesCosts[index].Text.Replace(".", string.Empty));

                    index++;
                }

                costs[4] = type == UpgradeType.Mine ? int.Parse(driver.FindElement(By.XPath("/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li[2]/span")).Text) : 0;
                UpgradeList.Add(new Upgrade(type, tab, new Cost(costs[0], costs[1], costs[2], costs[3], costs[4]), pathToUpgrade));
            }
        }
        public static string RetrieveResourceType(string arialabel)
        {
            string resourceType = string.Empty;

            foreach (char c in arialabel)
                if (!Char.IsWhiteSpace(c) && !Char.IsDigit(c) && c != '.')
                    resourceType += c;

            return resourceType;
        }
        public static int ConvertTime(string time)
        {
            string buffer = string.Empty;
            Dictionary<char, int> map = new Dictionary<char, int>();
            map.Add('h', 3600);
            map.Add('m', 60);
            map.Add('s', 1);

            int totalTime = 0;

            foreach (char c in time)
            {
                if (Char.IsDigit(c))
                    buffer += c;
                else if (c != ' ')
                {
                    totalTime += int.Parse(buffer) * map[c];
                    buffer = string.Empty;
                }
            }

            return totalTime;
        }
        #endregion
        #region Algorithm
        public static void DetermineCheapestUpgrade(List<List<Upgrade>> UpgradeList)
        {
            int cheapestListIndex = 0;
            int cheapestUpgradeIndex = 0;
            int lowestCost = int.MaxValue;

            int currentListIndex = 0;
            int currentUpgradeIndex = 0;
            int currentUpgradeCost = 0;

            foreach (List<Upgrade> list in UpgradeList)
            {
                currentUpgradeIndex = 0;

                foreach (Upgrade upgrade in list)
                {
                    currentUpgradeCost = upgrade.cost.Metal + upgrade.cost.Crystal + upgrade.cost.Deuterium;

                    if (lowestCost > currentUpgradeCost)
                    {
                        lowestCost = currentUpgradeCost;
                        cheapestListIndex = currentListIndex;
                        cheapestUpgradeIndex = currentUpgradeIndex;
                    }

                    currentUpgradeIndex++;
                }
                currentListIndex++;
            }

            QueueUpgrade(UpgradeList[cheapestListIndex][cheapestUpgradeIndex]);
        }
        public static void DetermineCheapestUpgrade(List<Upgrade> UpgradeList)
        {
            int cheapestUpgradeIndex = 0;
            int lowestCost = int.MaxValue;

            int currentUpgradeIndex = 0;
            int currentUpgradeCost = 0;

            foreach (Upgrade upgrade in UpgradeList)
            {
                currentUpgradeCost = upgrade.cost.Metal + upgrade.cost.Crystal + upgrade.cost.Deuterium;

                if (lowestCost > currentUpgradeCost)
                {
                    lowestCost = currentUpgradeCost;
                    cheapestUpgradeIndex = currentUpgradeIndex;
                }

                currentUpgradeIndex++;
            }

            QueueUpgrade(UpgradeList[cheapestUpgradeIndex]);
        }
        public static void QueueUpgrade(Upgrade upgradeToQueue)
        {
            if (upgradeToQueue.type == UpgradeType.Mine && upgradeToQueue.cost.Energy > Energy)
                DetermineCheapestUpgrade(EnergyPlant);
            else
            {
                if (upgradeToQueue.cost.Metal < Metal && upgradeToQueue.cost.Crystal < Crystal && upgradeToQueue.cost.Deuterium < Deuterium)
                    ProceedUpgrade(upgradeToQueue);
                    //if (CheckForCurrentUpgrade())
                    //    ProceedUpgrade(upgradeToQueue);
                    //else
                    //    ProceedUpgrade(upgradeToQueue, ConvertTime(driver.FindElement(By.XPath("/html/body/div[6]/div[3]/div[3]/div/div[2]/table/tbody/tr[4]/td/span")).Text));
            }
        }
        public static bool CheckForCurrentUpgrade()
        {
            GoToTab(Tab.Overview);
            return driver.FindElement(By.XPath("/html/body/div[6]/div[3]/div[3]/div/div[2]/table/tbody/tr/td/a")).Text == "Aucun bâtiment en construction.(Ressources)";
        }
        public static void ProceedUpgrade(Upgrade upgrade, int timeToWait)
        {
            Thread.Sleep(timeToWait);
            GoToTab(upgrade.tab);
            driver.FindElement(By.XPath(upgrade.upgradePath)).Click();
            Thread.Sleep(upgrade.cost.Time);
            DetermineCheapestUpgrade(PrimaryUpgrades);
        }
        public static void ProceedUpgrade(Upgrade upgrade)
        {
            GoToTab(upgrade.tab);
            driver.FindElement(By.XPath(upgrade.upgradePath)).Click();
            Thread.Sleep(upgrade.cost.Time * 1000);
            Update(upgrade.type);
        }
        public static void Update(UpgradeType type)
        {
            switch (type)
            {
                case UpgradeType.Mine:
                    RetrieveMinesCosts();
                    break;
                case UpgradeType.Facility:
                    RetrieveFacilitiesCost();
                    break;
                case UpgradeType.EnergyPlant:
                    RetrievePlantCosts();
                    break;
                case UpgradeType.Storage:
                    RetrieveStorageCost();
                    break;
            }
            RetrieveResources();
            DetermineCheapestUpgrade(PrimaryUpgrades);
        }
        #endregion
        public static void Debug()
        {
            Console.WriteLine($"Métal : {Metal}, Cristal : {Crystal}, Deut : {Deuterium}, Energy : {Energy}");
            for (int i = 0; i < Mines.Count; i++)
                Console.WriteLine($"Mines : {Mines[i].cost.Metal}, {Mines[i].cost.Crystal}, {Mines[i].cost.Deuterium}, {Mines[i].cost.Energy}, {Mines[i].cost.Time}");
            for (int i = 0; i < Storage.Count; i++)
                Console.WriteLine($"Storage : {Storage[i].cost.Metal}, {Storage[i].cost.Crystal}, {Storage[i].cost.Deuterium}, {Storage[i].cost.Energy}, {Storage[i].cost.Time}");
            for (int i = 0; i < EnergyPlant.Count; i++)
                Console.WriteLine($"Energy : {EnergyPlant[i].cost.Metal}, {EnergyPlant[i].cost.Crystal}, {EnergyPlant[i].cost.Deuterium}, {EnergyPlant[i].cost.Energy}, {EnergyPlant[i].cost.Time}");
            for (int i = 0; i < Facilities.Count; i++)
                Console.WriteLine($"Facilities : {Facilities[i].cost.Metal}, {Facilities[i].cost.Crystal}, {Facilities[i].cost.Deuterium}, {Facilities[i].cost.Energy}, {Facilities[i].cost.Time}");
        }
    }
}