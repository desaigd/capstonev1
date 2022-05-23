

Capstone

Distinctiveness and Complexity:

Trending of Heath Parameters
Design a website that accepts data (parameters) from a medical report of the user and create following functionality:

1. User can register or login with valid credentials. Signed users can input heath parameters.
2.  Display table of all parameters ordered by dates (History). User can input one or more parameters.
3. Create Trending Line Charts to visualise the progress of particular parameter over time for monitoring purpose. Line Charts to show values of each parameter on particular date.
4. User should be able to view normal ranges of parameters in respective charts to visualise if parameter values are in normal range or outside normal range.
5. User can delete any or all records. Update of charts after change of record.

Specification:
	User should be able to register and login/logout from application.
	User should be able to return to Home page by clicking navbar link.
	Users who are signed in should be able to input health parameters from a medical report and submit the record. One or more parameters can be recorded. Not necessary to input all parameters displayed on web page.
	Users who are signed in should be able to view historical records (data) by click of History button. Records should be ordered by most recent first.
	Database should be able to store data in SQLite.  
	Chart should be generated on clicking “Get Trends” button. Charts of all recorded parameters should be generated. Blank chart for the parameter where no value is recorded. Data value to be shown for each data set.
	On each chart, normal value range of that health parameter should be displayed. Range to be filled with colour to visualise if data value is in normal range or not.
	Webpage to display messages for success if record saved successfully. Error message if at least one data is not submitted.
	Display should be mobile responsive.



Complexities:
	Use of Django forms. Validation of input data in form with possible min and max values to avoid input of incorrect values. Form shows current date while opening of index page. However dates and years have selection fields.
	More than one model. Besides User model, There are two other models i.e. Data and Param. Type of model fields based on type of data input.
	Use of SQLite database to create tables and save records.
	Use of JavaScript. Besides log in/out and  register web pages, there is only one html template “index”.  All other programming are executed through JavaScript via index web page and view functions. JavaScript file has three functions which are executed via button click events. Fetch and PUT methods are used to receive and update data in SQL tables.
	For user convenience,  functionality of deletion of any record is added in case user enter incorrect data or there is a need to remove data from data base. Once data is removed, history table is updated.
	Use of Charts.js (JavaScript library for rendering charts in HTML5 canvas). All charts are rendered in canvas by this API. A Plug-in is used to add functionality of showing data-labels (values of data item) on line charts. When some data (record) is removed from history, all charts are updated with remaining data.
	Display of warning messages if user submit record without input of any single parameter data field. Warning message if delete record button pressed without single selection of row to delete.
	Success message displayed after data validation and storing data in data base table.
	(Mobile) Responsive design. Based on viewport size, data display adjusts automatically.
	The JavaScript program is optimised so that if additional parameters need to be included, minimum changes will be required in script.
	As the normal value of heath parameters are defined and constant, these values are recorded through creating superuser and by Django Administration page. These normal value ranges are displayed in respective charts with colour filled between ranges.
