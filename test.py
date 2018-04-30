import sys
from nltk import word_tokenize
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

#Expected the absolute path the coordinates' files reside. eg. /Dir1/Dir2/'directory name of folder with cordinates'
dir_of_files = sys.argv[1]
##
#Expected the substring of the file name which is the same for every one. eg. 'coordinates_l1_0.1_0.2.txt' then name should be 'coordinates_l1_'
file_name = sys.argv[2]
##

abs_dir = dir_of_files

Nu = [0.0005,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
G = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

#Make theta Plot
#Define a function which accepts arguments to plot a graph
#  
def make_plot_thetas(title,labelx,labely,x,y):
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(22.5,14.5)
    plt.title(title,fontsize=24)
    plt.xlabel(labelx,fontsize=24)
    plt.ylabel(labely,fontsize=24)
    plt.scatter(x,y,s=5,c='r',marker='+')
    #plt.plot(x,y,'ro')
    plt.xticks(np.arange(0.0,6.908,0.628))
    plt.yticks(np.arange(0.0,6.908,0.628))
    fig.savefig('./plots/thetas/'+title,dpi = 100, bbox_inches='tight')
    plt.gcf().clear()
    #plt.show()
#END_OF_MAKE_PLOT
#

#Make radius Plot
#Define a function which accepts arguments to plot a graph
#  
def make_plot_radius(title,labelx,labely,x,y):
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(22.5,14.5)
    plt.title(title,fontsize=24)
    plt.xlabel(labelx,fontsize=24)
    plt.ylabel(labely,fontsize=24)
    plt.scatter(x,y,s=5,c='r',marker='+')
    plt.xticks(np.arange(0.0,16,0.750))
    plt.yticks(np.arange(0.0,16,0.750))
    fig.savefig('./plots/radius/'+title,dpi = 100, bbox_inches='tight')
    plt.gcf().clear()
    #plt.show()
#END_OF_MAKE_PLOT
#

#Make likelihood Plot
#Define a function which accepts arguments to plot a graph
#
def make_plot_ll(title,labelx,labely,x,y):
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(22.5,14.5)
    plt.title(title,fontsize=24)
    plt.xlabel(labelx,fontsize=24)
    plt.ylabel(labely,fontsize=24)
    plt.plot(x,y)
    fig.savefig('./plots/'+title,dpi = 100, bbox_inches='tight')
#END_OF_MAKE_PLOT
#

#Make_List
#Creates an object containing the 4 lists of equal sizes and same indeces
#
def make_list2(gt_file,emb_file):

    gt = [0]*1000
    emb = [0]*1000

    #Reading files (Output sorted lists)
    gt_line = gt_file.readline()
    emb_line = emb_file.readline()
    while emb_line or gt_line:
        gt_tok = word_tokenize(gt_line)
        gt[int(gt_tok[0])-1] = gt_tok[1]+'\t'+gt_tok[2]
        gt_line = gt_file.readline()
        try:
            emb_tok = word_tokenize(emb_line)
            emb[int(emb_tok[0])-1] = emb_tok[1]+'\t'+emb_tok[2]
            emb_line = emb_file.readline()
        except:
            w=0

    #Find which indeces dont exists in both lists
    iter_emb = emb
    temp_emb = []
    for i, value in enumerate(iter_emb):
        if value == 0:
            temp_emb.append(i)
    
    #Delete indeces which dont exist in both lists
    j=0
    for i in temp_emb:
        del emb[i-j]
        del gt[i-j]
        j+=1
    
    ##Return a list containing 4 lists
    lists = []
    gt_theta = []
    gt_rad = []
    emb_theta = []
    emb_rad = []
    for i in gt:
        tok = word_tokenize(i)
        gt_theta.append(float(tok[0]))
        gt_rad.append(float(tok[1]))
    for i in emb:
        tok = word_tokenize(i)
        emb_theta.append(float(tok[0]))
        emb_rad.append(float(tok[1]))
    lists.append(gt_theta)
    lists.append(gt_rad)
    lists.append(emb_theta)
    lists.append(emb_rad)
    return lists
#END_OF_MAKE_LIST

#Create all plots
i=0
for nuu in Nu:
    for ge in G:
        testfilegt = open(abs_dir+'../coordinates_l1.txt')
        file_l = open(dir_of_files+file_name+str(nuu)[0:3]+'_'+str(ge)[0:3]+'.txt')
        #In this section we iterate through every file and create the appropriate plots
        #
        #Comment out to do nothing
        ll = make_list2(testfilegt,file_l)
        gt_th = ll[0]
        gt_r = ll[1]
        emb_th = ll[2]
        emb_r = ll[3]
        make_plot_thetas("Thetas_"+str(nuu)[0]+'_'+str(nuu)[2]+'_'+str(ge)[0]+'_'+str(ge)[2],"Real Thetas","Infered Thetas",emb_th,gt_th)
        make_plot_radius("Radius_"+str(nuu)[0]+'_'+str(nuu)[2]+'_'+str(ge)[0]+'_'+str(ge)[2],"Real Radius","Infered Radius",emb_r,gt_r)
        i+=1
    print(i)
#
#

#make_plot_radius(rad_list)
#Plotting log likelyhoods with legend
g = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.8,0.9]
nu = ["0.0005","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(22.5,14.5)
plt.title('LL vs G',fontsize=24)
plt.xlabel('Log Likelihood',fontsize=24)
plt.ylabel('G correlation',fontsize=24)
llind = [0]*10
lllab = [0]*10
i=0
for Nuu in nu:
    llfile = open(abs_dir+'./likelihoods_'+Nuu+'.txt')
    line = llfile.readline()
    llunp = []
    llpen = []
    while line:
        toks = word_tokenize(line)
        llunp.append(float(toks[1]))
        llpen.append(float(toks[2]))
        line = llfile.readline()
    llind[i], = plt.plot(g,llpen[:9],label = Nuu)
    lllab[i] = Nuu
    i+=1
plt.legend(handles=[llind[0],llind[1],llind[2],llind[3],llind[4],llind[5],llind[6],llind[7],llind[8],llind[9]],
labels=[lllab[0],lllab[1],lllab[2],lllab[3],lllab[4],lllab[5],lllab[6],lllab[7],lllab[9]])
plt.show()
#