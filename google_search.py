*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${URL}        https://www.google.com
${SEARCH_TERM}    Amazon

*** Test Cases ***
Google Search And Capture Report
    [Documentation]    Perform a Google search and capture a report with title and screenshot.
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name:q    10
    Input Text    name:q    ${SEARCH_TERM}
    Press Keys    name:q    ENTER
    Wait Until Element Is Visible    id:search    10
    Capture Page Screenshot    search_results.png
    ${title}=    Get Title
    Log    The page title is: ${title}
    Close Browser

