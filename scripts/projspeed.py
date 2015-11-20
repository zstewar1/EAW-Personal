from lxml import etree

import conf
import loghelp

logger = loghelp.get_logger(__name__)

def get_space_projectiles(projroot):
    for proj in projroot.iterfind('Projectile[@Name]'):
        name = proj.get('Name').lower()
        if not name.startswith('proj_ship'):
            continue

        yield proj

def set_projectile_speeds(projroot):
    logger.info('Setting projectile speeds')

    for proj in get_space_projectiles(projroot):
        logger.info('Changing projectile %s', proj.get('Name'))

        name = proj.get('Name').lower()

        speedtag = proj.find('Max_Speed')
        if speedtag is not None:
            speedval = float(speedtag.text)
            newspeed = speedval * 2.5
            logger.info('Old speed %g, new speed %g', speedval, newspeed)
            speedtag.text = str(newspeed)

def execute():
    sourcefile = conf.srcxml / 'projectiles.xml'
    logger.info('Loading from %s', sourcefile)
    with sourcefile.open() as projfile:
        projdata = etree.parse(projfile)

    set_projectile_speeds(projdata.getroot())

    destfile = conf.outxml / 'projectiles.xml'
    logger.info('Writing to %s', destfile)
    with destfile.open('wb') as projfile:
        projdata.write(projfile)
