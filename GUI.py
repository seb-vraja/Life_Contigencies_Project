#Francisco Brito
#Sebastian Vraja
# Atuariado Vida I
# Docente: Pedro Corte Real
#--------------------------------------
#--------------------------------------

# Packages:
import tkinter as tk #GUI
from tkinter import ttk
import pandas as pd # We are going to use the pandas package to manipulate the datasets
import numpy as np # Manipulate data, and optimized for numerical errors
import matplotlib.pyplot as plt# to plot the graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# To Display the panda dataframe

# Window
root = tk.Tk()  
root.geometry('600x500') # The standart size of the window of our aplication 
root.title('Term Life Insurance') # Title of te window

# Labels for the User Interface:
label_1=tk.Label(root, text='For the insured Person:')
label_2=tk.Label(root, text='For the Life Actuary:')
label_3=tk.Label(root,text='Select a Table:')
label_4=tk.Label(root,text='Life Insured Type:')
age_l = tk.Label(root, text="Insured Age: ")
term_l = tk.Label(root, text="Term")
tx_l = tk.Label(root, text="Flat Interesst(%): ")
capital_l = tk.Label(root, text="Underwritten Capital: ")
lev_l = tk.Label(root, text="Period to pay Leveled premium: ")
l0_l = tk.Label(root, text="Inicial population size (l_0): ")
empty=tk.Label(root, text='')
euro_l=tk.Label(root, text=' €')
year_1=tk.Label(root, text=' years')
year_2=tk.Label(root, text=' years')
year_3=tk.Label(root, text=' years')
live_l=tk.Label(root, text=' lives')
empty_2=tk.Label(root, text='')
var1=tk.IntVar() # Input variable for the Table choice (GRF95, GRM95, TV95) 
var2=tk.IntVar() # Input variable for the Type of life insured (Aggravated, Standart, Preferred)

#Inputs
x = tk.Spinbox(root,from_=18,to=65,textvariable=tk.IntVar) #Age from 18-65 years
n =tk.Spinbox(root,from_=5,to=25,textvariable=tk.IntVar) #Term 5-25 years
n_lev =tk.Spinbox(root,from_=5,to=25,textvariable=tk.IntVar) # Leveled years 5-25 years
tx= tk.Spinbox(root,from_=1,to=5,textvariable=tk.IntVar) #Flat Interesst
capital = tk.Spinbox(root,from_=0,to=999999999,textvariable=tk.IntVar)#Capital Underwritten
l_0 = tk.Spinbox(root,from_=0,to=99999999999,textvariable=tk.IntVar)# Inicial Size of the Population

#Table choice input
tab1=tk.Radiobutton(root,text='GRM95',variable=var1,value=1)#GRM95
tab2=tk.Radiobutton(root,text='GRF95',variable=var1,value=2)#GRF95
tab3=tk.Radiobutton(root,text='TV95',variable=var1,value=3)#TV95

#Insured type input:
tab4=tk.Radiobutton(root,text='Aggravated',variable=var2,value=1)#Aggravated
tab5=tk.Radiobutton(root,text='Standart',variable=var2,value=2)#Standart
tab6=tk.Radiobutton(root,text='Preferred',variable=var2,value=3)#Preferred


#Functions

#Table Choice:
def Table(var1,var2,x):

    #Which life table the actuary wants to use?
    if var1== 3:
        #Preparing the TV7377 DataFrame
        Table=pd.DataFrame(pd.read_csv("TV7377.csv"))
        Table= Table[['Table__Values__Axis__Y__@t','Table__Values__Axis__Y__#text']]
        Table.rename(columns={'Table__Values__Axis__Y__@t':"Age",'Table__Values__Axis__Y__#text':"qx"},inplace=True)
        
    elif var1 ==1:
        #GRM95 Data preparation:
        Table=pd.DataFrame(pd.read_csv("GRM95.csv"))
        Table= Table[['Table__Values__Axis__Y__@t','Table__Values__Axis__Y__#text']]
        Table.rename(columns={'Table__Values__Axis__Y__@t':"Age",'Table__Values__Axis__Y__#text':"qx"},inplace=True)
       
    elif var1 ==2:
        #GRF95 Data preparation:
        Table=pd.DataFrame(pd.read_csv("GRF95.csv"))
        Table= Table[['Table__Values__Axis__Y__@t','Table__Values__Axis__Y__#text']]
        Table.rename(columns={'Table__Values__Axis__Y__@t':"Age",'Table__Values__Axis__Y__#text':"qx"},inplace=True)
        
    #px calculation:
        
    #Preferred
    if var2==3:
        Table.loc[Table['Age']==x,'qx']=Table.loc[Table['Age']==x,'qx']*0.89 #q[x]=0.89qx
        Table.loc[Table['Age']==x+1,'qx']=Table.loc[Table['Age']==x+1,'qx']*0.99#q[x+1]-1=0.99qx
        Table.loc[Table['Age']==x+2,'qx']=Table.loc[Table['Age']==x+2,'qx']*0.95#q[x-2]+2=0.95qx
        Table["px"]=1-Table["qx"]#px=1-qx
    #Aggravated:
    elif var2==1:
        Table.loc[Table['Age']==x,'qx']=Table.loc[Table['Age']==x,'qx']*1.2 #q[x]=1.2qx
        Table.loc[Table['Age']==x+1,'qx']=Table.loc[Table['Age']==x+1,'qx']*1.1#q[x-1]=1.1qx
        Table.loc[Table['Age']==x+2,'qx']=Table.loc[Table['Age']==x+2,'qx']*1.05#q[x-2]+2=1.05qx
        Table["px"]=1-Table["qx"]#px=1-qx
    #Standart
    elif var2==2:
        Table["px"]=1-Table["qx"]#px=1-qx
   
    return Table # Dataframe of the Table choosen


