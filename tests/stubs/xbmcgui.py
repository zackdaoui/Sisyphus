SCRIPT = {"select": [], "yesno": [True]}
CALLS = []


class ListItem(object):
    def __init__(self, label="", label2=""):
        self.label, self.label2, self.art = label, label2, {}

    def setArt(self, art):
        self.art = art


class Dialog(object):
    def select(self, heading, items, autoclose=0, preselect=-1, useDetails=False):
        CALLS.append(("select", [i.label for i in items]))
        return SCRIPT["select"].pop(0)

    def yesno(self, heading, message, nolabel="", yeslabel="", **kw):
        CALLS.append(("yesno", message))
        return SCRIPT["yesno"].pop(0)

    def ok(self, heading, message):
        CALLS.append(("ok", message))

    def textviewer(self, heading, text):
        CALLS.append(("textviewer", text))


class DialogProgress(object):
    def create(self, heading, message=""):
        CALLS.append(("progress.create", message))

    def update(self, percent, message=""):
        CALLS.append(("progress.update", message))

    def close(self):
        CALLS.append(("progress.close", ""))
