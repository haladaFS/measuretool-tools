import os
import numpy as np
import re
from matplotlib.pyplot import *

### Konfigurace ###
path = './LWL/measuretool/'
t_steps = 3 #Kolik casovych kroku k prumerovani
bottom_lev = 0.045 #Uroven dna
almost_zero = 0.05 #Offset pro odstraneni nulovych okraju

### Deklarace ###
files = []; x_pos = []; y_pos = []; z_pos = []
mt_files = []

### Objekt jednoho souboru measuretoolu ###
class MT_file:
    # Konstruktor
    def __init__(self, _name, _x_pos, _y_pos, _z_pos):
        self.name = _name
        self.x_pos = _x_pos; self.y_pos = _y_pos; self.y_pos = _y_pos
        # Deklarace potrebnych promennych
        self.h_list = []
        self.h_list_avg = []
        self.h_list_f = [] # Odfiltrovane nulove hodnoty
        self.h_list_avg_f = [] # Odfiltrovne nulove hodnoty
        self.x_pos_f = [] # Odfiltrovane nulove hodnoty
        self.h_tot = 0
    # Pridani vysek z dane casove vrstvy
    def append_h(self,_h_arr):
        self.h_list.append(_h_arr)
    # Plot jednotlivych rezu
    def plot_h(self): # <- predelat na jednu plotovaci globalni funkci
        # Konfigurace grafu
        fig = figure(figsize=(10,5))
        ax1 = fig.add_subplot(111)
        xlabel('x [m]', fontsize=15); ylabel('h [m]', fontsize=15)
        title("Profil hladiny, y = " + str(self.y_pos[0]) + "m", fontsize=20) # <- udelat lepe
        grid(color='k', linestyle='--', linewidth=0.5)
        ax1.tick_params(labelsize=12)
        # Plot hodnot
        for i in self.h_list_f: # <- odstranit _f pro plot celeho MT
            ax1.plot(self.x_pos_f, i,linewidth=1)
        ax1.plot(self.x_pos_f, self.h_list_avg_f,linewidth=4,color="green",markersize="12",marker="o",label='h avg')
        # Obrazkvy vystup
        legend(loc='upper right',fontsize=15);
        plt_name = "h_level_y=" + str(self.y_pos[0]) + "_avg_h=" + str(round(self.h_tot,3)) + ".png" # <- udelat lepe
        fig.savefig(plt_name)
        ## show()
    # Prumerovani vysek v rezu daneho souboru
    def make_avg(self):
        h_tot = 0
        counter_tot = 0
        for i in range(0, len(self.x_pos)): # <- udelat lepe
            h_temp = 0
            counter = 0
            for j in self.h_list:
                h_temp += j[i]
                counter += 1
            self.h_list_avg.append(h_temp/counter)
            if h_temp/counter > almost_zero:
                h_tot += h_temp/counter
                counter_tot += 1
        self.h_tot = h_tot/counter_tot
    # Odfiltruje nulove hodnoty pro grafy
    def filter_zeros(self):
        for i in self.h_list:
            list_temp = []
            for j in i:
                if j > almost_zero:
                    list_temp.append(j)
            self.h_list_f.append(list_temp)
        for i in range(0, len(self.h_list_avg)):
            if self.h_list_avg[i] > almost_zero:
                self.h_list_avg_f.append(self.h_list_avg[i])
                self.x_pos_f.append(self.x_pos[i])
    # Odecte uroven dna
    def apply_offset(self):
        for i in range(0, len(self.h_list)):
            for j in range(0, len(self.h_list[i])):
                self.h_list[i][j] -=  bottom_lev
        for i in range(0, len(self.h_list_avg)):
            self.h_list_avg[i] -= bottom_lev
        self.h_tot -= bottom_lev
    # Kontrolni
    def print_h(self):
        print("Length of h_list: ", len(self.h_list))
        print("Name of file: ", self.name)
        print("Avg height level: ", self.h_tot)
        print("Avg height vector: ", np.round(self.h_list_avg,5))
    # Vypise data vysek do souboru
    def data_to_file(self):
        file_lines = []
        file_lines.append("Výška hladiny v řezu y = " + str(self.y_pos[0]) + " \n ")
        x_str = "\\textbf{x:} " + str(self.x_pos_f[0])
        h_str = "\\textbf{h:} " + str(round(self.h_list_avg_f[0],3))
        for i in range (1,len(self.h_list_avg_f)):
            x_str += " & " + str(self.x_pos_f[i])
            h_str += " & " + str(round(self.h_list_avg_f[i],3))
        x_str += "\\\\ \\hline \n"
        h_str += "\\\\ \\hline \n"
        head = "\\begin{tabular}{|"
        for i in range(0, len(self.x_pos_f)):
            head += "l|"
        head += "} \n"
        file_lines.append('\\begin{table}[H] \n')
        file_lines.append(head)
        file_lines.append(x_str)
        file_lines.append(h_str)
        file_lines.append('\\end{tabular} \n')
        file_lines.append('\\end{table} \n')
        with open("vysky_tabulka.tex", "a") as f:
            for i in file_lines:
                f.write(i)

