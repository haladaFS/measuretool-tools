import os
import numpy as np
import re
from matplotlib.pyplot import *
from matplotlib.cm import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import decimal

### Konfigurace ###
path = './measuretool/'
t_steps = 3 #Kolik casovych kroku k prumerovani

### Deklarace ###
files = []; x_pos = []; y_pos = []; z_pos = []
mt_files_m = []; mt_files_y = []
mt_files_m_all = []; mt_files_y_all = []

### Objekt jednoho souboru measuretoolu ###
class MT_file:
    # Konstruktor
    def __init__(self, _name, _x_pos, _y_pos, _z_pos):
        self.name = _name
        self.x_pos = _x_pos; self.y_pos = _y_pos; self.z_pos = _z_pos
        # Deklarace potrebnych promennych
        self.v_list = []
        self.v_avg = []
        self.vnz = []
        self.xnz_pos = []; self.ynz_pos = []; self.znz_pos = [];
        self.v_mean = 0
        self.Q = 0
        self.ostr = "========== Řez poloha y = " + str(_y_pos[0]) + " m ========= \n"
    # Pridani vysek z dane casove vrstvy
    def append_v(self,_v_arr):
        self.v_list.append(_v_arr)
    def append_time(self, _part, _time):
        self.part.append(_part)
        self.time.append(_time)
        #print(_part, _time)
        ## print("x")
    def print_v(self):
        print("Name of file: ", self.name)
        print("Length of v_list: ", len(self.v_list))
        print("v_list: ", self.v_list)
        print("v_avg: ", self.v_avg)
        print("-----> Q: ", self.Q)
    def get_nz_pos(self):
        for i in range(0,len(self.v_avg)):
            if self.v_avg[i] != 0:
                self.vnz.append(self.v_avg[i])
                self.xnz_pos.append(self.x_pos[i]);
                self.ynz_pos.append(self.y_pos[i]);
                self.znz_pos.append(self.z_pos[i]);
    def avg_vel(self):
        self.v_avg = self.v_list[0]
        for i in range(1,len(self.v_list)):
            self.v_avg += self.v_list[i]
        self.v_avg /= t_steps
    def analyze_q(self):
        #Streni hodnota rychlosti
        self.v_mean = np.mean(self.vnz)
        #Pocet nulovych a nenulovych bodu, velikost prut. plochy
        zp = len(self.v_avg) - len(self.vnz)
        nzp = len(self.v_avg) - zp
        #Prut. plocha
        xsize = abs(self.x_pos[0] - self.x_pos[-1])
        zsize = abs(self.z_pos[0] - self.z_pos[-1])
        A = xsize*zsize
        flowA = A/len(self.v_avg) * len(self.vnz)
        self.Q = flowA * self.v_mean
        #x print("VEL AVG LEN: ", len(self.v_avg), " VELnz AVG LEN: ", len(self.vnz))
        #x print("MEAN_VEL_VALUE: ", self.v_mean, " flowA: ", flowA)
        #x print("ZP: ", zp, " NZP: ", nzp, " PTOT: ", nzp+zp)
        self.ostr += "Průtok: Q = " + str(round(self.Q,5)) + ' [m^3/s]' + '\n'
        self.ostr += "Průtočná plocha: A_f = " + str(round(flowA,4)) + ' [m^2]' + '\n'
        if np.isnan(self.v_mean) == False:
            self.ostr += "Střední rychlost: v = " + str(round(self.v_mean)) + ' [m^2]' + '\n'
        self.ostr += "--- Výpočtovodá data --- \n"
        self.ostr += "Body: N_tot = " + str(len(self.v_avg)) + ' N_z = ' + str(zp) + ' N_nz = ' + str(nzp) + '\n'
        self.ostr += "Plocha MT: A_mt = " + str(round(A,4)) + ' [m^2]' + '\n'
    def plot_v(self):
        fig = figure(figsize=(8,8))
        ax1 = fig.add_subplot(111, projection='3d')
        p=ax1.scatter(self.xnz_pos, self.znz_pos, self.vnz,c=self.vnz, cmap = 'rainbow' ,marker='o')
        #divider = make_axes_locatable(ax1)
        cbar = fig.colorbar(p,fraction=0.026, pad=0.08)
        cbar.ax.tick_params(labelsize=12)
        ax1.tick_params(labelsize=12)
        ax1.set_xlabel('x [m]', fontsize=15)
        ax1.set_ylabel('z [m]', fontsize=15)
        ax1.set_zlabel('v [m/s]', fontsize=15)
        titstr = 'Rychlostní profil\ny = ' + str(self.y_pos[0]) + ' [m], Q = ' + str(round(self.Q,5)) + ' [m^3/s]'
        pltstr = 'v_profil_y=' + str(self.y_pos[0]) + '_Q=' + str(round(self.Q,5)) + '.png'
        ax1.set_title(titstr, fontsize=20)
        #gcf().set_size_inches((10, 10))
        fig.savefig(pltstr,bbox_inches='tight',pad_inches=0.05)
        ## show()
    def data_to_file(self):
        with open("prutok_data.txt", "a") as f:
            f.write(self.ostr)

