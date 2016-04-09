sectors = [
    dict(name="Arctic Ocean"),
    dict(name="North America"),
    dict(name="Central America"),
    dict(name="Carribean"),
    dict(name="South America"),
    dict(name="Europe"),
    dict(name="Middle East"),
    dict(name="Central Asia"),
    dict(name="East Asia"),
    dict(name="South Asia"),
    dict(name="Africa"),
    dict(name="Australasia & Oceana"),
    dict(name="North & West Asia"),
    dict(name="Arctic"),
    dict(name="Antarctic"),
    dict(name="Antarctic Ocean"),
    dict(name="Atlantic Ocean"),
    dict(name="Pacific Ocean"),
    dict(name="Indian Ocean"),
    dict(name="Atmosphere"),
    dict(name="Orbit")]

planet = dict(
    name="Earth",
    sectors=sectors)

planets = [planet]

star_system = dict(planets=planets)

star_systems = [star_system]

galaxy = dict(star_systems=star_systems)

universe = dict(galaxy=galaxy)

# END OF FILE #
