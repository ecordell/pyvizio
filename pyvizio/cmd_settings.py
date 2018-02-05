from .protocol import get_json_obj, ProtoConstants, CommandBase, CNames


class SettingsItem(object):
    def __init__(self, json_obj):
        self.id = int(get_json_obj(json_obj, ProtoConstants.Item.HASHVAL))
        self.c_name = get_json_obj(json_obj, ProtoConstants.Item.CNAME)
        self.type = get_json_obj(json_obj, ProtoConstants.Item.TYPE)
        self.name = get_json_obj(json_obj, ProtoConstants.Item.NAME)
        self.value = get_json_obj(json_obj, ProtoConstants.Item.VALUE)
        self.options = []
        options = get_json_obj(json_obj, ProtoConstants.Item.ELEMENTS)
        if options is not None:
            for opt in options:
                self.options.append(opt)


class SettingsCommandBase(CommandBase):
    BASE_URL = "/menu_native/dynamic/tv_settings"

    def get_url(self):
        return self.BASE_URL + self._url

    @staticmethod
    def _get_items(json_obj):
        items = get_json_obj(json_obj, ProtoConstants.RESPONSE_ITEMS)
        if items is None:
            return []

        results = []
        for itm in items:
            item = SettingsItem(itm)
            results.append(item)

        return results


class GetSettingsCommandBase(SettingsCommandBase):
    @property
    def _method(self):
        return "GET"


class GetAudioSettingsCommand(GetSettingsCommandBase):
    @property
    def _url(self):
        return "/audio"

    def process_response(self, json_obj):
        return self._get_items(json_obj)


class GetCurrentAudioCommand(GetAudioSettingsCommand):
    def process_response(self, json_obj):
        items = super().process_response(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Audio.VOLUME:
                return int(itm.value)

        return 0
      
class GetPictureSettingsCommand(GetSettingsCommandBase):
    @property
    def _url(self):
        return "/picture/picture_mode/"


    def process_response(self, json_obj):
        return self._get_items(json_obj)


class GetCurrentPictureModeCommand(GetPictureSettingsCommand):
    def process_response(self, json_obj):
        items = super().process_response(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Picture.MODE:
                return itm

        return 0
    

class GetPictureModesCommand(GetPictureSettingsCommand):
    def process_response(self, json_obj):
        items = super().process_response(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Picture.MODE:
                return itm.options

        return 0


class SetCurrentPictureMode(CommandBase):
    @property
    def _url(self):
        return "/menu_native/dynamic/tv_settings/picture/picture_mode"

    def __init__(self, id_, name):
        self.VALUE = str(name)
        # noinspection SpellCheckingInspection
        self.HASHVAL = int(id_)
        self.REQUEST = ProtoConstants.ACTION_MODIFY

    def process_response(self, json_obj):
        return True


class GetTimerSettingsCommand(GetSettingsCommandBase):
    @property
    def _url(self):
        return "/timers"

    def process_response(self, json_obj):
        return self._get_items(json_obj)


class GetCurrentTimerCommand(GetTimerSettingsCommand):
    def process_response(self, json_obj):
        items = super().process_response(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Timers.SLEEP:
                return itm

        return 0


class GetTimerOptionsCommand(GetTimerSettingsCommand):
    def process_response(self, json_obj):
        items = super().process_response(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Timers.SLEEP:
                return itm.options

        return 0


class SetCurrentTimer(CommandBase):
    @property
    def _url(self):
        return "/menu_native/dynamic/tv_settings/timers/sleep_timer"

    def __init__(self, id_, name):
        self.VALUE = str(name)
        # noinspection SpellCheckingInspection
        self.HASHVAL = int(id_)
        self.REQUEST = ProtoConstants.ACTION_MODIFY

    def process_response(self, json_obj):
        return True