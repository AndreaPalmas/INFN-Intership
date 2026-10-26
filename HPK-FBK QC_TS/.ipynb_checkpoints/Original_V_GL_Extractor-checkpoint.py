import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log10, floor

#Funzione per fit lineare 
def linear(x_data, m, q):
    return x_data*m + q

#Funzione per il calcolo dell'intercetta tra due fit lineari
def intercept_lin(m1, q1, m2, q2):
    intercept_x = (q2-q1)/(m1-m2)
    return intercept_x

#Lettura del file .txt con con la misura di capacità
#Filename="MacMarco/Productions/FBK/ETL-LF/CV/W1/NotIrr/CV_TEST_A_2-3.txt"
Filename="data/HPK6_APD52-045_A-TS6[C-V_LGAD - 2026-06-10 11_30_32 AM].txt"
file = open(Filename,"r")
Filelines=file.readlines() #lista delle righe che compongono il file
file.close()

#Tensione di inizio/fine, step in tensione e calcolo del numero di step nella misura
Start_Voltage = float(Filelines[22].split()[1])
Stop_Voltage = float(Filelines[23].split()[1])
Step_Voltage = abs(float(Filelines[25].split()[1]))
Num_biasStep = int((-Stop_Voltage+Start_Voltage)/Step_Voltage)

#Print a terminale di tensione di inizio, fine e step
print("\nBias ramp:")
print("Start = " + str(Start_Voltage) + " V")
print("Stop= " + str(Stop_Voltage) + " V")
print("Step= " + str(Step_Voltage) + " V")

#Filling delle liste con i valori dei parametri misurati
Bias_Voltage = []
Capacitance = []
Capacitance2 = [] #1/C^2
Line_first_data = 135 #Linea nel file di testo da cui iniziano i dati misurati di tensione e capacità
i = 0 #contatore del ciclo while successivo
# questo ciclo while riempie le liste Bias_Voltage/I_pad con i dati misurati
while i <= Num_biasStep:
    Bias_Voltage.append(abs(float(Filelines[Line_first_data + i].split()[0])))
    Capacitance.append(float(Filelines[Line_first_data + i].split()[1]))
    Capacitance2.append(1/(float(Filelines[Line_first_data + i].split()[1]))**2)
    i = i + 1

   ### FIT gain layer region ###
#limiti del fit
low_GL_bias = 10.     #limite basso del fit (in voltaggio); deve essere un multiplo dello step in voltaggio
high_GL_bias = 40.    #limite alto del fit (in voltaggio);deve essere un multiplo dello step in voltaggio
low_bulk_bias = 53.    #limite basso del fit (in voltaggio); deve essere un multiplo dello step in voltaggio
high_bulk_bias = 57.    #limite alto del fit (in voltaggio);deve essere un multiplo dello step in voltaggio
i_low_GL = int(low_GL_bias/Step_Voltage)   #indice del limite basso del fit
i_high_GL = int(high_GL_bias/Step_Voltage)    #indice del limite alto del fit
i_low_bulk = int(low_bulk_bias/Step_Voltage)   #indice del limite basso del fit
i_high_bulk = int(high_bulk_bias/Step_Voltage)    #indice del limite alto del fit
Bias_Voltage_GL = Bias_Voltage[i_low_GL:i_high_GL]
Capacitance2_GL = Capacitance2[i_low_GL:i_high_GL]
Bias_Voltage_bulk = Bias_Voltage[i_low_bulk:i_high_bulk]
Capacitance2_bulk = Capacitance2[i_low_bulk:i_high_bulk]
#fit lineare DI 1/C^2 VS V
parameter_n=2
popt_GL, pcov_GL = curve_fit(linear, Bias_Voltage_GL, Capacitance2_GL, bounds=(0,[7.*10**18, 7.*10**18]))
popt_bulk, pcov_bulk = curve_fit(linear, Bias_Voltage_bulk, Capacitance2_bulk, bounds=([0, -5.*10**24],[7.*10**22, 0]))
#popt = parametri del fit
#pcov = matrice di covarianza

print("\nGain Layer region *** Linear fit")
print("Angular coefficinet: m = " + str(popt_GL[0]))
print("y-intercept: q = " + str(popt_GL[1]))
print("Covariance matrix: " + str(pcov_GL))
#print("sigma_m = " + str(pcov_GL[0][0]))
#print("sigma_q = " + str(pcov_GL[1][1]))


print("\nBulk region *** Linear fit")
print("Angular coefficinet: m = " + str(popt_bulk[0]))
print("y-intercept: q = " + str(popt_bulk[1]))
print("Covariance matrix: " + str(pcov_bulk))
#print("sigma_m = " + str(pcov_bulk[0][0]))
#print("sigma_q = " + str(pcov_bulk[1][1]))

print("\n    ***   Depletion voltage of the gain layer   ***")
print("V_GL = " + str(intercept_lin(popt_GL[0], popt_GL[1], popt_bulk[0], popt_bulk[1])) + " V")


#Plot dei dati
x_fit1=np.linspace(0,60,100)
x_fit2=np.linspace(49,61,100)

plt.plot(Bias_Voltage, Capacitance2, "r^", markersize=3, linewidth=1.0)
plt.plot(x_fit1, linear(x_fit1,popt_GL[0],popt_GL[1]), "k",)
plt.plot(x_fit2, linear(x_fit2,popt_bulk[0],popt_bulk[1]), "k",)
plt.title("Sensor HPK6_APD52-045_A-TS6 " + "\nV_GL = " + str(intercept_lin(popt_GL[0], popt_GL[1], popt_bulk[0], popt_bulk[1])) + " V")
plt.xlabel("Bias [V]")
plt.ylabel("1/C^2 [F^-2]")
plt.legend()
plt.savefig("data/HPK6_APD52-045_A-TS6.png")
#plt.close()
plt.show()


