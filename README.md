# Roblox Badge Creator
Wanted to start a Roblox badge walk game without having to manually create 5 badges each day, or without paying robux? This is a simple flask application to automate this process with some required setup.
<br>
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fp1gyy%2Frobloxbadgecreator&env=RBXCOOKIE,APIKEY,WEBHOOK&repository-name=robloxbadgecreator)
<br>
## How to deploy
1. ### Getting your .ROBLOSECURITY cookie
    1. Login to roblox on a private/incognito browser window
    2. If the game you are making badges for is part of a group, make sure the account has these permissions in the group:
        - Spend group funds, Create avatar items, Configure avatar items, Create and edit group experiences
    3. Right click on the page and click inspect element, then navigate to the storage tab
    4. Copy the **.ROBLOSECURITY** value and save it for step 2
2. ### Getting the gameid
    1. On roblox, click on the Create tab on the top navigation bar
    2. Click on Dashboard on that page
    3. If required, change the View As dropdown to your group (if the game is on a group)
    4. Select your game you want to create badges in
    5. On the browser URL/search bar, select and copy the numbers that come after **create.roblox.com/dashboard/creations/experiences/**
3. ### Clone the repository with Vercel using the button below
    - [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fp1gyy%2Frobloxbadgecreator&env=RBXCOOKIE,APIKEY,WEBHOOK&repository-name=robloxbadgecreator)
4. ### Fill in the enviroment variables for the new application, as defined below:
    - **RBXCOOKIE**: The account's .ROBLOSECURITY authentication cookie that you obtained before
    - **APIKEY**: It's like a password for the application. choose something only you would know, keeping it somewhere until required in step 6.
    - **WEBHOOK**: The URL of a discord webhook where the console output and status will be posted.
5. ### Deploy the application
    - Keep note for the **domain name** that is shown on the dashboard after deploying, as it will be required in step 6.
6. ### Setting up the daily scheduler with Postman
    1. Create an account on postman.com (there are other services that do this, but I personally used Postman)
    2. Create a collection under the collections tab, then create a new GET request using the plus in the top left
    3. For the url, set it to as follows, replacing the values in {} with the values you obtained before: 
        - **https://{PROJECT DOMAIN NAME}/makebadges/{YOUR API KEY}/{GAME ID}**
    4. Click on the Monitors tab and create a Monitor:
        - NAME: Set this to anything
        - COLLECTION: Select the collection you just made
        - RUN THIS MONITOR: Set this to **Week timer, Every day,** and the time of day you want it to activate
        - SELECT **Set request timeout**, and set it to **10000ms to 20000ms**
    5. Test your monitor by clicking RUN in the top right corner after selecting your monitor in the list