#npx: (Probability function given aged x, lives n years)
def npx(n,x,Table):
    Table_i=Table.loc[Table['Age']>=x] # The Table starts from age x
    Table_i=Table_i.loc[Table['Age']<=x+n-1] # The multiplication of px ends at age n-1-> SEE the report with the demonstration
    result= Table_i['px'].prod(axis=0)# npx=p_(n-1)*p_(n-2)*...*p_(x+1)*p_x
    return result #npx

#A1x:n| Calculation:
def A(x,n,i,Table):#death benefit of 1 is payable at the end of the year of death, provided this occurs within n years
    values=[]
    for j in range(n):
        v=pow(1+i,-(j+1))
        value=v*npx(j,x,Table)*(1-npx(1,x+j,Table))# SEE REPORT
        values.append(value)
    result=sum(values)
    return result

#Single risk Premium function:
def risksingle(var1,var2,x,n,tx,capital):
    var1=int(var1.get())#.get() means that the code will obtain the values from the inputs, in this case: Table
    var2=int(var2.get())#Type of life
    x=int(x.get())#Age
    n=int(n.get())#terms
    tx=float(tx.get())/100#Flat interesst
    capital=float(capital.get())#capital underwritten
    table=Table(var1,var2,x)# Obtaining the Table to calculate values
    #Risk Single Premium:
    single_risk= capital * A(x,n, tx,table)# using the unitary benefit multiplied by the capital
    return single_risk

#a: x:lev_n-> Annuity used to level the premium
def axn(x,n_lev,i,table):
    values=[]
    for k in range(n_lev):
        v=pow(1+i,-k)
        value=v*npx(k,x,table)# The formula to calculate it´s in the report
        values.append(value)
    result= sum(values)
    return result

#Leveled premium:
def lev_premium(x,n,n_lev,capital,i,table):
    return (capital *A(x,n,i,table))/axn(x,n_lev,i,table)
    
# Net Premium Reserve:
def kVxm(k,x,n,n_lev,i,table):
    if k<=n_lev:
        result= A(x+k, n-k, i,table)-((A(x, n, i,table)/axn(x, n_lev, i,table))*axn(x+k, n_lev-k, i,table) )
    else:
        result= A(x+k, n-k, i,table) # Not needed this conditions, but why not??
    return result
    
