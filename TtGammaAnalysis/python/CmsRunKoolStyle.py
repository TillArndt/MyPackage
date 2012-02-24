__author__ = 'Heiner Tholen'

from ROOT import TStyle, gROOT

class _CmsRunKoolStyle(TStyle):
    """
    Initiates ROOT style according to cms guidelines.
    Also Utility functions for histogram colors are provided.

    >>> import CmsRunKoolStyle as style
    """

    def __init__(self):
        """
        Adjust all ROOT style stuff.
        Places self as new ROOT style.
        """

        super(_CmsRunKoolStyle, self).__init__("KoolStyle", "KoolStyle")
        self.root_style_settings()
        self.cd()
        gROOT.SetStyle("KoolStyle")
        gROOT.ForceStyle()

        # create fall backs
        self.fill_colors    = dict()
        self.pretty_names   = dict()
        self.stacking_order = []


    def set_fill_colors(self, colors):

        if type(colors) != dict:
            raise TypeError, "ERROR argument is not of type dict."
        else:
            self.fill_colors = colors


    def set_stacking_order(self, order):

        if type(order) != list:
            raise TypeError, "ERROR argument is not of type list."
        elif len(self.stacking_order):
            raise Exception, "ERROR stacking_order can only be set once."
        else:
            self.stacking_order = order


    def set_pretty_names(self, names):

        if type(names) != dict:
            raise TypeError, "ERROR argument is not of type dict."
        else:
            self.pretty_names = names


    def get_fill_color(self, sample_kind):
        """
        Returns ROOT color code for 'sample_kind'. For example 'signal' or
        'W + Jets'.
        """

        if self.fill_colors.has_key(sample_kind):
            return self.fill_colors[sample_kind]
        else:
            print "ERROR I don't have a color for '" + sample_kind \
            + "' please add this color in CRController.py"
            return 0


    def get_pretty_name(self, name_in_code):
        """
        Returns pretty name for plots, etc. for the abbreviations used in the
        code.
        """

        if self.pretty_names.has_key(name_in_code):
            return self.pretty_names[name_in_code]
        else:
            return name_in_code


    def get_stacking_order(self):
        """
        Returns copy of MC stacking order.
        """

        return self.stacking_order[:]


    def root_style_settings(self):
        """
        All custom style is specified here and applied to self.
        """

        self.SetFrameBorderMode(0)
        self.SetCanvasBorderMode(0)
        self.SetPadBorderMode(0)
        self.SetPadBorderMode(0)

        #self.SetFrameColor(0)
        self.SetPadColor(0)
        self.SetCanvasColor(0)
        self.SetStatColor(0)
        self.SetFillColor(0)

        self.SetPaperSize(20, 26)
        #self.SetPadTopMargin(0.08)
        #self.SetPadBottomMargin(0.14)
        self.SetPadRightMargin(0.04)
        self.SetPadLeftMargin(0.16)
        #self.SetCanvasDefH(800)
        #self.SetCanvasDefW(800)
        #self.SetPadGridX(1)
        #self.SetPadGridY(1)
        self.SetPadTickX(1)
        self.SetPadTickY(1)

        self.SetTextFont(42) #132
        self.SetTextSize(0.09)
        self.SetLabelFont(42, "xyz")
        self.SetTitleFont(42, "xyz")
        self.SetLabelSize(0.045, "xyz") #0.035
        self.SetTitleSize(0.045, "xyz")
        self.SetTitleOffset(1.6, "y")

        self.SetTitleX(0.16)
        self.SetTitleY(0.93)
        self.SetTitleColor(1)
        self.SetTitleTextColor(1)
        self.SetTitleFillColor(0)
        self.SetTitleBorderSize(1)
        self.SetTitleFontSize(0.04)
        #self.SetPadTopMargin(0.05)
        self.SetPadBottomMargin(0.13)
        #self.SetPadLeftMargin(0.14)
        #self.SetPadRightMargin(0.02)

        # use bold lines and markers
        self.SetMarkerStyle(1)
        self.SetMarkerSize(1)
        self.SetHistLineWidth(0)
        self.SetLineWidth(1)

        self.SetOptTitle(1)
        self.SetOptStat(0)

        # don't know what these are for. Need to ask the Kuess'l-o-Mat.
        self.colors = [1, 2, 3, 4, 6, 7, 8, 9, 11]
        self.markers = [20, 21, 22, 23, 24, 25, 26, 27, 28]
        self.styles = [1, 2, 3, 4, 5, 6, 7, 8, 9]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
else:
    import sys
    sys.modules[__name__] = _CmsRunKoolStyle()