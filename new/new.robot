*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://www.google.com
${BROWSER}    Chrome

*** Test Cases ***
Scenario: User can open the Google homepage
    Given the browser is open    ${BROWSER}
    When I navigate to the homepage
    Then the title should be Google

*** Keywords ***
Given the browser is open
    [Arguments]    ${BROWSER}
    Open Browser    ${URL}    ${BROWSER}

When I navigate to the homepage
    Go To    ${URL}

Then the title should be Google
    Title Should Be    Google