# TARGET Data Frame:--->This is the dataframe we are trying to obtain, using the previous functions
def tdf(x,n,l_0,n_lev,tx,capital,var1,var2):
    var1=int(var1.get())
    var2=int(var2.get())
    n_lev=int(n_lev.get())
    x=int(x.get())
    n=int(n.get())
    l_0=int(l_0.get())
    tx=float(tx.get())/100
    capital=float(capital.get())
    table=Table(var1,var2,x)#### Allready explained above
    Table_intern=table.loc[table['Age']>=x] # The Table starts from age x
    Table_intern=Table_intern.loc[table['Age']<=x+n+1] # The Table ends at age x+n, but we need the p_(x+n+1) for intermediate calculations
    Table_intern = Table_intern.reset_index(drop=True)# reseting the index to make programming easy!
    # l calculations:
    Table_intern['lx']=l_0 #defining the first value
    for i in range(1,np.shape(Table_intern)[0]):
        Table_intern['lx'].iloc[i]=float(Table_intern['px'].iloc[i-1]*Table_intern['lx'].iloc[i-1]) # lx=p_(x-1)*l_(x-1)
    #Leveled Premium:´
    levpm=lev_premium(x, n, n_lev, capital, tx,table)
    # Premium column:
    Table_intern['Premium']=levpm * Table_intern['lx']
    Table_intern.loc[Table_intern['Age']>=x+n_lev,'Premium']=0 # Pays during n_lev years!
    # Claims column:
    Table_intern['Claims']=0# Forcing the first claim value to be 0 
    for k in range(1,np.shape(Table_intern)[0]):
        Table_intern['Claims'].iloc[k]=(Table_intern['lx'].iloc[k-1]-Table_intern['lx'].iloc[k])*capital
    # Net Premiums Reserve:   
    Table_intern['Net Premiums Reserve']=0# Forcing the first claim value to be 0 
    for j in range(1,np.shape(Table_intern)[0]):
        Table_intern['Net Premiums Reserve'].iloc[j]=kVxm(j,x,n,n_lev,tx,table)*capital # Net reserves for each individual
    Table_intern['Net Premiums Reserve']=Table_intern['Net Premiums Reserve']*Table_intern['lx']#Times population still alive at j-year
    #Fund:
    Table_intern['Fund']=Table_intern['Premium']+Table_intern['Net Premiums Reserve']# Fund = Premiums + Net Reserve
    
    # returning only what we need:
    result=Table_intern[['Age','lx','Premium','Claims','Fund','Net Premiums Reserve']].round(2).drop(n+1)#removing the last row (intermidate row)
        
    return result #Might have numerical precision issues!!!! -> refer this common problem in the report, however we used numpy and pandas :)
    
#Display dataframe:
def display_df(x,n,l_0,n_lev,tx,capital,var1,var2):
    df=tdf(x,n,l_0,n_lev,tx,capital,var1,var2)
    root1=tk.Tk()
    root1.title("Leveled Premiums")
    root1.geometry('2000x500')
    tree = ttk.Treeview(root1)
    #annuity:
    table=Table(int(var1.get()),int(var2.get()),int(x.get()))
    annuity=axn(int(x.get()),int(n_lev.get()),float(tx.get()),table)# Also this is needed in the Output
    tree["columns"] = list(df.columns)
        # Define columns
    for col in df.columns: 
        tree.column(col, anchor="center")
        tree.heading(col, text=col, anchor="center")
    # Insert data into the Treeview
    for i, row in df.iterrows():
        tree.insert("", i, values=list(row))
    # Pack the Treeview
    tree.pack(expand=True, fill="both")
    # show the Annuity used to level the premium
    label_annuity=tk.Label(root1,text='The Annuity used to level the premiums is '+str(annuity))
    label_annuity.pack()
    # Run the Tkinter event loop
    root1.mainloop()#-----------------> keeps the window running, until closed

# Data Frame plots:
def graph_df(x,n,l_0,n_lev,tx,capital,var1,var2):
    df=tdf(x,n,l_0,n_lev,tx,capital,var1,var2)
    # Create a Tkinter window
    root2 = tk.Tk()
    root2.title("DataFrame Plotting")

    # Create a Figure and a set of subplots
    fig, axes = plt.subplots(3, 1, figsize=(6, 12), sharex=True, gridspec_kw={'hspace': 0.5})
    
    # Plotting the first graph
    df.plot(x='Age', y='Premium', marker='o', linestyle='-', color='b', ax=axes[0])# Age vs Premium Plot
    axes[0].set_title('Premium vs Age')

    # Plotting the second graph
    df.plot(x='Age', y='Claims', marker='o', linestyle='-', color='g', ax=axes[1])#Age vs Claims Plot
    axes[1].set_title('Claims vs Age')

    # Plotting the third graph
    df.plot(x='Age', y='lx', marker='o', linestyle='-', color='r', ax=axes[2])# Age vs Population size PLot
    axes[2].set_title('Population size vs Age')

    # Embed the plots in a Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Run the Tkinter event loop
    root2.mainloop()

# Window for the output of the single risk premium:
def window_risk(var1,var2,x,n,tx,capital):
    s_risk=risksingle(var1,var2,x,n,tx,capital)
    risk=tk.Tk()# new window
    risk.geometry('400x400')# window size
    risk.title('Single Risk Premium')
    risk_label=tk.Label(risk, text='The Single Risk Premium is '+str(round(s_risk,2))+' €')
    risk_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    risk.mainloop()

