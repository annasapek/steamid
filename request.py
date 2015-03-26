from requests import get
from config import STEAM_API_KEY
from string import find
from string import digits

BASE = long(76561197960265728)
PREFIX = 'U:1:'
STEAM_COMMUNITY = 'http://steamcommunity.com/id/'

class NoSuchSteamIDError(Exception):
	pass

def get_64bit_steam_id(vanityurl):
	""" Retrieves the 64-bit Steam ID for the given vanity url
		eg. http://steamcommunity.com/id/vanityurl -> xxxxxxxxxxxxxxxxx
	
	"""	
	
	if vanityurl.startswith(STEAM_COMMUNITY):
		vanityurl = vanityurl[len(STEAM_COMMUNITY):]
	
	RESOLVE_VANITY_URL = \
		'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=%s&vanityurl=%s'
	if vanityurl == None:
		raise ValueError('Must provide vanityurl')
		exit(1)
	else:
		result = get(RESOLVE_VANITY_URL % (STEAM_API_KEY, vanityurl))
		if result.status_code == 403:
			raise ValueError('Invalid Steam API key: %s' % STEAM_API_KEY)
		else:
			result.raise_for_status()
			data = result.json()
			if data['response']['success'] == 1:
				return data['response']['steamid']
			else:
				raise NoSuchSteamIDError('Could not resolve vanity url: %s' % vanityurl)
				exit(1)

def get_32bit_steam_id(vanityurl):
	""" Retrieves the 32-bit Steam ID for the given vanity url
		eg. http://steamcommunity.com/id/vanityurl -> U:1:XXXXXXXX
	
	"""
	
	steam_id = long(get_64bit_steam_id(vanityurl))
	return 'U:1:%s' % (steam_id - BASE)

def convert_32bit_to_64bit(steamid):
	""" Given a valid 32-bit Steam ID, in the form U:1:XXXXXX or XXXXXX, returns the 
		equivalent 64-bit Steam ID in the form xxxxxxxxxxxxxxxxx
	"""
	
	u_index = find(str(steamid), PREFIX)
	if u_index != -1:
		steamid = steamid[u_index + len(PREFIX):]
	validate_id_number(steamid)
	return str(long(steamid) + BASE)

def convert_64bit_to_32bit(steamid):
	""" Given a valid 64-bit Steam ID, in the form xxxxxxxxxxxxxxxxx, returns the 
		equivalent 32-bit Steam ID in the form U:1:XXXXXX
	"""
	
	validate_id_number(steamid)
	return 'U:1:%s' % (long(steamid) - BASE)

def validate_id_number(value):
	""" Given an id number, returns true if it only contains digits
	"""
	
	for char in str(value):
		if char not in digits:
			raise ValueError('%s is not a valid number' % value)
