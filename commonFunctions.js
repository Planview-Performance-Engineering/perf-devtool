import http from 'k6/http';
import { fail } from "k6";
import { Rate, Trend } from "k6/metrics";
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';
import { parseHTML } from 'k6/html';


let passRate = new Rate(`RequestEndpointPassRate`)
let requestTimeoutRate = new Rate(`RequestEndpointRequestTimeoutRate`)
let responseTime = new Trend(`RequestEndpointResponseTime`, true)

let loginPassRate = new Rate(`LoginPassRate`)
let loginRequestTimeoutRate = new Rate(`LoginRequestTimeoutRate`)
let loginResponseTime = new Trend(`LoginResponseTime`, true)



export function awLogin(host, versionNumber, username, password, requestTimeout = '1m') {
    const LOGIN_URL = `${host}/${versionNumber}_Application/Pages/Service/Login.aspx?ReturnUrl=%2f${versionNumber}_Application%2f`

    const payload = {
        __VIEWSTATE: '',
        txtLogin: username,
        txtPassword: password,
        lbtLogin: 'Log In',
      }

    const headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    const params = {
        headers: headers,
        timeout: requestTimeout
    }

    const response = http.post(LOGIN_URL, payload, params);
    const objMetrics = {
        passRate: loginPassRate,
        reqTimeoutRate: loginRequestTimeoutRate,
        responseTimeRate: loginResponseTime
    }
    verifyPageLoadByTitle("Login", response, requestTimeout, "Cases - Clarizen.com", objMetrics, LOGIN_URL)
}

export function login(host, dsn, username, password, requestTimeout = '1m') {
    const LOGIN_URL = `${host}/planview/login/body.aspx?manual=y`

    const payload = {
        DSN: dsn,
        Username: username,
        UserPass: password
    }
    const headers = {
        "content-type": "application/x-www-form-urlencoded",
        "referer": `${host}/planview/login/body.aspx`
    }

    const params = {
        headers: headers,
        timeout: requestTimeout
    }

    console.log('==================',JSON.stringify(payload), LOGIN_URL)


    const response = http.post(LOGIN_URL, payload, params);
    // console.log('==================', response.body)

    const ADMIN_LOGIN_CERT = verifyLogin(response, username, requestTimeout)
    return ADMIN_LOGIN_CERT
}

export function getAccessToken(host, clientID, clientSecret){

    const url = `${host}/polaris/public-api/oauth/token`

    const requestBody = {
    client_id: clientID,
    client_secret: clientSecret,
    scope: NaN,
    grant_type : 'client_credentials'
    }

   const response = http.post(url, requestBody)
   const accessToken = verifyGetAccessToken(response)
   return accessToken

}

export function constructSummaryObj(CONFIG_ID, data, testData, logPath, requestTimeOut) {

    const RUN_NAME = __ENV['runName']

    let endDateObj = new Date()
    let strEndTime = endDateObj.toISOString()
    let testDuration = data['state']['testRunDurationMs']
    let numVirtualUsers = data['metrics']['vus_max']['values']['max']
    let totalIterations = data['metrics']['iteration_duration']['values']['count']

    let strStartTime = endDateObj - testDuration
    let startDateObj = new Date(strStartTime)
    strStartTime = startDateObj.toISOString()

    let testDurationMin = Math.round(testDuration / 60000)

    let testSummary = {
        "StartTime": strStartTime,
        "EndTime": strEndTime,
        "TestDurationMin": testDurationMin,
        "VirtualUsers": numVirtualUsers,
        "testData": testData,
        "RequestTimeOut": requestTimeOut,
        "TotalIterations": totalIterations
    }

    data['TestSummary'] = testSummary

    let strTime =strStartTime.replace(':', '-')
    strTime = strTime.replace(':', '-')

    let STR_TIMESTAMP = strTime.toString()
    let StrName = STR_TIMESTAMP.split(".");


    let FILE_PATH = (RUN_NAME) ? `${RUN_NAME}_${StrName[0]}` : `${StrName[0]}`


    let jsonPath = `${logPath}/${CONFIG_ID}/${FILE_PATH}.json`

    let resultSummary = { 'stdout': textSummary(data, { indent: ' ', enableColors: false }) }

    resultSummary[jsonPath] = JSON.stringify(data)

    console.log(`****************** TEST SUMMARY REPORT ${jsonPath} IS GENERATED ******************`)
    return resultSummary
}

function verifyGetAccessToken(response){
    let accessToken;
    try {
        accessToken = response.json()['access_token']

    } finally {
        if (response.status == 200) {
            return accessToken
        }
        else {
            fail(`Token API failed with, ${response.body}`)
        }
    }
}