# The short report function
def last_report(x,n,n_lev,tx,capital,var1,var2):
    var1=int(var1.get())
    var2=int(var2.get())
    n_lev=int(n_lev.get())
    x=int(x.get())
    n=int(n.get())
    tx=float(tx.get())/100
    capital=float(capital.get())
    table=Table(var1,var2,x)
    #Single risk Premium
    single_risk= capital * A(x,n, tx,table)
    #Leveled Premium
    annuity=axn(x,n_lev,tx,table)
    leveled_premium=single_risk/annuity##Calculations... again :( not very computational cost friendly

    report=tk.Tk() # new window for the report
    report.geometry('1200x400')#Size of the window to display the report
    report.title('Term Life Insurance Report')
    #Labels for the report window:
    r_l1=tk.Label(report, text='Bellow follows a comprise short report on the conditions and expected values if you decide to subscribe our life term insurance product.')
    r_l2=tk.Label(report, text='In the case of product subscription please note the following applicable conditions:')
    r_l3=tk.Label(report, text='Term Life Insurance, which the Benefit is payable to the beneficiaries, in the case of death within the stipulated period, and at the end of the year of death, occurring within '+str(n)+' years')
    r_l4=tk.Label(report, text='You were given the option of:')
    r_l5=tk.Label(report, text='Gender: '+str(['Male','Female','--'][var1-1]))
    r_l6=tk.Label(report, text='Age: '+str(x)+ ' years')
    r_l7=tk.Label(report, text='Period to pay leveled premium: '+str(n_lev)+' years')
    r_l8=tk.Label(report, text='Underwritten Capital: '+str(round(capital,2))+' €')
    r_l9=tk.Label(report, text='Flat Interest: '+str(round(tx*100,2))+'%')
    r_l10=tk.Label(report, text='Health Condition: '+str(['Aggravated','Standart','Preferred'][var2-1]))
    r_l10_1=tk.Label(report, text='')
    r_l11=tk.Label(report, text='For those conditions above, the policy Premium will be given by:')
    r_final=tk.Label(report, text='Single Premium: '+str(round(single_risk,2))+' €')
    r_final_lev=tk.Label(report, text='Annual Leveled Premium: '+str(round(leveled_premium,2))+' € per year')
    #The position of the labels or strings, however you may call it:
    r_l1.grid(row=1, column=0)
    r_l2.grid(row=2, column=0)
    r_l3.grid(row=3, column=0)
    r_l4.grid(row=4, column=0)
    r_l5.grid(row=5, column=0)
    r_l6.grid(row=6, column=0)
    r_l7.grid(row=7, column=0)
    r_l8.grid(row=8, column=0)
    r_l9.grid(row=9, column=0)
    r_l10.grid(row=10, column=0)
    r_l10_1.grid(row=11, column=0)
    r_l11.grid(row=12, column=0)
    r_final.grid(row=13, column=0)
    r_final_lev.grid(row=14, column=0)

    report.mainloop()#Running...
    
    
    
    
    


# Outputs Buttons:
RiskSingleButton = tk.Button(root, text="Risk Single Premium",activeforeground='blue',command=lambda:window_risk(var1,var2,x,n,tx,capital))# when the actuary wants the Risk Single Premium
TableButton=tk.Button(root, text="Table with Leveled Premiums",activeforeground='blue',command=lambda:display_df(x,n,l_0,n_lev,tx,capital,var1,var2))# The Table
GraphsButton=tk.Button(root, text="Graphs",activeforeground='blue',command=lambda:graph_df(x,n,l_0,n_lev,tx,capital,var1,var2))# The Graphs
ReportButton = tk.Button(root, text="Summary Report",activeforeground='blue',command=lambda:last_report(x,n,n_lev,tx,capital,var1,var2))# The small report to be presented to he/she to take a decision
###---> the functions are only called when the user calls




# Place label, entry, and button placements ( for the main window):
label_1.grid(row=0,column=1)
age_l.grid(row=1, column=0)
year_1.grid(row=1, column=2)
x.grid(row=1, column=1)
term_l.grid(row=2,column=0)
year_2.grid(row=2, column=2)
n.grid(row=2, column=1)
lev_l.grid(row=3, column=0)
n_lev.grid(row=3, column=1)
year_3.grid(row=3, column=2)
label_2.grid(row=4, column=1)
tx_l.grid(row=5, column=0)
tx.grid(row=5, column=1)
capital_l.grid(row=6, column=0)
capital.grid(row=6, column=1)
euro_l.grid(row=6,column=2)
l0_l.grid(row=7, column=0)
live_l.grid(row=7, column=2)
l_0.grid(row=7, column=1)
label_3.grid(row=8, column=0)
tab1.grid(row=9, column=0)
tab2.grid(row=9, column=1)
tab3.grid(row=9, column=2)
label_4.grid(row=10, column=0)
tab4.grid(row=11, column=0)
tab5.grid(row=11, column=1)
tab6.grid(row=11, column=2)
empty.grid(row=12, column=2)# empty space
RiskSingleButton.grid(row=13, column=0)
TableButton.grid(row=13, column=1)
GraphsButton.grid(row=13, column=2)
empty_2.grid(row=14,column=2)
ReportButton.grid(row=15,column=1)

  

# Main loop
root.mainloop()
