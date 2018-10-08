#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import sys
import os
import pandas as ps
p = os.path.abspath('..')
sys.path.append(p+"/")

class Downloader:
    def __init__(self, city):
        self.city = city
        self.ssh_bigdatadb = "cocca@bigdatadb.polito.it:"
        self.ssh_tlcdocker1 = "d046373@polito.it@tlcdocker1.polito.it:"
        self.src_home_oo = "/data/03/Carsharing_data/output/"
        self.src_home_oa = "/data/03/Carsharing_data/output_analysis/"
        self.dst_home = "../data"+city+"/"
        self.plt_home = "../plot"+city+"/"
        self.plt_aggr = "../plotAggregated/"
    
    def changeDstHome(self, city):
        self.city = city
        self.dst_home = "../data"+city+"/"
        self.plt_home = "../plot"+city+"/"
        
    
    def acquireLastSimulationID(self):
        lastS = int(subprocess.check_output("ssh bigdatadb \
                                     ls -tr " + src_home_oa   +\
                                     "| tail -1 \
                                     | tr -d Simulation_ ", shell=True))
        return lastS
    
    def dowloadOutAnalysis(self, simID):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
        
        src1 = self.ssh_bigdatadb + self.src_home_oa + "Simulation_"+str(lastS) + "/out_analysis.txt "
        
        fileName="out_analysis_"+str(lastS)+"_cr.txt"
        dst =  self.dst_home + fileName
        print ('scp ' + src1 + dst)
        os.system('scp ' + src1 + dst)
        print ("Simulation_",lastS,"correctly downloaded")
        return lastS, fileName
    
    def downloadLog(self, simID, policy, algorithm, zones,acs,tt,wt,utt,p):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
        
    
        fileName= "car2go_%s_%s_%d_%d_%d_%d_%d_%d.txt" %(policy,algorithm, zones,acs,tt,wt,utt,p)
        src1 = self.ssh_bigdatadb + self.src_home_oo + "Simulation_"+str(lastS) + "/"+ fileName + " "
    
        dst =  self.dst_home + fileName 
        os.system('scp ' + src1 + dst)
        print (fileName, "correctly downloaded")
        return fileName
    
    def downloadPlacementOrder(self, algorithm, city):
        name = "car2go_" + algorithm + "500.csv"
        
        command = "ssh -t d046373@polito.it@tlcdocker1.polito.it "
    #    awk_script =""
    #    awk_script = "\"awk -F\",\" '{print \$1}' /home/d046373@polito.it/sim3.0/input/"+name+"\""
        
        cat_script = "cat /home/d046373@polito.it/"+self.city+"sim3.0/input/"+name
    
        result = subprocess.Popen([command + cat_script], 
                                stdout=subprocess.PIPE, shell=True)
    #    result = result.stdout.decode('utf-8')
        result, err = result.communicate()
        result = result.decode('utf-8')
        result_list = result.split("\n")[1:-1]
        out =[]
        for i in result_list:
            out.append(int(i.split(",")[0]))
        return out
    
    def downloadBookingsStats(self, city):
    #    command = "ssh -t d046373@polito.it@tlcdocker1.polito.it "
    #    awk_script =""
    #    awk_script = "\"awk -F\",\" '{print \$1}' /home/d046373@polito.it/sim3.0/input/"+name+"\"
        dwld_script = "scp d046373@polito.it@tlcdocker1.polito.it:/home/d046373@polito.it/"+city.capitalize()+"_sim3.0/input/stats_on_bookings "
        dwld_script += dst_home
        print (dwld_script)
        result = subprocess.Popen([dwld_script], 
                                stdout=subprocess.PIPE, shell=True)
        df = pd.read_pickle("/Users/mc/Desktop/csExp/dataVancouver/stats_on_bookings")
        return df
    
    def downloadBookingsPerHour(self, city):
        
#        srvr_ssh = "d046373@polito.it@tlcdocker1.polito.it:"
#        srvr_ssh += "/home/d046373@polito.it/%s_sim3.0/output_analysis/bookings_per_hour_%s "%(self.city, self.city)
#        dst = self.dst_home + "bookings_per_hour_"+self.city+".csv"
#        os.system('scp ' + srvr_ssh + dst)
        if city == 'Berlino': 
            city_dld= 'Berlin'
        else: 
            city_dld = city

        cmd = 'scp tlcdocker2:/home/d046373@polito.it/sim3.0/input/bookings_per_hour_%s.csv '%(city_dld)
        cmd +='../data%s/bookings_per_hour_%s.csv' %(city,city)
        os.system(cmd)
        print ("bookings_per_hour_"+city+".csv", "downloaded" )
        return
    
    def downloadBookingsPerDay(self, city):
        
