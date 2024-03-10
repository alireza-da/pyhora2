from hora import const, utils
from hora.horoscope.chart import charts, house,arudhas
from hora.horoscope.dhasa import narayana
""" Mahadhasa lord and period matches with JHora. Antardasa does not match """
sidereal_year = const.sidereal_year

def get_dhasa_antardhasa(dob,tob,place,divisional_chart_factor=1,years=1,months=1,sixty_hours=1,include_antardasa=False):
    jd_at_dob = utils.julian_day_number(dob, tob)
    planet_positions = charts.divisional_chart(jd_at_dob, place, divisional_chart_factor=divisional_chart_factor)
    trikonas = house.trines_of_the_raasi(planet_positions[0][1][0])
    ds1 = house.stronger_rasi_from_planet_positions(planet_positions, trikonas[0], trikonas[1])
    dhasa_seed_sign = house.stronger_rasi_from_planet_positions(planet_positions, ds1, trikonas[2])
    #print(trikonas,dhasa_seed_sign)
    #return narayana._narayana_dhasa_calculation(planet_positions,dhasa_seed_sign,dob,tob,place,years=years,months=months,sixty_hours=sixty_hours,include_antardasa=include_antardasa,varsha_narayana=False)
    #dhasa_lords = dhasa_lord_list[dhasa_seed_sign]
    dhasa_lords = [(dhasa_seed_sign+h)%12 for h in range(12)]
    if dhasa_seed_sign in const.even_signs:
        dhasa_lords = [(dhasa_seed_sign-h+12)%12 for h in range(12)]
    dhasa_info = []
    start_jd = jd_at_dob
    for dhasa_lord in dhasa_lords:
        duration = narayana._dhasa_duration(planet_positions,dhasa_lord)
        bhukthis = [(dhasa_lord+h)%12 for h in range(12)]
        if dhasa_lord in const.even_signs:
            bhukthis = [(dhasa_lord-h+12)%12 for h in range(12)]
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
    from hora.panchanga import drik
    dob = (1996,12,7)
    tob = (10,34,0)
    tobh = (tob[0]+tob[1]/60+tob[2]/3600)/24
    place =drik.Place('Chennai',13.0878,80.2785,5.5)
    include_antardasa = False
    sd = get_dhasa_antardhasa(dob, tob, place,include_antardasa=include_antardasa)
    if include_antardasa:
        for d,b,t,_ in sd:
            print(house.rasi_names_en[d],house.rasi_names_en[b],t)
    else:
        for d,b,t,_ in sd:
            print(house.rasi_names_en[d],b,t)
