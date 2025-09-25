import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import math
import scipy 

X=[0,5,10,15,15,15,15,20,7.5,10,10,20,0]
Yavant=[61,61,61,61,84,84,61,61,84,61,81.5,61,61]
Yapres=[67,76,86,95,117,117,95,105,101,85,105,103,65]


st.set_page_config(layout="wide")
st.title("Statistiques du poids de la barre")

def reglin(X,Y,ax=None,show_reglin="non"):
    X=np.array(X)
    Y=np.array(Y)
    n=len(X)

    J=np.zeros((n,2))
    J[:,1]=X
    J[:,0]=1
    Jt=np.transpose(J)
    Beta=np.linalg.solve(Jt@J,Jt@Y)
    a,b=Beta[1],Beta[0]

    SCT=np.sum((Y-np.mean(Y))**2)
    SCR=np.sum((np.mean(Y)-J@Beta)**2)
    SCE=np.sum((Y-J@Beta)**2)
    Sigmac=SCE/(n-2)
    gam=np.linalg.inv(Jt@J)

    a_utile=scipy.stats.t.pdf(-abs(a/math.sqrt(Sigmac*gam[1,1])),df=n-2)
    b_utile=scipy.stats.t.pdf(-abs(b/math.sqrt(Sigmac*gam[0,0])),df=n-2)

    if show_reglin=="oui":
        if ax is None:
            plt.plot(X,a*X+b,label="y={:.2f}x+{:.2f}".format(a,b))
            plt.legend()
            plt.show()
        else:
            ax.plot(X,a*X+b,label="y={:.2f}x+{:.2f}".format(a,b))
            ax.text(0.85, 0.86, "R²={:.2f}".format(SCR/SCT), transform=ax.transAxes)
            ax.legend()
    return a,b,a_utile,b_utile

st.write("Le poids de la barre a été mesuré en se pesant au départ, puis en se pesant avec la barre. En modifiant la charge de la barre a chaque fois")
st.write("Aucune balance n'a été bléssée durant ces expériences (Promis)")
## -------------------- BARRE NORMALE
X=np.array(X)
Yavant=np.array(Yavant)
Yapres=np.array(Yapres)



poids_barre=Yapres-Yavant-2*X


datas=[Yavant,Yapres,X]


poulie=st.expander("Statistiques du poids de la barre avec poulie")
poulie.markdown("## Moyenne du poids de la barre: "+str(round(np.mean(poids_barre),2))+" kg")



VarY=poids_barre
sboxX=poulie.selectbox("le poids de la barre en fonction de ",("le poid avant de porter la barre","le poids après avoir porté la barre","le poids rajouté de chaque coté de la barre (a multiplier par 2 pour avoir le poids total rajouté)"),index=2)
VarX=datas[["le poid avant de porter la barre","le poids après avoir porté la barre","le poids rajouté de chaque coté de la barre (a multiplier par 2 pour avoir le poids total rajouté)"].index(sboxX)]
pcol=poulie.columns(2)
show_reglin=pcol[1].radio("Afficher la regression linéaire ?",("oui","non"),index=1)
#plot varX and VarY
fig, ax = plt.subplots()
ax.plot(VarX, VarY, 'ro')

a,b,a_utile,b_utile=reglin(X=VarX,Y=VarY,ax=ax,show_reglin=show_reglin)
pcol[1].write("Lorsqu'une probabilité est superieure a 5 %, on considère que c'est non négligeable")
pcol[1].write("Probabilité que le poids de la barre change selon "+sboxX+": **"+str(round(a_utile,4)*100)+"** %")
pcol[1].write("Probabilité que le poids de la barre soit négligeable : **"+str(round(b_utile,4)*100)+"** %")
pcol[0].pyplot(fig,width=800)





## -------------------- BARRE LOURDE 

X_lourd=[10,0,15]
Y_lourd_avant=[61,60.9,61]
Y_lourd_apres=[97,76,106]

X_lourd=np.array(X_lourd)
Y_lourd_avant=np.array(Y_lourd_avant)
Y_lourd_apres=np.array(Y_lourd_apres)

poids_barre_lourd=Y_lourd_apres-Y_lourd_avant-2*X_lourd

datas=[Y_lourd_avant,Y_lourd_apres,X_lourd]


poulie=st.expander("Statistiques du poids de la barre sans poulie")
poulie.markdown("## Moyenne du poids de la barre: "+str(round(np.mean(poids_barre_lourd),2))+" kg")



VarY=poids_barre_lourd
sboxX=poulie.selectbox("le poids de la barre en fonction de ",("le poid avant de porter la barre","le poids après avoir porté la barre","le poids rajouté de chaque coté de la barre (a multiplier par 2 pour avoir le poids total rajouté)"),index=2,key="lourd")
VarX=datas[["le poid avant de porter la barre","le poids après avoir porté la barre","le poids rajouté de chaque coté de la barre (a multiplier par 2 pour avoir le poids total rajouté)"].index(sboxX)]
pcol=poulie.columns(2)
show_reglin=pcol[1].radio("Afficher la regression linéaire ?",("oui","non"),index=1,key="lourdradio")
#plot varX and VarY
fig, ax = plt.subplots()
ax.plot(VarX, VarY, 'ro')

a,b,a_utile,b_utile=reglin(X=VarX,Y=VarY,ax=ax,show_reglin=show_reglin)
pcol[1].write("Lorsqu'une probabilité est superieure a 5 %, on considère que c'est non négligeable")
pcol[1].write("Probabilité que le poids de la barre change selon "+sboxX+": **"+str(round(a_utile*100,4))+"** %")
pcol[1].write("Probabilité que le poids de la barre soit négligeable : **"+str(round(b_utile*100,4))+"** %")
pcol[0].pyplot(fig,width=800)


