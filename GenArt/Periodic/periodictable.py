import sys
def main():
    while True:
        # show periodic table and get user input
        print('''
        H                                                                   He  
        Li  Be                                          B   C   N   O   F   Ne
        Na  Mg                                          Al  Si  P   S   Cl  Ar
        K   Ca  Sc  Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
        Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe
        Cs  Ba  La  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn
        Fr  Ra  Ac  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og
                
                Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu
                Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr
                ''')
        print('Enter atomic symbol or number to examine, or QUIT to quit.')
        response = input('> ').upper()
        if response in ['QUIT', 'quit', 'Quit', 'q', 'Q', 'exit', 'Exit', 'EXIT']:
            print('Goodbye!')
            sys.exit()



if '__main__' in __name__:
    print('\nThe Periodic Table of Elements')
    print('Written by Sean C. Lewis')
    print('-------------------------')
    main()