### Graf pohledu z boku ###
def plot_sideView(): # <- udelat lepe
    # Konfigurace grafu
    fig = figure(figsize=(10,7))
    ax1 = fig.add_subplot(111)
    xlabel('x [m]', fontsize=15); ylabel('h [m]', fontsize=15)
    title("Profil hladiny, bocni pohled", fontsize=20)
    grid(color='k', linestyle='--', linewidth=0.5)
    # Nacteni dat a plot
    ax1.tick_params(labelsize=12)
    x0idx = np.where(mt_files[0].x_pos == 0)
    y_arr = []
    h = []
    for i in mt_files:
        y_arr.append(i.y_pos[0])
        h.append(i.h_list_avg[x0idx[0][0]]) #np.where vraci komplikovanou strukturu
    # Obrazkovy vystup
    ax1.scatter(y_arr,h,marker="o",label='y = '+str(i.y_pos[0]))
    legend(loc='upper right', fontsize=15);
    fig.savefig("h_bocni_pohled.png")

### Graf pohledu z predu ###
def plot_frontView():
    fig = figure(figsize=(10,7))
    ax1 = fig.add_subplot(111)
    xlabel('x [m]', fontsize=15); ylabel('h [m]', fontsize=15)
    title("Profil hladiny, predni pohled", fontsize=20)
    grid(color='k', linestyle='--', linewidth=0.5)
    ax1.tick_params(labelsize=12)
    for i in mt_files: # <- odstranit _f pr plot celeho MT
        ax1.plot(i.x_pos_f, i.h_list_avg_f,linewidth=2,markersize="8",marker="o",label='y = '+str(i.y_pos[0]))
    legend(loc='upper right',bbox_to_anchor = (1.3, 1.02),fontsize=12);
    tight_layout()
    fig.savefig("h_predni_pohled.png")
    #show()

### Nacte soubory z measureootlu ###
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and '_PointsHeight' in i:
        files.append(i)

### Nacte potreba data z jednotlivych souboru ###
for i in range(0,len(files)):
    x_pos.append(int(re.search(r'\d+', files[i]).group()))
    with open(path + files[i]) as myfile:
        file_to_lines = myfile.readlines()
        # Nacte x-ove souradnice
        l1 = ''.join(file_to_lines[0])
        ## l1_part = l1.split(';')
        ## l1_arr = np.asarray(l1_part[2:], dtype=np.float32)
        l1_arr = np.asarray(l1.split(';')[2:], dtype=np.float32)
        # Nacte y-ove souradnice
        l2 = ''.join(file_to_lines[1])
        l2_arr = np.asarray(l2.split(';')[2:], dtype=np.float32)
        # Nacte y-ove souradnice
        l3 = ''.join(file_to_lines[2])
        l3_arr = np.asarray(l3.split(';')[2:], dtype=np.float32)
        # Vytvori objekt tridy measretool-files #
        mt_files.append(MT_file(files[i], l1_arr, l2_arr, l3_arr))
        # Nacte vysledky mereni #
        for j in range(0, t_steps):
            ll = ''.join(file_to_lines[len(file_to_lines) - 1 - j])
            ll_arr = np.asarray(ll.split(';'), dtype=np.float32)
            h_part = np.delete(ll_arr, [0, 1])
            mt_files[i].append_h(h_part)

### Prumerovani a vyhodnoceni jednotlivych rezu ###
for i in mt_files:
    i.make_avg(); i.apply_offset(); i.filter_zeros();  i.plot_h()

### Vytovireni finalnich vystupu ###
plot_frontView()
plot_sideView()

### Vypis protridenych dat do souboru ve forme LaTeXove tabulky ###
# Vytvori soubor vypisu
if not os.path.exists('vysky_tabulka.tex'):
    os.mknod('vysky_tabulka.tex')
for i in mt_files:
    i.data_to_file()

### Kontrola ###
print("Files lenght: ", len(files), " MT_files list length: ", len(mt_files))
print("Lenght of mt-files len: ", len(mt_files[0].h_list))
mt_files[12].print_h()

