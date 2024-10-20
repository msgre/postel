CMD_NEXT_EFFECT = '1'
CMD_END_EFFECT = '2'
CMD_SET_EFFECT = '3'
CMD_CONFIGURATION = '4'



# priklady

# CMD_NEXT_EFFECT = '1'
# 1,,1234567


# CMD_END_EFFECT = '2'
# 2,,1234567


# CMD_SET_EFFECT = '3'
# spusteni vody, bez prechodu:
# 3,1:0,1234567
# spusteni vody, s prechodem:
# 3,1:1,1234567


# CMD_CONFIGURATION = '4'


"""
lepsi asi bude delat dotazy jen ve tme
- ono to asi jde videt, mirne se to seka pri ohni

tj. nova strategie
- na zacatku budou v nejakem spacim stavu
- jakmile se chytnou wifiny, roznou treba jednu zelenou ledku
    - a budou cekat
- kdyby se neco posralo, tak roznou cervenou
    - a zkusi to znovu (pokud se to zase posere, rozne druhou cerveneou)
    - atd


cekani na command
- set effect
    - cislo efektu 0-3
    - parametry, vcetne doby, po jakou ma efekt fungovat
- jakmile by se cely efekt prehral, tak se udela fadeout a zas skonci v cerne
  ve ktere se bude pravidelne dotazovat na dalsi efekt


- debug rezim
    - to same jako set efekt
    - ale cekoval by hodne pravidelne stav na serveru, treba %40

!!!!!
toto je crucial

cmd, parameters, ts = r.content.decode().split('\n')
"""
