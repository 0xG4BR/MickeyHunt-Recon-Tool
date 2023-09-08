import json
import subprocess
import requests
import sys
import signal


print(r"""                                                                          
                                                
       @@@@@@@@@                   @@@@@@@@@      
    @@@@@@@@@@@@@@@             @@@@@@@@@@@@@@@   
  @@@@@@@@@@@@@@@@@@%         @@@@@@@@@@@@@@@@    
  @@@@@@@@@@@@@@@@@@@         @@@@@ .@@@@@@@@@    
  @@@@@@@@@@@@@@@@@@@         @@@@@&*@@@@@@@@@@@@ 
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   
       @@@@@@@@@@@/  @@@@@@@@@@  @@@@@@@@@@@      
            @@@@ @    @@@@@@@,   , (@@@@          
           @@@@@      @@@@@@@@     @@@@@@         
          @@@@@@    ,@@@@@@@@@@    @@@@@@%        
          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
           @@@ @* @@@@@@@@@@@@@@@& @ %@@@         
            @@  @ @  .     %     . @ @@@          
             @@@  @   @@ @@&&.@  @ &@@@           
               &@@@@@@ @@, @ @@@@@@@&             
                   @@@@@@@@@@@@@@                
                   
                   """)



def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)


print("[+]Welcom to MickeyHunt\n")

url = "https://api.securitytrails.com/v1/domain/"+sys.argv[1]+"/subdomains?children_only=false&include_inactive=true"
 
headers = {
    "accept": "application/json",
    "APIKEY": "z5hr9vGQGaCs1DdEnHfBPEPFMFW" #Change API 
}
print("[+]Searching for subdomains...")

response = requests.get(url, headers=headers)

data  = json.loads(response.text)

print("[+]Finshed searching for subdomains")
print("[+]checking for active subdomains\n")

# opens file with the name of domain
f = open(sys.argv[1]+".txt", 'w')
counter = 0
for i in set(data['subdomains']):
    try:
        requests.head("https://"+i+"."+sys.argv[1],timeout=5)
        
        f.write("https://"+i+"."+sys.argv[1]+"\n")
        print(i+"."+sys.argv[1])
        counter+=1
    except requests.exceptions.RequestException :
            pass

print("\n[+]Found "+str(counter)+" active subdomains")
f.close()


print("[+]Starting vuln scan")

subprocess.run(["nuclei","-l",str(sys.argv[1])+".txt","-o",str(sys.argv[1])+"_vuln.txt"])

print("[+]Finshed scanning")

