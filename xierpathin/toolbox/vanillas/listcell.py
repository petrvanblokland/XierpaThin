# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Font Bureau
#
#     F B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     listcell.py
#
from AppKit import NSTextFieldCell, NSSmallControlSize, NSFont, NSLeftTextAlignment, NSRightTextAlignment, NSCenterTextAlignment

def hideColumn(name, listView, hide=True):
    u"""
    Bit of code to hide the column, because this is not in Vanilla. Name is the identifier of the column in the list.
    """
    tableView = listView.getNSTableView()
    index = tableView.columnWithIdentifier_(name)
    column = tableView.tableColumns()[index]
    column.setHidden_(hide)

def SmallTextListCell(editable=False):
    cell = NSTextFieldCell.alloc().init()
    size = NSSmallControlSize # NSMiniControlSize
    cell.setControlSize_(size)
    font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    cell.setFont_(font)
    cell.setEditable_(editable)
    return cell

def SmallLeftAlignTextListCell(editable=False):
    u"""
    Alternate options: NSLeftTextAlignment, NSRightTextAlignment,NSCenterTextAlignment, NSJustifiedTextAlignment, or
    NSNaturalTextAlignment.
    """
    cell = SmallTextListCell(editable=editable)
    cell.setAlignment_(NSLeftTextAlignment)
    return cell

def SmallRightAlignTextListCell(editable=False):
    cell = SmallTextListCell(editable=editable)
    cell.setAlignment_(NSRightTextAlignment)
    return cell

def SmallCenterAlignTextListCell(editable=False):
    cell = SmallTextListCell(editable=editable)
    cell.setAlignment_(NSCenterTextAlignment)
    return cell
