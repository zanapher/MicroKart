import pyglet

# prepare the sprites
sprite_seq = {
    'banana': pyglet.resource.image('sprite_banana.png'),
    'green shell': pyglet.resource.image('sprite_greenshell.png'),
    'red shell': pyglet.resource.image('sprite_redshell.png'),
    'lap 2': pyglet.resource.image('sprite_lap2.png'),
    'lap 3': pyglet.resource.image('sprite_lap3.png'),
    'lap 4': pyglet.resource.image('sprite_lap4.png'),
    'final lap': pyglet.resource.image('sprite_finallap.png'),
    'lakitu flag': pyglet.resource.image('sprite_lakituflag.png'),
    'lakitu fishing': pyglet.resource.image('sprite_lakitufishing.png'),
    'ghost wall': pyglet.resource.image('sprite_ghostwall.png'),
    'item block': pyglet.resource.image('sprite_itemblock.png'),
    'item block empty': pyglet.resource.image('sprite_itemblockempty.png'),
    'item empty': pyglet.resource.image('sprite_itemempty.png'),
    'item coins': pyglet.resource.image('sprite_itemcoins.png'),
    'item banana': pyglet.resource.image('sprite_itembanana.png'),
    'item mushroom': pyglet.resource.image('sprite_itemmushroom.png'),
    'item green shell': pyglet.resource.image('sprite_itemgreenshell.png'),
    'item red shell': pyglet.resource.image('sprite_itemredshell.png'),
    'item feather': pyglet.resource.image('sprite_itemfeather.png'),
    'item lightning': pyglet.resource.image('sprite_itemlightning.png'),
    'item star': pyglet.resource.image('sprite_itemstar.png'),
    'item unknown': pyglet.resource.image('sprite_itemunknown.png'),
    'shadow': pyglet.resource.image('sprite_shadow.png'),
    'none': pyglet.resource.image('sprite_none.png'),
}
for img in sprite_seq.values():
    img.anchor_x = img.width / 2
    img.anchor_y = img.height / 2
sprite_seq['lakitu fishing'].anchor_x = 30
sprite_seq['lakitu fishing'].anchor_y = -24
sprite_seq['shadow'].anchor_y = 9