function verifyLogin(response, username, requestTimeout) {

    let adminLoginCert
    let vuJar = http.cookieJar()
    let cookiesForLoginURL = vuJar.cookiesForURL(response.url)

    let { vu, iter } = getVUandITER()

    if ('LoginCert' in cookiesForLoginURL) {
        adminLoginCert = cookiesForLoginURL.LoginCert[0]
        console.log(`[VU: ${vu}  Iter: ${iter}] User ${username} login Cert: ${adminLoginCert}`)

        if (adminLoginCert.length < 20) {
            loginPassRate.add(false, { action: "Login"})
            loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout })
            fail(`[VU: ${vu}  Iter: ${iter}] Invalid login cert ${adminLoginCert} for user ${username}`)
        }
        else {
            loginPassRate.add(true, { action: "Login"})
            loginResponseTime.add(response.timings.duration, { action: "Login"})
            loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout})
        }
    }
    else if (response.error.includes('request timeout')) {
        loginPassRate.add(false, { action: "Login"})
        loginRequestTimeoutRate.add(true, { action: "Login", timeout: requestTimeout})
        fail(`[VU: ${vu}  Iter: ${iter}] Request timeout exception occured at Login`)
    }
    else {
        loginPassRate.add(false, { action: "Login"})
        loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout})
        fail(`[VU: ${vu}  Iter: ${iter}] Login Cert is not returned by Login API for user ${username}`)
    }
    return adminLoginCert
}


export function verifyResponseStatus(response, endPoint, apiAction, verifyString, requestTimeout){
        if (response.status == 200 && verifyString) {
            if (response.body.includes(verifyString)) {
                passRate.add(true, { action: apiAction, endPoint: endPoint })
                requestTimeoutRate.add(false, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
                responseTime.add(response.timings.duration, { action: apiAction, endPoint: endPoint })
            }
            else {
                passRate.add(false, { action: apiAction, endPoint: endPoint })
                fail(`Verification filaed for ${endPoint} endpoint`)
            }
        }
        else if (response.status == 200){
            passRate.add(true, { action: apiAction, endPoint: endPoint })
            requestTimeoutRate.add(false, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
            responseTime.add(response.timings.duration, { action: apiAction, endPoint: endPoint })
        }
        else if (response.error.includes('request timeout')) {
            passRate.add(false, { action: apiAction, endPoint: endPoint })
            requestTimeoutRate.add(true, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
            fail(`Request timeout exception occured while getting attributes,API url is:${endPoint}`)
        }
        else {
            passRate.add(false, { action: apiAction, endPoint: endPoint })
            fail(`${endPoint} endpoint failed with, ${response.body}`)
        }
}


export function getVUandITER() {
    let vu, iter
    if (typeof __ITER === 'undefined') {
        iter = 'setup/teardown'
        vu = 'setup/teardown'
    }
    else {
        iter = __ITER
        vu = __VU
    }
    return { vu, iter }
}

export function verifyPageLoadByTitle(action, response, requestTimeout, expectedPageTitle, objMetrics, reqUrl) {
    const SECTION = __ENV['section']
    let pageTitle = ''
    let { vu, iter } = getVUandITER()


    try {
        let doc = parseHTML(response.body);
        pageTitle = doc.find('title').text();
        // console.log('+++++++++++++++++++++++++++++++++++++++++++++', pageTitle)
    }
    finally {
        if (response.error.includes('request timeout')) {
            objMetrics.passRate.add(false, { action: action, section: SECTION })
            objMetrics.reqTimeoutRate.add(true, { action: action, timeout: requestTimeout, section: SECTION })
            fail(`[VU: ${vu}  Iter: ${iter}] Request timeout exception occured while loading - ${expectedPageTitle}. Request URL: ${reqUrl}. Request Timeout at: ${requestTimeout}`)
        }
        else if (pageTitle.includes(expectedPageTitle)) {
            objMetrics.passRate.add(true, { action: action, section: SECTION })
            objMetrics.reqTimeoutRate.add(false, { action: action, timeout: requestTimeout, section: SECTION })
            objMetrics.responseTimeRate.add(response.timings.duration, { action: action, section: SECTION })
        }
        else {
            objMetrics.passRate.add(false, { action: action, section: SECTION })
            objMetrics.reqTimeoutRate.add(false, { action: action, timeout: requestTimeout, section: SECTION })
            fail(`[VU: ${vu}  Iter: ${iter}] Page with title ${expectedPageTitle} failed to load. Response: , ${response.body}. Request URL: ${reqUrl}`)
        }
    }
}