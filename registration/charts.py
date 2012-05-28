"""
Simple charting with reportlab/PIL
"""

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
#from reportlab.graphics.charts.legends import Legend


class ConversionChart(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        apply(Drawing.__init__, (self, width, height) + args, kw)
        self._add(self, VerticalBarChart(), name='bar', validate=None,
                  desc=None)
        self.bar.categoryAxis.categoryNames = ['Conversion Rate']
        self.bar.categoryAxis.labels.fillColor = None
        self.bar.width = 200
        self.bar.height = 150
        self.bar.x = 30
        self.bar.y = 15
        self.bar.barSpacing = 5
        self.bar.groupSpacing = 5
        self.bar.valueAxis.labels.fontName = 'Helvetica'
        self.bar.valueAxis.labels.fontSize = 8
        self.bar.valueAxis.forceZero = 1
        self.bar.valueAxis.rangeRound = 'both'
        self.bar.valueAxis.valueMax = None
        self.bar.categoryAxis.visible = 1
        self.bar.categoryAxis.visibleTicks = 0
        self.bar.barLabels.fontSize = 6
        self.bar.valueAxis.labels.fontSize = 6
        self.bar.strokeWidth = 0.1
        self.bar.bars.strokeWidth = 0.5

        # Add and set up legend
        #self._add(self, Legend(), name='legend', validate=None, desc=None)
        #self.legend.columnMaximum = 10
        #self.legend.fontName = 'Helvetica'
        #self.legend.fontSize = 5.5
        #self.legend.boxAnchor = 'w'
        #self.legend.x = 260
        #self.legend.y = self.height/2
        #self.legend.dx = 8
        #self.legend.dy = 8
        #self.legend.alignment = 'right'
        #self.legend.yGap = 0
        #self.legend.deltay = 11
        #self.legend.dividerLines = 1|2|4
        #self.legend.subCols.rpad = 10
        #self.legend.dxTextSpace = 5
        #self.legend.strokeWidth = 0
        #self.legend.dividerOffsY = 6
