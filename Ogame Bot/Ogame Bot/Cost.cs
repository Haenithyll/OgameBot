using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Ogame_Bot
{
    public class Cost
    {
        public int Time;
        public int Metal;
        public int Crystal;
        public int Deuterium;
        public int Energy;

        public Cost(int iTime, int iMetal, int iCrystal, int iDeuterium, int iEnergy)
        {
            Time = iTime;
            Metal = iMetal;
            Crystal = iCrystal;
            Deuterium = iDeuterium;
            Energy = iEnergy;
        }
    }
}
