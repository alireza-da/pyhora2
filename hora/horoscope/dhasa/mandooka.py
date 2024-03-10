from hora import const, utils
from hora.panchanga import drik
from hora.horoscope.chart import charts, house
""" Not fully implemented """
sidereal_year = const.sidereal_year
dhasa_order = {0:([0,3,6,9, 2,5,8,11, 1,4,7,10],[0,9,6,3, 2,11,8,5, 1,10,7,4]),
               3:([3,6,9,0, 2,5,8,11, 1,4,7,10],[3,0,9,6, 2,11,8,5, 1,10,7,4]),
               6:([6,9,0,3, 2,5,8,11, 1,4,7,10],[6,3,0,9, 2,11,8,5, 1,10,7,4]),
               9:([9,0,3,6, 2,5,8,11, 1,4,7,10],[9,6,3,0, 2,11,8,5, 1,10,7,4]),
               2:([2,5,8,11, 1,4,7,10, 0,3,6,9],[2,11,8,5, 1,10,7,4,0,9,6,3]),
               5:([5,8,11,2, 1,4,7,10,0,3,6,9],  [5,2,11,8, 1,10,7,4,0,9,6,3]),
               8:([8,11,2,5, 1,4,7,10,0,3,6,9 ],[8,5,2,11, 1,10,7,4,0,9,6,3]),
               11:([11,2,5,8, 1,4,7,10, 0,3,6,9],[11,8,5,2, 1,10,7,4,0,9,6,3]),
               1:([1,4,7,10, 0,3,6,9, 2,5,8,11],[1,10,7,4, 0,9,6,3, 2,11,8,5]),
               4:([4,7,10,1, 0,3,6,9, 2,5,8,11],[4,1,10,7, 0,9,6,3, 2,11,8,5]),
               7:([7,10,1,4, 0,3,6,9, 2,5,8,11],[7,4,1,10, 0,9,6,3, 2,11,8,5]),
               10:([10,1,4,7, 0,3,6,9, 2,5,8,11],[10,7,4,1, 0,9,6,3, 2,11,8,5])
               }
               
def _dhasa_duration_kn_rao(planet_positions,sign):
    p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    h_to_p = utils.get_house_to_planet_dict_from_planet_to_house_dict(p_to_h)
    lord_of_sign = house.house_owner_from_planet_positions(planet_positions, sign)
    house_of_lord = p_to_h[lord_of_sign]
    #print('dhasa_lord',sign,'lord_of_sign',lord_of_sign,'house_of_lord',house_of_lord,'strength',const.house_strengths_of_planets[lord_of_sign][house_of_lord])
    dhasa_period = 0
    #print('start woth dhasa years 0 - sign lord of sign house of lord dhasa years',sign,lord_of_sign,house_of_lord,dhasa_period)
    """ The length of a dasa is determined by the position of the lord of dasa rasi with respect to dasa rasi."""
    if sign in const.even_footed_signs: # count back from sign to house_of_lord
        dhasa_period = (sign-house_of_lord+1)%12
            #print('house_of_lord',house_of_lord,'> sign',sign,'dhasa_period',dhasa_period)
    else:
        dhasa_period = (house_of_lord-sign+1)%12
    if dhasa_period <=0 or const.house_strengths_of_planets[lord_of_sign][house_of_lord] == const._OWNER_RULER:# or \
            #house_of_lord==(sign+11)%12:
        dhasa_period = 12
    if house_of_lord==(sign+6)%12:
        dhasa_period = 10
    return dhasa_period
def _dhasa_duration(lord):
    if lord in const.movable_signs:
        return 7
    elif lord in const.fixed_signs:
        return 8
    else:
        return 9
def get_dhasa_antardhasa(dob,tob,place,divisional_chart_factor=1,years=1,months=1,sixty_hours=1,include_antardasa=True):
    method = 2
    jd_at_dob = utils.julian_day_number(dob, tob)
    planet_positions = charts.divisional_chart(jd_at_dob, place, ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE, 
                                               divisional_chart_factor=divisional_chart_factor, years=years, 
                                               months=months, sixty_hours=sixty_hours)
    asc_house = planet_positions[0][1][0] ; seventh_house = (asc_house+6)%12
    dhasa_seed = asc_house
    if method == 1 and asc_house in const.even_signs: # Sanjay Rath Method
        dhasa_seed = 8
        if asc_house in const.fixed_signs:
            dhasa_seed = 6
        elif asc_house in const.dual_signs:
            dhasa_seed = 7
    else:
        dhasa_seed = house.stronger_rasi_from_planet_positions(planet_positions, asc_house, seventh_house)
    dir = 0
    if dhasa_seed in const.even_signs:
        dir = 1
    dhasa_lords = dhasa_order[dhasa_seed][dir]
    #print('dhasa_seed',dhasa_seed,'dhasa_lords',dhasa_lords)
    dhasa_info = []
    start_jd = jd_at_dob
    for dhasa_lord in dhasa_lords:
        dhasa_index = dhasa_lords.index(dhasa_lord)
        duration = _dhasa_duration_kn_rao(planet_positions,dhasa_lord) # 
        if method == 1:
            duration = _dhasa_duration(dhasa_lord)
        #print(house.rasi_names_en[dhasa_lord],duration,'years')
        bhukthis =  [dhasa_lords[(dhasa_index+h)%12] for h in range(12)]
        if include_antardasa:
            dd = duration/12
            for bhukthi_lord in bhukthis:
                y,m,d,h = utils.jd_to_gregorian(start_jd)
                dhasa_start = '%04d-%02d-%02d' %(y,m,d) +' '+utils.to_dms(h, as_string=True)
                dhasa_info.append((dhasa_lord,bhukthi_lord,dhasa_start,dd))
                start_jd += dd * sidereal_year
        else:
            y,m,d,h = utils.jd_to_gregorian(start_jd)
            dhasa_start = '%04d-%02d-%02d' %(y,m,d) +' '+utils.to_dms(h, as_string=True)
            dhasa_info.append((dhasa_lord,bhukthis,dhasa_start,duration))
            start_jd += duration * sidereal_year
    return dhasa_info
if __name__ == "__main__":
    utils.set_language('en')
    dob = (1996,12,7)
    #dob = (1964,11,16)
    #dob = (1917,11,19) #Indira Gandth
    tob = (10,34,0)
    #tob = (4,30,0)
    #tob = (23,11,0) #Indira Gandth
    place = drik.Place('Chennai',13.0878,80.2785,5.5)
    #place = drik.Place('karamadai',11.2428,76.9587,5.5)
    #place = drik.Place('',25+27/60,81+51/60,5.5) #Indira Gandth
    include_antardasa = True
    sd = get_dhasa_antardhasa(dob, tob, place,include_antardasa=include_antardasa)
    if include_antardasa:
        for d,b,t,_ in sd:
            print(house.rasi_names_en[d],house.rasi_names_en[b],t)
    else:
        for d,b,t,_ in sd:
            print(house.rasi_names_en[d],b,t)
