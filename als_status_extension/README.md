# ALS Status Monitor

This simple Chrome extension shows how to create a "browser action",
which is Google-speak for a toolbar icon that is always present, regardless
of the page you're on.

This browser action displays the status of the ALS (up or down) as well as 
the current beam current.

A background script periodically refreshes a copy of the ALS status data
from the controls.als.lbl.gov, and stores it. Based on the contents, the 
browser action icon is updated.

Separately, a "popup" with code can query the background script for the 
same data, and use it to generate a more complete table showing all the 
basic status parameters.

## Author

Dave Jacobowitz
dgj@lbl.gov

## Version

0.0.1

## Date

September, 2016