#        srvr_ssh = "d046373@polito.it@tlcdocker1.polito.it:"
#        srvr_ssh += "/home/d046373@polito.it/%s_sim3.0/output_analysis/bookings_per_hour_%s "%(self.city, self.city)
#        dst = self.dst_home + "bookings_per_hour_"+self.city+".csv"
#        os.system('scp ' + srvr_ssh + dst)
        if city == 'Berlino': 
            city_dld= 'Berlin'
        else: 
            city_dld = city

        cmd = 'scp tlcdocker2:/home/d046373@polito.it/sim3.0/input/bookings_per_day_%s.csv '%(city_dld)
        cmd +='../data%s/bookings_per_day_%s.csv' %(city,city)
        os.system(cmd)
        print ("bookings_per_day_"+city+".csv", "downloaded" )
        return
    
        
    def downloadBookingsInCsv(self, city):
        
#        srvr_ssh = "d046373@polito.it@tlcdocker1.polito.it:"
#        srvr_ssh += "/home/d046373@polito.it/%s_sim3.0/output_analysis/bookings_per_hour_%s "%(self.city, self.city)
#        dst = self.dst_home + "bookings_per_hour_"+self.city+".csv"
#        os.system('scp ' + srvr_ssh + dst)
        
        cmd = 'scp tlcdocker1:/home/d046373@polito.it/%s_sim3.0/input/%s_completeDataset.csv '%(city, city)
        cmd +='../data%s/' %(city)
        os.system(cmd)
        print ("%s_CompleteDatset downloaded"%city)
        return
    
    def downloadFleetPerDayPickle(self, city):
        cmd = 'scp tlcdocker1:/home/d046373@polito.it/%s_sim3.0/input/fleet_per_day '%(city)
        cmd +='../data%s/%s_fleet_per_day' %(city,city)
        os.system(cmd)
        print ("%s_fleet_per_day downloaded"%city)
        return

    def downloadLogHDFS(self, simID, policy, algorithm, zones, acs, tt, wt, p, city, fromSSD, kwh=''):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
            
        
        '''
        car2go_Hybrid_max-parking_24_4_25_1000000_100_100.txt
        car2go_Hybrid_max-parking_22_4_25_1000000_100_25_2.txt
        '''
        strOutput = ""
        attempt = 0
        while len(strOutput) == 0 and attempt<=2:
            if len(str(kwh)) == 0 :
                fileName= "car2go_%s_%s_%d_%d_%d_%d_%d.txt" %(policy,algorithm, zones,acs,
                                                                 tt,wt,p)
            else:
                fileName= "car2go_%s_%s_%d_%d_%d_%d_%d_%d.txt" %(policy,algorithm, zones,acs,
                                                                    tt,wt,p, kwh)
                
            if fromSSD ==True: return fileName
            print(11111)
    
            bashCommand = "ssh cocca@bigdatadb "+\
              "hdfs dfs -cat "+\
              "Simulator/output/Simulation_"+ str(simID) +"/"+\
              fileName
              
        
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            strOutput =  output.decode("utf-8") 
            
            print ("city:",city, "====", "zones:", zones, "====", len(strOutput))
            zones += 1
            attempt +=1
        
        path = "../data"+city+"/"
        newFileName = fileName
        
        f = open(path+newFileName, "w")
        f.write(strOutput)
        f.close()
        
        return fileName
    
    def downloadOptLogs(self, city, filename_root):
        path_in_docker = '/home/d046373@polito.it/test_on_danilo_fix/sim3.0/output/'
        if 'genetic' in filename_root:
            path_in_docker+='simulazioni/'
        
        all_files_in_dir = subprocess.check_output(['ls', '../data'+city]).decode("utf-8").split('\n')
        all_files = subprocess.check_output(['ssh', 'tlcdocker1', 'ls', path_in_docker]).decode("utf-8").split('\n')

        dowloaded = 0
        for file in all_files:
            if filename_root in file and file not in all_files_in_dir:
                
                subprocess.check_output(['scp', 'tlcdocker1:'+path_in_docker+file, '../data'+city]) 
                print('downloaded', path_in_docker+file)
                dowloaded +=1
        print ('Downloaded %d files'%dowloaded )
        return

#
#dld = Downloader("Torino")
#dld.downloadOptLogs(dld.city, 'genetico')

    
    



       
        

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
