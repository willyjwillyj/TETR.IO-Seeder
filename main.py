import tkinter as tk
import requests
import time
import webbrowser
root = tk.Tk()
root.title("TETR.IO Seeder")
root.geometry("500x500")

def getSeedings():
    global rankvar
    global outvar
    global eentry
    global sentry
    global rentry
    global rankcapcheck
    global unrankcheck
    global rankslist
    
    players = eentry.get("1.0", tk.END).split("\n")
    players.pop()
    api_base = "https://ch.tetr.io/api/users/"
    values = []
    names = []
    ranks = []
    delnames = []
    mranks = []
    for i in range(len(players)):
        outvar.set("fetching player " + str(i+1) + " of " + str(len(players)))
        root.update()
        pname = players[i]
        headers = requests.utils.default_headers()
        headers["User-Agent"] = "willyjwillyj Seeder Script"
        data = requests.get(api_base + pname.lower() + "/summaries/league", headers=headers) 
        try:
            item = data.json()["data"]["tr"]
        except:
            item = -1
        try:
            rank = data.json()["data"]["rank"]
        except:
            rank = "z"
        try:
            mrank = data.json()["data"]["bestrank"]
            if(considerPreviousSeason.get() == 1):

                for i in data.json()["data"]["past"]:
                    this_data = data.json()["data"]["past"][i]
                    
                    if(this_data["bestrank"] is not None):
                        
                        if(rankslist.index(mrank) > rankslist.index(this_data["bestrank"])):
                            print(this_data)
                            mrank = this_data["bestrank"]
        except:
            mrank = "z"
        values.append(item)
        names.append(pname)
        ranks.append(rank)
        mranks.append(mrank)
        time.sleep(1)

        
    #filter out bad users
    i = 0
    while i < len(names):
        removed = False
        if unrankcheck.get() == 1:
            if ranks[i] == "z":
                removed = True
                values.pop(i)
                delnames.append(names.pop(i))
                ranks.pop(i)
                mranks.pop(i)
        if (rankcapcheck.get() == 1) and (not removed):
            try:
                prankindex = rankslist.index(mranks[i])
                ranklimindex = rankslist.index(rankvar.get())
                if prankindex < ranklimindex:
                    removed = True
                    values.pop(i)
                    delnames.append(names.pop(i))
                    ranks.pop(i)
                    mranks.pop(i)
            except:
                print(mranks[i])
                print("net error")
        if (rankfloorcheck.get() == 1) and (not removed):
            try:
                prankindex = rankslist.index(mranks[i])
                rankfloorindex = rankslist.index(ranklowvar.get())
                if prankindex > rankfloorindex:
                    removed = True
                    values.pop(i)
                    delnames.append(names.pop(i))
                    ranks.pop(i)
                    mranks.pop(i)
            except:
                print("net error")
        if not removed:
            i += 1
    sl = sorted(zip(values, names),reverse=True)
    names = [point[1] for point in sl]
    sentry.delete("1.0", tk.END)
    sentry.insert(tk.END,"\n".join(names))
    rentry.delete("1.0", tk.END)
    rentry.insert(tk.END,"\n".join(delnames))

        

current_version = "v1.2.0"
github_connection_success = False
newest_version = current_version

try:
    release_data = requests.get("https://api.github.com/repos/willyjwillyj/TETR.IO-Seeder/releases/latest")
    newest_version = (release_data.json()["name"])
except:
    pass
else:
    github_connection_success = True
    

ver_label = tk.Label(master=root, text="You are using version " + current_version)
ver_label.grid(row=0,column=0)

if github_connection_success:
    if newest_version == current_version:
        ver_label_success = tk.Label(master=root, text="You are on the latest version")
        ver_label_success.grid(row=0,column=1)
    else:
        ver_label_failure = tk.Button(master=root, text="Update to the latest version", command=lambda:webbrowser.open("https://github.com/willyjwillyj/TETR.IO-Seeder/releases", new=0, autoraise=True))
        ver_label_failure.grid(row=0,column=1)
else:
    ver_label_failure = tk.Label(master=root, text="Failed to discover latest version")
    ver_label_failure.grid(row=0,column=1)





elabel = tk.Label(master=root, text="Input Players")
eentry = tk.Text(master=root, width=20, height=5)
elabel.grid(column=0, row=1,columnspan=1)
eentry.grid(column=0, row=2, columnspan=2)

unrankcheck = tk.IntVar(master=root)
settingRemoveUnrankedLabel = tk.Label(master=root, text="Remove Unranked")
settingRemoveUnrankedCheckbox = tk.Checkbutton(master=root, variable=unrankcheck)
settingRemoveUnrankedLabel.grid(column=0, row=3)
settingRemoveUnrankedCheckbox.grid(column=1,row=3)

rankslist = ["x+","x", "u", "ss", "s+", "s", "s-", "a+", "a", "a-", "b+", "b", "b-", "c+", "c", "c-", "d", "d-"]

rankcapcheck = tk.IntVar(master=root)
settingRemoveRankCapLabel = tk.Label(master=root, text="Remove Above Max Rank")
settingRemoveRankCapCheckbox = tk.Checkbutton(master=root, variable=rankcapcheck)
rankvar = tk.StringVar(master=root, value="ss")
settingRemoveRankCapDropdown = tk.OptionMenu(root, rankvar, *rankslist)
settingRemoveRankCapLabel.grid(column=0,row=4)
settingRemoveRankCapCheckbox.grid(column=1,row=4)
settingRemoveRankCapDropdown.grid(column=2,row=4)

rankfloorcheck = tk.IntVar(master=root)
settingRemoveRankFloorLabel = tk.Label(master=root, text="Remove Below Max Rank Floor")
settingRemoveRankFloorCheckbox = tk.Checkbutton(master=root, variable=rankfloorcheck)
ranklowvar = tk.StringVar(master=root, value="ss")
settingRemoveRankFloorDropdown = tk.OptionMenu(root, ranklowvar, *rankslist)
settingRemoveRankFloorLabel.grid(column=0,row=5)
settingRemoveRankFloorCheckbox.grid(column=1,row=5)
settingRemoveRankFloorDropdown.grid(column=2,row=5)

considerPreviousSeason = tk.IntVar(master=root)
considerPreviousSeasonLabel = tk.Label(master=root, text="Consider Previous Seasons For Rank Caps/Floors")
considerPreviousSeasonCheckbox = tk.Checkbutton(master=root, variable=considerPreviousSeason)
considerPreviousSeasonLabel.grid(row=6,column=0)
considerPreviousSeasonCheckbox.grid(row=6,column=1)



seedbutton = tk.Button(master=root, text="Get Seedings", command=getSeedings)
outvar = tk.StringVar(master=root)
seedStatus = tk.Label(master=root, textvariable=outvar)
seedbutton.grid(column=0, row=7)
seedStatus.grid(column=1, row=7)

slabel = tk.Label(master=root, text="Seeded Players")
sentry = tk.Text(master=root, width=20, height=5)
slabel.grid(column=0,row=8, columnspan=1)
sentry.grid(column=0,row=9, columnspan=2)

rlabel = tk.Label(master=root, text="Removed Players")
rentry = tk.Text(master=root, width=20, height=5)
rlabel.grid(column=0,row=10, columnspan=1)
rentry.grid(column=0,row=11, columnspan=2)


root.mainloop()