class MT_file_all(MT_file):
    def __init__(self, _name, _x_pos, _y_pos, _z_pos):
        super().__init__(_name, _x_pos, _y_pos, _z_pos)
        self.part = []
        self.time = []
        self.v_mean_tlist = []
        self.Q_tlist = []
    def analyze_q_all(self):
        #Prut. plocha
        xsize = abs(self.x_pos[0] - self.x_pos[-1])
        zsize = abs(self.z_pos[0] - self.z_pos[-1])
        A = xsize*zsize
        for i in range(0, len(self.part)):
            vnz_temp = []
            for j in range(0, len(self.v_list[i])):
                if self.v_list[i][j] != 0:
                    vnz_temp.append(self.v_list[i][j])
            flowA = A/len(self.v_list[i]) * len(vnz_temp)
            v_mean_temp = np.mean(vnz_temp)
            self.v_mean_tlist.append(v_mean_temp)
            self.Q_tlist.append(flowA*v_mean_temp)
    def to_fille_all(self):
        namef = "prutok_y" + str(self.y_pos[0]) + ".dat"
        with open(namef, "w") as f:
            for i in range(0, len(self.part)-1):
                f.write(str(self.part[i]))
                f.write(";")
                f.write(str(self.time[i]))
                f.write(";")
                f.write(str(round(self.v_mean_tlist[i],5)))
                f.write(";")
                f.write(str(round(self.Q_tlist[i],5)))
                f.write("\n")
                #print(i)
    def kontrola(self):
        print("asdasdasd", len(self.part))
        print("asdasdasd", len(self.time))
        print("asdasd v ", len(self.v_list))
        #print("asdasd ", self.part)
        #print("asdasd ", self.time)

### Nacte soubory z measureootlu ###
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and '_PointsVelocity' in i:
        files.append(i)

### Nacte potreba data z jednotlivych souboru ###
cm = 0; cy = 0 #pocitadlo
cma = 0; cya = 0 #pocitadlo
real_steps = 0
for i in range(0,len(files)):
    x_pos.append(int(re.search(r'\d+', files[i]).group()))
    with open(path + files[i]) as myfile:
        file_to_lines = myfile.readlines()
        # Nacte x-ove souradnice
        ts = len(file_to_lines)
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
        if 'Vel.m' in files[i]:
            mt_files_m.append(MT_file(files[i], l1_arr, l2_arr, l3_arr))
            # Nacte vysledky mereni #
            for j in range(0, t_steps):
                ll = ''.join(file_to_lines[len(file_to_lines) - 1 - j])
                ll_arr = np.asarray(ll.split(';'), dtype=np.float32)
                v_part = np.delete(ll_arr, [0, 1])
                mt_files_m[cm].append_v(v_part)
            cm += 1
        if 'Vel.y' in files[i]:
            mt_files_y.append(MT_file(files[i], l1_arr, l2_arr, l3_arr))
            # Nacte vysledky mereni #
            for j in range(0, t_steps):
                ll = ''.join(file_to_lines[len(file_to_lines) - 1 - j])
                ll_arr = np.asarray(ll.split(';'), dtype=np.float32)
                v_part = np.delete(ll_arr, [0, 1])
                mt_files_y[cy].append_v(v_part)
            cy += 1

        # Vytvori ojekty tridy dat pro srovani #
        if 'Vel.m' in files[i]:
            mt_files_m_all.append(MT_file_all(files[i], l1_arr, l2_arr, l3_arr))
            # Nacte vysledky mereni #
            for j in range(0, len(file_to_lines)-4):
                ll = ''.join(file_to_lines[len(file_to_lines) - 1 - j])
                ll_arr = np.asarray(ll.split(';'), dtype=np.float32)
                mt_files_m_all[cma].append_time(ll_arr[0], ll_arr[1])
                v_part = np.delete(ll_arr, [0, 1])
                mt_files_m_all[cma].append_v(v_part)
            cma += 1
        if 'Vel.y' in files[i]:
            mt_files_y_all.append(MT_file_all(files[i], l1_arr, l2_arr, l3_arr))
            # Nacte vysledky mereni #
            for j in range(0, len(file_to_lines)-4):
                ll = ''.join(file_to_lines[len(file_to_lines) - 1 - j])
                ll_arr = np.asarray(ll.split(';'), dtype=np.float32)
                mt_files_y_all[cya].append_time(ll_arr[0], ll_arr[1])
                v_part = np.delete(ll_arr, [0, 1])
                mt_files_y_all[cya].append_v(v_part)
            cya += 1

if not os.path.exists('prutok_data.txt'):
    os.mknod('prutok_data.txt')

### Prumerovani a vyhodnoceni jednotlivych rezu ###
for i in mt_files_y:
    # i.shift_y(); # <- NEFUNGUJE
    i.avg_vel();
    i.get_nz_pos();
    i.analyze_q()
    i.print_v();
    i.plot_v();
    i.data_to_file()

for i in mt_files_y_all:
    i.avg_vel();
    i.analyze_q_all()
    i.to_fille_all()
    i.kontrola()

### Vytovireni finalnich vystupu ###


### Kontrola ###
print("Files lenght: ", len(files), " MT_files list length: ", len(mt_files_y))
print("Lenght of mt-files v-list: ", len(mt_files_y[0].v_list))

print("Files lenght: ", len(files), " MT_files_all list length: ", len(mt_files_y_all))
print("Lenght of mt-files v-list: ", len(mt_files_y_all[0].v_list))
print("Lenght of mt-files v-list: ", len(mt_files_y_all[0].part))
