from requests import get
from config import STEAM_API_KEY

class NoSuchSteamIDError(Exception):
	pass

def get_64bit_steam_id(vanityurl):
	"""Retrieves the 64-bit Steam ID for the given vanity url
	eg. http://steamcommunity.com/id/vanityurl
	
	"""
	
	RESOLVE_VANITY_URL = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=%s&vanityurl=%s'
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
		

print get_64bit_steam_id('None')