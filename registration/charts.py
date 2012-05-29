"""
Simple charting with reportlab/PIL
"""

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart


def conversion_chart(data, labels):
    """Create chart that can be drawn as a gif with given data/labels"""

    drawing = Drawing(400, 370)
    bc = VerticalBarChart()

    bc.x = 50
    bc.y = 50

    bc.height = 300
    bc.width = 300

    bc.data = data

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.valueAxis.labelTextFormat = '%2.2f'
    bc.barLabels.fontSize = 15
    bc.barLabelFormat = '%2.2f'
    bc.barLabels.boxAnchor = 's'

    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = 2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = labels

    drawing.add(bc)

    return drawing
