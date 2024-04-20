import tkinter as tk
import requests
root = tk.Tk()
root.geometry("400x400")

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
    print(players)
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
        data = requests.get(api_base + pname.lower())
        try:
            item = data.json()["data"]["user"]["league"]["rating"]
            rank = data.json()["data"]["user"]["league"]["rank"]
            mrank = data.json()["data"]["user"]["league"]["bestrank"]
        except:
            item = -1
            rank = "z"
            mrank = "z"
        values.append(item)
        names.append(pname)
        ranks.append(rank)
        mranks.append(mrank)

        
    #filter out bad users
    i = 0
    print(unrankcheck.get())
    print(rankcapcheck.get())
    print(mranks)
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
                print(prankindex)
                print(ranklimindex)
                if prankindex < ranklimindex:
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

        



elabel = tk.Label(master=root, text="Input Players")
eentry = tk.Text(master=root, width=20, height=5)
elabel.grid(column=0, row=0,columnspan=1)
eentry.grid(column=0, row=1, columnspan=2)

unrankcheck = tk.IntVar(master=root)
settingRemoveUnrankedLabel = tk.Label(master=root, text="Remove Unranked")
settingRemoveUnrankedCheckbox = tk.Checkbutton(master=root, variable=unrankcheck)
settingRemoveUnrankedLabel.grid(column=0, row=2)
settingRemoveUnrankedCheckbox.grid(column=1,row=2)

rankcapcheck = tk.IntVar(master=root)
rankslist = ["x", "u", "ss", "s+", "s", "s-", "a+", "a", "a-", "b+", "b", "b-", "c+", "c", "c-", "d", "d-"]
settingRemoveRankCapLabel = tk.Label(master=root, text="Remove Above Max Rank")
settingRemoveRankCapCheckbox = tk.Checkbutton(master=root, variable=rankcapcheck)
rankvar = tk.StringVar(master=root, value="ss")
settingRemoveRankCapDropdown = tk.OptionMenu(root, rankvar, *rankslist)
settingRemoveRankCapLabel.grid(column=0,row=3)
settingRemoveRankCapCheckbox.grid(column=1,row=3)
settingRemoveRankCapDropdown.grid(column=2,row=3)


seedbutton = tk.Button(master=root, text="Get Seedings", command=getSeedings)
outvar = tk.StringVar(master=root)
seedStatus = tk.Label(master=root, textvariable=outvar)
seedbutton.grid(column=0, row=4)
seedStatus.grid(column=1, row=4)

slabel = tk.Label(master=root, text="Seeded Players")
sentry = tk.Text(master=root, width=20, height=5)
slabel.grid(column=0,row=5, columnspan=1)
sentry.grid(column=0,row=6, columnspan=2)

rlabel = tk.Label(master=root, text="Removed Players")
rentry = tk.Text(master=root, width=20, height=5)
rlabel.grid(column=0,row=7, columnspan=1)
rentry.grid(column=0,row=8, columnspan=2)


root.mainloop()