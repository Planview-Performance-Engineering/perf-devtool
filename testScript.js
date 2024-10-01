import http from 'k6/http';
import { group, sleep } from "k6";
import { fail } from "k6";
import { Rate, Trend } from "k6/metrics";
import { findBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

import * as commonFunctions from './commonFunctions.js'

// let testData = open("./data/configuration/config.json")
// testData = JSON.parse(testData)

const CONFIG_ID = __ENV['configID']

let testData = {}
let REQUEST_TIME_OUT = ''



export default function main(){
    
    
}

export function handleSummary(data) {
  let logPath = `./data/resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(CONFIG_ID, data, testData, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}