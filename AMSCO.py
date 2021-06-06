# szyfr zwykłej zamiany ( podstawieniowy lub substytucji )
import random
from time import time as tm
import math
from Kryptografia.ngram import Ngram_score

ngs = Ngram_score('english_quadgrams.txt')

alfabet = ''.join( [ chr(65+i) for i in range(26) ] )


#''.join( random.sample( alfabet, 26 ) )

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += str(ele)
    return str1


def countEl(n, level):
    nieparz = (n % 2 == 1)
    if nieparz:
        n = n - 1
        return 3 * n / 2 + (level + 1) % 2 + 1
    else:
        return 3 * n / 2 + 0


def countElCol(k, dl_key, rows):  # 1 3
    suma = 0
    for i in range(0, rows):
        suma += ((k + 1) % 2) + 1
        k += dl_key
    return suma


def encrypt(txt, key):
    dl_txt = len(txt)
    dl_key = len(key)
    dl_cipher = 0
    rows = 0
    i = 0
    while dl_cipher < dl_txt:
        dl_cipher += int(countEl(dl_key, i))
        rows += 1
        i += 1

    indeksy = [0] * dl_key
    indeks = 0
    for i in range(0, dl_key):
        indeksy[i] = indeks
        indeks += countElCol(int(key[i]) - 1, dl_key, rows)

    indeksy_maks = [0] * dl_key
    indeksy_maks[dl_key - 1] = indeks
    i = dl_key - 1
    while i >= 1:
        indeksy_maks[i - 1] = indeksy[i]
        i -= 1
    block_size = 2
    indeks = 0
    txtc = [0] * (dl_cipher + 1)
    i_row = 0
    i = 0
    j = 0
    while i_row < rows:
        i = 0
        while i < dl_key:
            j = 0
            while j < block_size:
                if (indeks < dl_txt):
                    txtc[indeksy[int(key[i]) - 1]] = txt[indeks]
                    indeksy[int(key[i]) - 1] += 1
                    indeks += 1
                j += 1

            block_size = (block_size % 2) + 1
            i += 1
        i_row += 1

    i = 0
    while (i < dl_key):
        while (indeksy[i] < indeksy_maks[i]):
            txtc[indeksy[i]] = ' '
            indeksy[i] += 1

        i += 1

    txtc[dl_cipher] = '\0'
    txtc = listToString(txtc)
    return txtc

def decrypt(txt, key):
    dl_txt = len(txt) - 1

    dl_key = len(key)
    dl_cipher = 0
    rows = 0
    i = 0
    while dl_cipher < dl_txt:
        dl_cipher += int(countEl(dl_key, i))
        i += 1
        rows += 1

    indeksy = [0] * dl_key
    indeks = 0
    i = 0
    while i < dl_key:
        indeksy[i] = indeks
        indeks += countElCol(int(key[i]) - 1, dl_key, rows)
        i += 1

    indeksy_maks = [0] * dl_key
    indeksy_maks[dl_key - 1] = indeks
    i = dl_key - 1
    while i >= 1:
        indeksy_maks[i - 1] = indeksy[i]
        i -= 1

    txtd = [0] * (dl_txt + 1)
    block_size = 2
    indeks = 0
    i_row = 0
    j = 0
    i = 0
    while i_row < rows:
        i = 0

        while i < dl_key:
            j = 0
            while j < block_size:
                if (indeks < dl_txt):
                    txtd[indeks] = txt[indeksy[int(key[i]) - 1]]
                    indeks += 1
                    indeksy[int(key[i]) - 1] += 1
                j += 1

            block_size = (block_size % 2) + 1
            i += 1
        i_row += 1

    txtd[dl_txt] = '\0'
    txtd = ''.join(txtd)
    return txtd

def generacjaKlucza( dl ):
    return( random.sample( range( dl), dl) )

def swap2( key ):
    key2 = key.copy()
    r1,r2 = sorted( random.sample( range( len(key) ),2 ) )
    key2[r1],key2[r2] = key2[r2],key2[r1]
    return( key2 )

def swap3( key ):
    key2 = key.copy()
    r1,r2,r3 = sorted( random.sample( range( len(key) ),3 ) )
    if random.random() < 0.5:
        key2[r1],key2[r2],key2[r3] = key2[r2],key2[r3],key2[r1]
    else:
        key2[r1],key2[r2],key2[r3] = key2[r3],key2[r1],key2[r2]        
    return( key2 )

def shift( key ):
    r = random.choice( range( len(key) ) )
    return( key[r:] + key[:r] )

def changekey( key ):
    key2 = key
    r = random.random()
    if r < 0.8:
        key3 = swap2( key2 )
    elif r <0.85:
        key3 = shift( key2 )
    else:
        key3 = swap3( key2 )
    return( key3 )

def funkcjaAkceptacji( rozn, t ):
    return( math.exp( -rozn/t ) )

