var validate = '<img src="/static/image/validate.png" style="height:18px;"/>';
var cancel = '<img src="/static/image/delete.png" style="height:18px;"/>';
var edit = '<img src="/static/image/edit-svgrepo-com.svg" style="height:18px;"/>';
var change = '<img src="/static/image/change.jpeg" style="height:18px;"/>';

// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTableApidae').DataTable({
    "sScrollX" : "100%",
    "bScrollCollapse" : true,
    "fixedHeader": {
        "header": false,
        "footer": false
    },
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "110px", "targets": 1 },
      { "width": "70px", "targets": 2 },
      { "width": "70px", "targets": 3 },
      { "width": "400px", "targets": 4 },
      { "width": "120px", "targets": 5 },
      { "width": "80px", "targets": 6 },
      { "width": "80px", "targets": 7 },
      { "width": "350px", "targets": 8 },
      { "width": "350px", "targets": 9 },
      { "width": "80px", "targets": 10 },
      { "width": "180px", "targets": 11 },
      { "width": "100px", "targets": 12 },
      { "width": "300px", "targets": 13 },
      { "width": "800px", "targets": 14 },
      { "width": "1400px", "targets": 15 },
      { "width": "600px", "targets": 16 },
      { "width": "60px", "targets": 17 },
      { "width": "70px", "targets": 18 },
      { "width": "300px", "targets": 19 },
      { "width": "60px", "targets": 20 },
      { "width": "250px", "targets": 21 },
      { "width": "70px", "targets": 22 },
      { "width": "70px", "targets": 23 },
      { "width": "20px", "targets": 24 },
    ],
    "fnRowCallback" : function ( nRow, aData ) {
      $('td:eq(23)', nRow).html(validate);
      $('td:eq(23)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/validate_lieu/' + id;
      });
    }
  });

  $('#dataTableValid').DataTable({
    "sScrollX" : "100%",
    "bScrollCollapse" : true,
    "fixedHeader": {
        "header": false,
        "footer": false
    },
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "85px", "targets": 1 },
      { "width": "70px", "targets": 2 },
      { "width": "80px", "targets": 3 },
      { "width": "80px", "targets": 4 },
      { "width": "400px", "targets": 5 },
      { "width": "200px", "targets": 6 },
      { "width": "200px", "targets": 7 },
      { "width": "70px", "targets": 8 },
      { "width": "170px", "targets": 9 },
      { "width": "100px", "targets": 10 },
      { "width": "300px", "targets": 11 },
      { "width": "800px", "targets": 12 },
      { "width": "1400px", "targets": 13 },
      { "width": "1400px", "targets": 14 },
      { "width": "600px", "targets": 15 },
      { "width": "180px", "targets": 16 },
      { "width": "90px", "targets": 17 },
      { "width": "90px", "targets": 18 },
      { "width": "150px", "targets": 19 },
      { "width": "180px", "targets": 20 },
      { "width": "300px", "targets": 21 },
      { "width": "70px", "targets": 22 },
      { "width": "280px", "targets":23 },
      { "width": "80px", "targets":24 },
      { "width": "80px", "targets":25 },
      { "width": "20px", "targets":26 },
      { "width": "20px", "targets":27 }
    ],
    "fnRowCallback" : function ( nRow, aData ) {
      $('td:eq(25)', nRow).html(edit);
      $('td:eq(25)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/edit_lieu_valide/' + id;
      });
      $('td:eq(26)', nRow).html(cancel);
      $('td:eq(26)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/remove_lieu/' + id;
      });
    }
  });

  $('#dataTableAdmin').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0 },
      { "width": "50px", "targets": 1 },
      { "width": "80px", "targets": 2 },
      { "width": "10px", "targets": 3 }
    ],
    "fnRowCallback" : function ( nRow, aData ) {
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/delete_admin/' + id;
      });
    }
  });

  $('#dataTableSelection').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "20px", "targets": 1 },
      { "width": "80px", "targets": 2 },
      { "width": "30px", "targets": 3 },
      { "width": "80px", "targets": 4 },
      { "width": "40px", "targets": 5 },
      { "width": "20px", "targets": 6 },
      { "width": "20px", "targets": 7 },
    ],
    "fnRowCallback" : function ( nRow, aData ) {
      $('td:eq(5)', nRow).html(validate);
      $('td:eq(5)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/launch_extract/' + id;
      });
      $('td:eq(6)', nRow).html(cancel);
      $('td:eq(6)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/delete_selection/' + id;
      });
    }
  });

  $('#dataTableMessage').DataTable({
    "order": [[ 1, "desc" ]]
  });
  $('#dataTableCoolnessValues').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "100px", "targets": 1 },
      { "width": "60px", "targets": 2 },
      { "width": "15px", "targets": 3 }
    ],
    "order": [[ 0, "desc" ]],
    "fnRowCallback" : function ( nRow, aData ) {
      $('td:eq(2)', nRow).html(change);
      $('td:eq(2)', nRow).click( function () {
        var id = aData[0];
        window.location.href = '/change_coolness_status/' + id;
      });
    }
  });
});