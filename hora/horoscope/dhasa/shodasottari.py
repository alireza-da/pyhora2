from hora import const, utils
from hora.panchanga import drik
sidereal_year = const.sidereal_year
""" Applicability: Lagna in Sun's hora in Sukla paksha or Lagna in Moon's hora in Krishna paksha """

_dhasa_cycles = 1
seed_star = 8 # Poosam
seed_lord = 0 # Sun
dhasa_adhipathi_list = {0:11,2:12,4:13,6:14,8:15,1:16,3:17,5:18} #  Total 116 years
dhasa_adhipathi_dict = {0:[8,16,24,5],2:[9,17,25,6],4:[10,18,26,7],6:[11,19,27],8:[12,20,1],1:[13,21,2],3:[14,22,3],5:[15,23,4]} 
count_direction = 1 # 1> base star to birth star zodiac -1> base star to birth star antizodiac
def _next_adhipati(lord):
    """Returns next lord after `lord` in the adhipati_list"""
    current = list(dhasa_adhipathi_list.keys()).index(lord)
    next_lord = list(dhasa_adhipathi_list.keys())[((current + 1) % len(dhasa_adhipathi_list))]
    return next_lord
def _get_dhasa_dict():
    dhasa_dict = {k:[] for k in dhasa_adhipathi_list.keys()}
    nak = seed_star-1
    lord = seed_lord
    lord_index = list(dhasa_adhipathi_list.keys()).index(lord)
    for _ in range(27):
        dhasa_dict[lord].append(nak+1)
        nak = (nak+1*count_direction)%27
        lord_index = (lord_index+1) % len(dhasa_adhipathi_list)
        lord = list(dhasa_adhipathi_list.keys())[lord_index]
    return dhasa_dict
#dhasa_adhipathi_dict = _get_dhasa_dict()

def _maha_dhasa(nak):
    return [(_dhasa_lord, dhasa_adhipathi_list[_dhasa_lord]) for _dhasa_lord,_star_list in dhasa_adhipathi_dict.items() if nak in _star_list][0]
def _antardhasa(lord):
    _bhukthis = []
    for _ in range(len(dhasa_adhipathi_list)):
        _bhukthis.append(lord)
        lord = _next_adhipati(lord)
    return _bhukthis
def _dhasa_start(jd,star_position_from_moon=1):
    nak, rem = drik.nakshatra_position(jd,star_position_from_moon=star_position_from_moon)
    #print('nak,rem',nak,rem) # returns 0..26
    one_star = (360 / 27.)        # 27 nakshatras span 360°
    lord,res = _maha_dhasa(nak+1)          # ruler of current nakshatra
    #print(lord,res)
    period = res
    period_elapsed = rem / one_star * period # years
    #print('period_elapsed',period_elapsed,rem/one_star)
    period_elapsed *= sidereal_year        # days
    start_date = jd - period_elapsed      # so many days before current day
    return [lord, start_date,res]
def get_dhasa_bhukthi(dob,tob,place,include_antardhasa=True,star_position_from_moon=1):
    """
        returns a dictionary of all mahadashas and their start dates
        @return {mahadhasa_lord_index, (starting_year,starting_month,starting_day,starting_time_in_hours)}
    """
    jd = utils.julian_day_number(dob, tob)
    timezone = place.timezone
    """ Dhasa start jd changed to UTC based to almost match JHora V2.8.9 """
    jd_utc = jd - place.timezone / 24.
    dhasa_lord, start_jd,_ = _dhasa_start(jd_utc,star_position_from_moon=star_position_from_moon)
    retval = []
    for _ in range(_dhasa_cycles):
        for _ in range(len(dhasa_adhipathi_list)):
            _dhasa_duration = dhasa_adhipathi_list[dhasa_lord]
            if include_antardhasa:
                bhukthis = _antardhasa(dhasa_lord)
                _dhasa_duration /= len(bhukthis)
                for bhukthi_lord in bhukthis:
                    y,m,d,h = utils.jd_to_gregorian(start_jd+timezone/24)
                    dhasa_start = '%04d-%02d-%02d' %(y,m,d) +' '+utils.to_dms(h, as_string=True)
                    retval.append((dhasa_lord,bhukthi_lord,dhasa_start,_dhasa_duration))
                    start_jd += _dhasa_duration * sidereal_year
            else:
                y,m,d,h = utils.jd_to_gregorian(start_jd+timezone/24)
                dhasa_start = '%04d-%02d-%02d' %(y,m,d) +' '+utils.to_dms(h, as_string=True)
                retval.append((dhasa_lord,dhasa_start,_dhasa_duration))
                lord_duration = dhasa_adhipathi_list[dhasa_lord]
                start_jd += lord_duration * sidereal_year
            dhasa_lord = _next_adhipati(dhasa_lord)
    return retval
if __name__ == "__main__":
    utils.set_language('en')
    dob = (1996,12,7)
    tob = (10,34,0)
    place = drik.Place('Chennai',13.0878,80.2785,5.5)
    print('_get_dhasa_dict',_get_dhasa_dict())
    #exit()
    jd = utils.julian_day_number(dob, tob)
    yd = get_dhasa_bhukthi(dob,tob,place,include_antardhasa=False)
    print(yd)
