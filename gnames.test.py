#! /usr/bin/env python

import datetime
import csv
import random
import logging
import click


def init (numToGenerate=10, companyDomain="company.com", defaultStart=datetime.date(2017,4,26),
        leaveProbability=0.3, managerProbability=0.05):
    surnames=["Smith","Johnson","Hammer","Cleese","Wang","Xhou","Palin","Gilliam","Idle","Chapman",
              "Garden","Jones","Atkinson","Perretti","Schumer","Noah","Stewart","Milligan","Davis",
              "Webb","Mitchell","Fey","Flannigan","Kamal","Fry","Carr","Colbert","Jefferies","Eddy",
              "Eoin","Enfield","Oddie","Garden","Brooke-Taylor","Sellers"]
    firstnames=["Bill","John","Timothy","Fung","Dwayne","Harry","Xavier","Graham","Michael","Terry","Alan",
                "Jane","Eric","Rowan","David","Amy","Tina","Chelsea","Spike","Kitty","The Machine",
                "Akmal","Jimmy","Stephen","Jim","Steady","Harry","Bill","Tim","Peter"]
    # As managers are assigned, add the index to this list, first user will always be a manager
    managers=[]
    namesUsed=[]
    
    maxPermutations = len(surnames) * len(firstnames)
    logging.debug("maxPermutations = %d", maxPermutations)
    if numToGenerate > maxPermutations:
        raise RuntimeError("Cannot generate that many unique names with current sample sizes [{:d} * {:d} = {:d}]".format(len(surnames), len(firstnames), maxPermutations))
    
    print("IDX,SURNAME,FIRST_NAME,EMAIL,MOBILE,IS_MANAGER,MANAGED_BY,START_DATE,END_DATE,PICTURE")
    for idx in range(numToGenerate):
        logging.debug("Generate user [%d/%d]", idx+1, numToGenerate)

        fname = ""
        sname = ""
        tryCount = 0
        while True:
            fname = random.choice(firstnames)
            sname = random.choice(surnames)
            logging.debug("Check username [%s]", sname + fname)
            if (sname+fname) not in namesUsed:
                namesUsed.append(sname+fname)
                break;
            if tryCount > (5 * numToGenerate):
                raise RuntimeError("Could not generate an unused name in {:d} attempts".format(5 * numToGenerate))
            logging.debug("Username [%s] rejected because it is already in use [Try %d/%d]", sname + fname, tryCount+1, 5 * numToGenerate)
            tryCount += 1

        startDelay = random.randint(-2, 2) + (random.randint(0, 7) * 7)
        startDate = defaultStart + datetime.timedelta(days=startDelay)

        endDate = startDate + datetime.timedelta(weeks=random.randint(0, 104)) if random.random() < leaveProbability else datetime.date(1970,1,1)
        endDbgString = (", (Finished: {:s}".format(endDate,)) if endDate > startDate else ""

        email = "%s.%s@%s" % (fname.lower().replace(' ', ''), sname.lower().replace(' ', ''), companyDomain)

        mobile = "04{0:02d} {1:03d} {2:03d}".format((random.randint(0, 7) * 10 + random.randint(0, 10)), random.randint(0, 1000), random.randint(0, 1000))

        # TODO: pic resource
        isManager = ((random.random() < managerProbability) and (endDate <= startDate)) or (idx == 0)
        myManager = random.choice(managers) if idx > 0 else -1
        
        # Append to managers list after assigning our own manager
        if isManager:
            managers.append(idx)
        managerDbgString = ("Manager IDX: {:d}\n".format(myManager,)) if myManager >= 0 else ""
        logging.debug("Employee: %s, %s %s\nStarted: %s%s\nMobile: %s, Email: %s%s\n",
                        sname.upper(), fname, "[Manager]" if isManager else "",
                        startDate, endDbgString,
                        mobile, email,
                        managerDbgString)
        csvString = "{:d},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},,".format(idx, sname, fname, email, mobile, str(isManager),
                        str(myManager) if myManager >= 0 else "", str(startDate), str(endDate) if endDate > startDate else "")
        print(csvString)
    

if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    logging.debug('Got [%d] args', len(sys.argv))
    init(numToGenerate=int(sys.argv[1]) if len(sys.argv) > 1 else 20)
    