
import cmstoolsac3b.rendering as rnd

class SimpleTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS work in progress #sqrt{s}=8 TeV  "

class LumiTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS work in progress  L="\
               + str(round(self.renderers[0].lumi/1000.,1))\
               + " fb^{-1} at #sqrt{s}=8 TeV"