#hillclimbing
def wyzarzenie( kt, dl ):
    T = 100
    dT = -1
    
    oldkey = generacjaKlucza( dl )
    oldvalue = ngs.score( decrypt(kt,oldkey) )

    t0 = tm()
    t = T
    druk = oldvalue
    
    j = 0
    bestkey = oldkey
    bestvalue = oldvalue
    
    while t > 0:
        for i in range( 15*dl ):
            newkey = changekey( oldkey )
            newvalue = ngs.score( decrypt(kt,newkey) )
                    
            if newvalue > oldvalue:
                oldvalue, oldkey = newvalue, newkey

            elif random.random() < funkcjaAkceptacji( abs(oldvalue-newvalue), t ):

                if oldvalue - newvalue > 200:
                   print( oldvalue,' -> ', newvalue )
                if oldvalue > bestvalue:
                    bestvalue, bestkey = oldvalue, oldkey
                #if abs( bestvalue - ngs.score( decrypt(kt, bestkey) ) ) > 0.01:
                #    print('!!!')
                j = 0
                 
                oldvalue, oldkey = newvalue, newkey
                j += 1
            else:
                j += 1


            if j > 50 and oldvalue < bestvalue:
                oldvalue, oldkey = bestvalue, bestkey
                j = 0
                

            if oldvalue > druk:
                print( oldvalue )
                druk = oldvalue
                
        t += dT

    if bestvalue > oldvalue:
        oldvalue, oldkey = bestvalue, bestkey

    print('best: ',[bestvalue,bestkey])
    print('old: ',[oldvalue,oldkey])
    
    return( [oldvalue,oldkey,tm()-t0] )


#hillclimbing

def wspinaczkaZRestartem2( kt, dl ):
    oldkey = generacjaKlucza( dl )
    oldvalue = ngs.score( decrypt(kt,oldkey) )
    wyniki = [ [oldvalue,oldkey] ]
    t0 = tm()
    druk = oldvalue
    while oldvalue / len(kt) < -4.3: #tm()-t0 < 3:
        newkey = changekey( oldkey )
        newvalue = ngs.score( decrypt(kt,newkey) )
        if newvalue > oldvalue:
            oldvalue = newvalue
            oldkey = newkey
        if random.random() < 0.002:
            wyniki.append( [oldvalue,oldkey] )
            wyniki.sort()
            wyniki.reverse()            
            if len(wyniki) >= 10:
                r = random.random()
                if r < 0.9:
                    oldvalue,oldkey = random.choice( wyniki[:5] )                   
                else:
                    oldkey = generacjaKlucza( dl )
                    oldvalue = ngs.score( decrypt(kt,oldkey) )
        if oldvalue > druk:
            print( oldvalue )
            druk = oldvalue
    wyniki.append( [oldvalue,oldkey])
    wyniki.sort()
    wyniki.reverse()

    #for w in wyniki:
    #    print(w)
    
    return( [wyniki[0][0],wyniki[0][1],tm()-t0] )

lenkey = 7
key = generacjaKlucza( lenkey )
tj = 'NOAMOUNTOFEVIDENCEWILLEVERPERSUADEANIDIOTWHENIWASSEVENTEENMYFATHERWASSOSTUPIDIDIDNTWANTTOBESEENWITHHIMINPUBLICWHENIWASTWENTYFOURIWASAMAZEDATHOWMUCHTHEOLDMANHADLEARNEDINJUSTSEVENYEARSWHYWASTEYOURMONEYLOOKINGUPYOURFAMILYTREEJUSTGOINTOPOLITICSANDYOUROPPONENTWILLDOITFORYOUIWASEDUCATEDONCEITTOOKMEYEARSTOGETOVERITNEVERARGUEWITHSTUPIDPEOPLETHEYWILLDRAGYOUDOWNTOTHEIRLEVELANDTHENBEATYOUWITHEXPERIENCEIFYOUDONTREADTHENEWSPAPERYOUREUNINFORMEDIFYOUREADTHENEWSPAPERYOUREMISINFORMEDHOWEASYITISTOMAKEPEOPLEBELIEVEALIEANDHOWHARDITISTOUNDOTHATWORKAGAINGOODDECISIONSCOMEFROMEXPERIENCEEXPERIENCECOMESFROMMAKINGBADDECISIONSIFYOUWANTTOCHANGETHEFUTUREYOUMUSTCHANGEWHATYOUREDOINGINTHEPRESENTDONTWRESTLEWITHPIGSYOUBOTHGETDIRTYANDTHEPIGLIKESITWORRYINGISLIKEPAYINGADEBTYOUDONTOWETHEAVERAGEWOMANWOULDRATHERHAVEBEAUTYTHANBRAINSBECAUSETHEAVERAGEMANCANSEEBETTERTHANHECANTHINKTHEMOREILEARNABOUTPEOPLETHEMOREILIKEMYDOG'
#tj = tj[:100]
print(alfabet)
print(key)

#tj = 'THISISTEST'
print('tekst jawny -',tj,' ', ngs.score(tj))
kt = encrypt( tj, key )
print('kryptotekst = ',kt,' ', ngs.score(kt))
ntj = decrypt( kt, key )
print('odszyfrowany tekst = ',ntj,' ', ngs.score(ntj))
#
wsp = wspinaczkaZRestartem2( kt, lenkey )
print('\n\nWYŻARZENIE:')
wsp = wyzarzenie( kt, lenkey )
print( 'wsp = ',wsp )
print(wsp[1])
dw = decrypt(kt, wsp[1] )
print( dw, ' ', ngs.score(dw) )
print( wsp[2], ' sekund\n\n WSPINACZKA:')

wsp = wspinaczkaZRestartem2( kt, lenkey )
print( 'wsp = ',wsp )
dw = decrypt(kt, wsp[1] )
print( dw, ' ', ngs.score(dw) )
print( wsp[2], ' sekund')

