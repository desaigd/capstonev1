

document.addEventListener('DOMContentLoaded', function() {
  //  Get element and on-click execute function  
  document.querySelector('#gethistory').addEventListener('click', get_history);
  document.querySelector('#gettrend').addEventListener('click', get_trend);
  document.querySelector('#deleterecord').addEventListener('click', delete_record);
  document.querySelector('#table-view').style.display = 'none';
  document.querySelector('#chart-view').style.display = 'none';
});




//  History visible on click of button
function get_history() {
  document.querySelector('#table-view').style.display = 'block';
  elmsgs = document.querySelector('.messages');
  if(elmsgs ){
    document.querySelector('.messages').style.display = 'none';
  }
  
}




// Delete selected record (row) from html page and from database 
function delete_record(){
  var table = document.getElementById('recordtable');
  var rowcount = table.rows.length;

  // Find selected row and id of that row (record)
  let rowid_todelete = [];
  let index = [];
  var element =[];
  
  // Itereate from 1 as row[0] is header row
  for(var i=1; i<rowcount; i++){
    // Get the row id of checked rows and push in array
    element[i] = table.rows[i].cells[0].children[0];
    if (element[i].checked) {
      rowid_todelete.push(table.rows[i].id);
      index.push(table.rows[i].rowIndex);
    }
  }
 
  // with PUT method, send id of the row/s to be deleted, to view function 'deleterecord()'
  fetch("/deleterecord", {
    method: 'PUT',
    body: JSON.stringify({
    rowid: rowid_todelete,
    })
  })
  .then(response => response.json())
  .then(result => {
    document.querySelector("#mes").innerHTML = `${result.message}`;
    document.querySelector("#mes").style.display = 'block';
  })
  
  // Delete selected rows by getting checked rows by id in document.  
  var j=0;
    while (j<rowid_todelete.length){
      document.getElementById(rowid_todelete[j]).remove();
      j++;
    }

    // Destroy previous charts as record is deleted.
    var l = table.rows[0].cells.length;
    // for 'Select' and 'Date' column no chart exist i.e iterate upto c<l-2 to get Chart id
    for (let c=0; c<l-2; c++){  
    // JS - Destroy exiting Chart Instance to reuse <canvas> element
    let chartStatus = Chart.getChart("myChart"+c); // <canvas> id
    
    if (chartStatus != undefined) {
      
      chartStatus.destroy();
    }
    //-- End of chart destroy   
  }
  // End of delete_record
}





// on click get multiple charts of all parameters
function get_trend() {
 
  // Delete previous messages if any
  elmsg = document.querySelector('.messages');
  if(elmsg ){
    document.querySelector('.messages').style.display = 'none';
  }
  document.querySelector("#mes").style.display = 'none';
 
  
  // Stores normal value of parameters
  var nv = [];
   // Gets normal values, title of each parameter
   fetch("/normalval")
   .then(response => response.json())
   .then ( content => {
    for (let c of content){
      nv.push(c);
    }
    
  var rec = [];
  var labels = [];
  var parameters = [];
  for (let m=0; m<nv.length; m++){
    parameters[m] = [];
  }
  
  fetch("/chart")
  .then(response => response.json())
  .then(record => {

    for (let r of record){
      rec.unshift(r);
      //store dates in array to create x axis of charts
      labels.unshift(r.date)
      //store each parameter value in seperate arrays for each record 
      parameters[0].unshift(r.fs);
      parameters[1].unshift(r.pp);
      parameters[2].unshift(r.hba1c);
      parameters[3].unshift(r.hb);
      parameters[4].unshift(r.rbc);
      parameters[5].unshift(r.wbc);
      parameters[6].unshift(r.pl);
      parameters[7].unshift(r.cr); 
    };

    const myData = [];
    const config = [];
    const arr = [];
    //To create normal values chart, against first and last record date, high value of each parameter
    // recorded. Remaining arr values filled with null values (to remove datalables) to create straight line chart
    // of normal value high. It will be filled upto normal value low later.
    for (let j=0; j<nv.length; j++){
      arr[j] = [nv[j].normalval_high];
        for (let i=0; i<rec.length-2; i++){
          arr[j].push('null');
        }
      arr[j].push(nv[j].normalval_high); 
    };
    
    // To generate chart, create x(labels) and y(parameter value) axis data for each parameter and save in myData array
    for (let p=0; p<nv.length; p++){
      myData[p] = {
        labels: labels,
        datasets: [{
          label: nv[p].param,
          backgroundColor:'rgb(0, 0, 255)',
          borderColor: 'rgb(0, 0, 255)',
          borderWidth: 1,
          data: parameters[p],
      }, {
        //Dataset for Normal value of each parameter
        label: nv[p].title,
        backgroundColor:'rgba(91, 255, 77, 0.2',
        borderColor: 'rgb(255, 255, 255)',
        borderWidth: 1,
        data: arr[p],
        fill: {value:nv[p].normalval_low},
        }] 
      }
    };

    //create config array for charts
    for (var i = 0; i < nv.length; i++) {
      config[i] = {
        type: 'line',
        data: myData[i],
        plugins: [ChartDataLabels],
        options: {
          scales: {
            yAxes: {
              beginAtZero: true,
            } 
          },
          spanGaps: true,
          plugins:{
            datalabels: {
              anchor: 'end',
              align: 'end',
              labels: {
                value: {
                  color: 'blue',
                }
              }
            }
          }
        }
      }
    };

  //create empty canvas elements to create chart
  for (var a = 0; a < nv.length; a++) {
  let elem = document.createElement('div');
  elem.className= 'col';
  let eleminner = document.createElement('canvas');
  eleminner.id = 'myChart'+a;
  elem.appendChild(eleminner);
  document.querySelector('#chart-view').appendChild(elem);
  }

  var ctx = [];
  var myChart =[];
  for (var b = 0; b < nv.length; b++) {
    ctx[b] = document.getElementById('myChart'+b);
  }

  for (var d = 0; d < nv.length; d++) {
    myChart[d] = new Chart(ctx[d], config[d]);
  }

  //Destroy previous chrarts if any
  for (var e = 0; e < nv.length; e++) {
    myChart[e].destroy();
  }

  // Create new charts
  for (var f = 0; f < nv.length; f++) {
    myChart[f] = new Chart(ctx[f], config[f]);
  }

  document.querySelector('#chart-view').style.display = 'block';
   
  });
});
}
