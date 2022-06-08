using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Ogame_Bot
{
    public class Upgrade
    {
        public UpgradeType type;
        public Tab tab;
        public Cost cost;
        public string upgradePath;

        public Upgrade(UpgradeType iUpgradeType, Tab iTab, Cost iCost, string iUpgradePath)
        {
            type = iUpgradeType;
            tab = iTab;
            cost = iCost;
            upgradePath = iUpgradePath;
        }
    }
}
