from lxml import etree

import conf
import loghelp

logger = loghelp.get_logger(__name__)

def get_player_factions(factroot):
    for fact in factroot.iterfind('Faction[@Name]'):
        name = fact.get('Name').lower()
        if not name in {'empire', 'rebel'}:
            continue
        yield fact

def set_unit_cap(fact):
    cap = fact.find('Space_Tactical_Unit_Cap')
    if cap is not None:
        cv = int(cap.text)
        newcv = round(cv * 2)
        cap.text = str(newcv)
        logger.info('Changed unit cap to %d, was %d', newcv, cv)

def execute():
    sourcefile = conf.srcxml / 'factions.xml'
    logger.info('Loading from %s', sourcefile)
    with sourcefile.open() as factfile:
        factdata = etree.parse(factfile)

    for faction in get_player_factions(factdata.getroot()):
        logger.info('Changing faction %s', faction.get('Name'))
        set_unit_cap(faction)


    destfile = conf.outxml / 'factions.xml'
    logger.info('Writing to %s', destfile)
    with destfile.open('wb') as factfile:
        factdata.write(factfile, xml_declaration=True, encoding='utf-8')
