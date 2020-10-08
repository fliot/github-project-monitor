import re, requests, sys

if len(sys.argv) < 2:
    print("Use a github project as parameter")
    print("- example:")
    print("      >  python3 forks-level.py https://github.com/constverum/ProxyBroker")
    sys.exit(2)

project = sys.argv[1]
if "https://github.com" not in sys.argv[1]:
    project = "https://github.com/%s" % project 

if project.endswith("/"):
    project = project[0:-1]

r = requests.get(project)
if r.status_code != 200:
    print("Project %s not found !" % project)
    sys.exit(2)


print("Reviewing forks of project: %s" % project)
r = requests.get("%s/network/members" % project)
urls = re.findall(r'href=[\'"]?([^\'" >]+)', r.text)

dico = {}

for i in urls:
    if i.startswith("/") and len(i.split("/")) == 3 and not(i.startswith("/features/")):
        # relativelly good approximation....
        url = "https://github.com%s" % i
        s = requests.get(url)
        try:
            txt = s.text.split('<div class="d-flex flex-auto">')[1].split('</div>')[0].strip()
            print("%s       %s" % (url, txt))
            if "ahead" in txt:
                dico[url] = txt
        except:
            print(url)

print("########################################################################################")
for i in dico.keys():
    print("%s       %s" % (i, dico[i]))

import pdb; pdb.set_trace()
