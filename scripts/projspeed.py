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

def set_projectile_speed(proj):
    name = proj.get('Name').lower()

    speedtag = proj.find('Max_Speed')
    if speedtag is not None:
        if 'laser' in name or '_ion_' in name:
            speedtag.text = '120.0'
            logger.info('Set speed to 120.0')
        else:
            speedval = float(speedtag.text)
            newspeed = speedval * 8
            speedtag.text = str(newspeed)
            logger.info('Set speed to %g (from %g)', newspeed, speedval)

def set_laser_type(proj):
    name = proj.get('Name').lower()

    if 'turbolaser' not in name:
        return

    model = etree.SubElement(proj, 'Space_Model_Name')
    if 'green' in name:
        model.text = 'W_LASER_LARGEG.ALO'
    else:
        model.text = 'W_LASER_LARGE.ALO'

    width = proj.find('Projectile_Width')
    if width is not None:
        width.text = '2'

    length = proj.find('Projectile_Length')
    if length is not None:
        length.text = '25'

    texslot = proj.find('Projectile_Texture_Slot')
    if texslot is not None:
        if 'green' in name:
            texslot.text = '3,0'
        else:
            texslot.text = '0,0'

    custrend = proj.find('Projectile_Custom_Render')
    if custrend is not None:
        custrend.text = '1'

    color = proj.find('Projectile_Laser_Color')
    if color is not None:
        proj.remove(color)

ION_COLOR = '104,181,230,255'

def set_ion_appearance(proj):
    name = proj.get('Name').lower()

    if '_ion_' not in name:
        return

    color = proj.find('Projectile_Laser_Color')
    if color is not None:
        color.text = ION_COLOR

    width = proj.find('Projectile_Width')
    if width is not None:
        widval = float(width.text)
        width.text = str(widval * 1.75)

    length = proj.find('Projectile_Length')
    if length is not None:
        lenval = float(length.text)
        length.text = str(lenval *  4)

def set_laser_appearance(proj):
    name = proj.get('Name').lower()

    if 'laser' not in name:
        return

    width = proj.find('Projectile_Width')
    if width is not None:
        widval = float(width.text)
        width.text = str(widval * 1)

    length = proj.find('Projectile_Length')
    if length is not None:
        lenval = float(length.text)
        length.text = str(lenval *  4)

def set_proj_damage(proj):
    damage = proj.find('Projectile_Damage')
    if damage is not None:
        dmg = float(damage.text)
        damage.text = str(dmg * 6)

def execute():
    sourcefile = conf.srcxml / 'projectiles.xml'
    logger.info('Loading from %s', sourcefile)
    with sourcefile.open() as projfile:
        projdata = etree.parse(projfile)

    for proj in get_space_projectiles(projdata.getroot()):
        logger.info('Changing projectile %s', proj.get('Name'))
        set_projectile_speed(proj)
        set_laser_type(proj)
        set_ion_appearance(proj)
        set_laser_appearance(proj)
        set_proj_damage(proj)


    destfile = conf.outxml / 'projectiles.xml'
    logger.info('Writing to %s', destfile)
    with destfile.open('wb') as projfile:
        projdata.write(projfile, xml_declaration=True, encoding='utf-8')
