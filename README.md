# sugg-script
backpack.tf suggestion script for premium users to make suggestions easier

## SETUP

Install python **2.7.x** from http://python.org

Run setup.bat on Windows, or setup.sh on Linux.

Run Main.py. You will be presented with a prompt asking you to enter a cookie.

To get the cookie, go to backpack.tf while logged in, and type: "javascript: alert(document.cookie)". Type, it, don't copy paste; most browsers remove the "javascript: " part. In the alert box is your cookie. Copy and paste it into the script's prompt.

The cookie will get saved in the data/cookie.txt file so you only need to enter it once.

Now, You will be presented with another prompt, asking for your URL. You need to enter the premium page of the item you want to get sales for. Just go to a premium search page and copy the URL in your browser. So for example, for a disco beatdown Team Captain: Go to backpack.tf/premium/search, fill in "Team Captain" at the item field, "Disco Beatdown" at the effect field, and click on the "Confirm" button. You will get the URL. In this case: "http://backpack.tf/premium/search?item=Team%20Captain&particle=62". This script only handles single pages at the moment. If your unusual has multiple pages, you will need to browse to the next page and run the script again.

You will be presented with yet another prompt now, asking for an outfile. Name this anything you like. I'd recommend something like "effect-hat.txt", so with out previous example, "dbd-teamcaptain.txt". 

After running the script, browse to the "output" dir, and open the file which name you entered in the outfile prompt.

### DISCLAIMER

Nothing you enter will be sent to 3rd parties.

This script doesn't work nicely with duped unusuals. 

