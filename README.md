<!-- Original Author - Swastik2442 (https://github.com/Swastik2442) -->

# FB-to-Discord
Send Latest Facebook Posts to Discord using Discord Webhooks

> Note: This only works for Public Accounts.

## Setup

* Clone the repo using `git clone https://github.com/Swastik2442/FB-to-Discord.git`
* Run this command from the Repo Directory `pip install -r requirements.txt --no-cache-dir`
* Add a File with name `.env` and create the following Variables-
    * `PAGE_NAME`
    * `DISCORD_WEBHOOK` <!-- https://i.imgur.com/f9XnAew.png -->
    * `PAGE_PROFILE_URL` (Optional)
* Create a file with the name `cookiefile.txt` in the same folder as the program & add Cookies from Facebook.

<details><summary>How to get Cookies file-</summary>

You can extract cookies from your browser after logging into Facebook with an extension like [Get Cookies.txt (Chrome)](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) or [Cookie Quick Manager (Firefox)](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/). Make sure that you include both the `c_user` cookie and the `xs` cookie, you will get an InvalidCookies exception if you don't.
</details>

> Special Thanks to [facebook-scraper](https://github.com/kevinzg/facebook-scraper) Module
