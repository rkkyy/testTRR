#!/usr/bin/env python
#### =======================================================
import platform
import os
import sys
import requests
import json

## TODOs
        # cope with network issues:
        #     - e.g. firebase unresponsive
#### =======================================================

gtoken = "ya29.c.EluwBdn0hRoaw5skrAvMfH-jdIEYm7OatIjxfudcsrFkkMu5Fq8QcXl0Pt7Q-9Kxd7I3vtkhQDcfC3d8CjKc1JCH-AD6doOTSNSv3o0f2nHaMHqNs6SAJIrhNPoD"
bearerToken = "Bearer " + gtoken

def getBranch():
    result = os.environ.get('USER_BRANCH')
    return result

def getCoverageReport():
    # print("getCoverageReport()!")
    return 44.7

def getBaselineCoverageValue():
    baselineCoverageValue = getFireBaseData()
    return baselineCoverageValue

def getFireBaseData():
    # print("getting data")
    headers = {'Authorization': bearerToken}
    url = "https://test01-c0a07.firebaseio.com/REPOS/REPO01.json"
    r=requests.get(url, headers=headers)
    # print("response is: " + r.text)
    r.raise_for_status()
    baselineCoverage = r.json()["coverage"]
    return baselineCoverage

def sendFireBaseData(newCoverageValue):
    # print("sendFireBaseData()!")
    url = "https://test01-c0a07.firebaseio.com/REPOS/REPO01.json"
    data = { "coverage" : newCoverageValue }
    headers = {'Content-type': 'application/json',
                'Accept': 'text/plain',
                'Authorization': bearerToken}
    req = requests.put(url, data=json.dumps(data), headers=headers)
    req.raise_for_status()

def main():
    assert_on_coverage_drop = True

    curr_coverage = getCoverageReport()
    print ("===============================================")
    print("CURRENT COVERAGE (total lines %) IS: " + str(curr_coverage))
    baseline_coverage = getBaselineCoverageValue()
    print("BASELINE COVERAGE - COVERAGE LAST VALUE (total lines %) WAS: " + str(baseline_coverage))
    print ("===============================================")

    if getBranch()=="develop":
        print("This is the \"develop\" branch!")
        # print ("REPO_COVERAGE_TOTAL_LINES_PCT : " + str(curr_coverage))
        if (assert_on_coverage_drop):
            if (curr_coverage < baseline_coverage):
                print ("** Current coverage is less than previous value (" + str(baseline_coverage) + ") **")
                print ("--- current build will be failed.")
                return 1
            if (curr_coverage == baseline_coverage):
                print ("Coverage has stayed the same. No action taken.")
            else:
                print("Updating records with new coverage value: " + str(curr_coverage))
                sendFireBaseData(curr_coverage)
        else:
            print("Updating records with new coverage value: " + str(curr_coverage))
            sendFireBaseData(curr_coverage)
    return 0

#### =======================================================
if __name__ == '__main__':
    sys.exit(main())
