#!/usr/bin/env python
# coding=utf-8

import dbus

MPRIS_NAME_PREFIX = "org.mpris.MediaPlayer2"
MPRIS_OBJECT_PATH = "/org/mpris/MediaPlayer2"
IROOT = "org.mpris.MediaPlayer2"
IPLAYER = IROOT + ".Player"
ITRACKLIST = IROOT + ".TrackList"
IPLAYLISTS = IROOT + ".PlayLists"
IPROPERTIES = "org.freedesktop.DBus.Properties"


def convert(dbus_obj):
    if isinstance(dbus_obj, dbus.Boolean):
        return bool(dbus_obj)
    if filter(lambda obj_type: isinstance(dbus_obj, obj_type),
              (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
               dbus.UInt16, dbus.UInt32, dbus.UInt64)):
        return int(dbus_obj)
    if isinstance(dbus_obj, dbus.Double):
        return float(dbus_obj)
    if filter(lambda obj_type: isinstance(dbus_obj, obj_type),
             (dbus.ObjectPath, dbus.Signature, dbus.String, dbus.UTF8String)):
        return str(dbus_obj)
    if isinstance(dbus_obj, dbus.Array):
        return map(convert, dbus_obj)


def available_players():
    bus = dbus.SessionBus()
    players = set()
    for name in filter(lambda item: item.startswith(MPRIS_NAME_PREFIX),
                       bus.list_names()):
        owner_name = bus.get_name_owner(name)
        players.add(convert(owner_name))
    return players


print(available_players())
