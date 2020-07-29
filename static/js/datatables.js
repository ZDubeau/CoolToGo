// Last update 28 July 2020

var validate = '<img src="/static/image/validate.png" style="height:18px;"/>';
var cancel = '<img src="/static/image/delete.png" style="height:18px;"/>';
var edit = '<img src="/static/image/edit-svgrepo-com.svg" style="height:18px;"/>';
var json = '<img src="/static/image/json.png" style="height:18px;"/>';
var on_off = '<img src="/static/image/toggle.jpeg" style="height:18px;"/>';

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Apidae
// Call the dataTables jQuery plugin
$(document).ready(function () {
  $('#dataTableApidae').DataTable({
    "sScrollX": "100%",
    "bScrollCollapse": true,
    "fixedHeader": {
      "header": false,
      "footer": false
    },
    dom: 'Bfrtip',
    buttons: [{
      extend: 'colvis',
      collectionLayout: 'fixed four-column'
    }],
    "columnDefs": [
      { "visible": false, "targets": 0 },       //id primary key
      { "width": "10px", "targets": 1 },        //id_Apidae
      { "width": "5px", "targets": 2 },         //type_apidae
      { "width": "60px", "targets": [12, 13] }, //latitude, longitude

      //telephone, email, site web, description courte, description détaillée, image
      { "targets": [14, 15, 16, 17, 19], "visible": false },
      { "targets": 21, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },
      { "width": "20", "targets": 22 }, //payant 
      { "targets": 23, "render": $.fn.dataTable.render.ellipsis(19, false), className: "truncate" },
      { "targets": 24, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },

      // id_selection, titre, publics
      // equipement, services, periode, activites, ouverture, typology, bons_plan
      // dispositions_speciales, service_enfants, service_cyclistes, nouveaute_2020
      {
        "targets": [
          3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 20, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
        ],
        "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate"
      },
      { "width": "20px", "targets": 38 } // modify
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(32)', nRow).html(edit);
      $('td:eq(32)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_category_profil/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Apidae (json mode)
  $('#dataTableApidaejsonmode').DataTable({
    "sScrollX": "100%",
    "bScrollCollapse": true,
    "fixedHeader": {
      "header": false,
      "footer": false
    },
    dom: 'Bfrtip',
    buttons: [{
      extend: 'colvis',
      collectionLayout: 'fixed four-column'
    }],
    "columnDefs": [
      { "targets": 0, "width": "5px" },                                                               //id primary key
      { "targets": [1, 2], "width": "10px" },                                                         //ID APIDAE, TYPE APIDAE
      { "targets": 3, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },   //TITLE
      { "targets": 4, "render": $.fn.dataTable.render.ellipsis(12, false), className: "truncate" },   //PROFIL_CTG
      { "targets": 5, "render": $.fn.dataTable.render.ellipsis(17, false), className: "truncate" },   //CATEGORY_CTG
      { "targets": [6, 7], "render": $.fn.dataTable.render.ellipsis(13, false), className: "truncate" },   //ADDRESS 1 & 2
      { "targets": 8, "width": "20px" },                                                              //CODE POSTAL
      { "targets": 9, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },   //CITY
      { "targets": 10, "width": "15px" },                                                              //ALTITUDE
      { "targets": [11, 12], "width": "25px" },                                                        //LONGITUDE, LATITUDE
      { "targets": [13, 14, 15], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //TEL, MAIL, URL
      { "targets": [16, 17], "render": $.fn.dataTable.render.ellipsis(20, false), className: "truncate" },//DESCRIPTION SHORT & LONG
      { "targets": [18, 19], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },   //IMAGE, PUBLIC
      { "targets": 20, "render": $.fn.dataTable.render.ellipsis(18, false), className: "truncate" },   //ACCESSIBILITY
      { "targets": 21, "width": "10" },                                                                //PAYING
      { "targets": 22, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },   //ENVIRONMENT
      { "targets": 23, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },   //OPENING
      { "targets": [24, 25], "width": "15" },                                                          //DATE_START, DATE_END
      { "targets": 26, "width": "10", "className": "text-center" }  //***EDIT***
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(26)', nRow).html(edit);
      $('td:eq(26)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_category_profil/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table manual entry
  $('#dataTableManualEntry').DataTable({
    "sScrollX": "100%",
    "bScrollCollapse": true,
    "fixedHeader": {
      "header": false,
      "footer": false
    },
    dom: 'Bfrtip',
    buttons: [{
      extend: 'colvis',
      collectionLayout: 'fixed four-column'
    }],
    "columnDefs": [
      { "targets": 0, "visible": false },      //id primary key
      { "targets": 1, "width": "1px" },        //id_Apidae
      { "targets": 2, "width": "5px" },        //type_apidae
      { "targets": [3, 4, 5, 6, 7], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },
      { "targets": [9, 10], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },
      { "targets": [11, 12, 13, 14, 15, 16], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },
      { "targets": [18, 21, 24], "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },
      { "targets": [8, 17, 19, 20, 23, 25, 26, 27, 28, 32, 33, 34, 35, 36, 37], "visible": false },
      { "targets": 22, "width": "20" }, //payant
      { "targets": [29, 30, 31], "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },
      { "targets": [38, 39], "width": "20px" }, // Modify, Remove
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(22)', nRow).html(edit);
      $('td:eq(22)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_category_profil_manual_entry/' + id;
      });
      $('td:eq(23)', nRow).html(cancel);
      $('td:eq(23)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/remove_manual_entry/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Admin
  $('#dataTableAdmin').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0 },
      { "width": "50px", "targets": 1 },
      { "width": "80px", "targets": 2 },
      { "width": "10px", "targets": 3, "className": "text-center" }
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_admin/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Element Reference
  $('#dataelementreference').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "50px", "targets": 1 },
      { "width": "80px", "targets": 2 },
    ]
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Selection
  $('#dataTableSelection').DataTable({
    "columnDefs": [
      { "width": "15px", "targets": 0 },
      { "width": "40px", "targets": 1 },
      { "width": "50px", "targets": 2 },
      { "width": "130px", "targets": 3 },
      { "width": "140px", "targets": 4 },
      { "width": "35px", "targets": 5 },
      { "targets": 6, "render": $.fn.dataTable.render.ellipsis(40, false), className: "truncate" }, // CATEGORIES
      { "width": "36px", "targets": 7, "className": "text-center" },
      { "width": "49px", "targets": 8, "className": "text-center" }
    ],
    "fnRowCallback": function (nRow, aData) {

      $('td:eq(7)', nRow).html(validate);
      $('td:eq(7)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/launch_extract/' + id;
      });

      $('td:eq(8)', nRow).html(edit);
      $('td:eq(8)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_selection/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Projet
  $('#dataTableProjet').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "60px", "targets": [1, 2], "className": "text-center" },
      // { "width": "60px", "targets": 2 },
      { "width": "20px", "targets": [3, 4], "className": "text-center" },
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(2)', nRow).html(validate);
      $('td:eq(2)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/launch_selection_extract/' + id;
      });
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_projet/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Message
  $('#dataTableMessage').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "130px", "targets": 1 },
      { "width": "50px", "targets": 2 },
      { "width": "50px", "targets": 3 },
      { "width": "10px", "targets": 4 },
      { "width": "10px", "targets": 5 },
      { "width": "10px", "targets": 6 }
    ],
    "order": [[0, "desc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(edit);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_message/' + id;
      });
      $('td:eq(4)', nRow).html(json);
      $('td:eq(4)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/publish_message/' + id;
      });
      $('td:eq(5)', nRow).html(cancel);
      $('td:eq(5)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_message/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Coolness Values
  $('#dataTableCoolnessValues').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "100px", "targets": 1 },
      { "width": "60px", "targets": 2 },
      { "width": "15px", "targets": [3, 4], "className": "text-center" },
    ],
    "order": [[0, "asc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(on_off);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/change_coolness_status/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Category
  $('#dataTableCategory').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0, "className": "text-center" },
      { "width": "180px", "targets": 1, "className": "text-center" },
      { "width": "20px", "targets": [2, 3], "className": "text-center" },
    ],
    "order": [[0, "asc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(2)', nRow).html(edit);
      $('td:eq(2)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_category/' + id;
      });
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_category/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Profil
  $('#dataTableProfil').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0 },
      { "width": "180px", "targets": 1 },
      { "width": "30px", "targets": 2 },
      { "width": "30px", "targets": [3, 4], "className": "text-center" }
    ],
    "order": [[0, "asc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(edit);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_profil/' + id;
      });
      $('td:eq(4)', nRow).html(cancel);
      $('td:eq(4)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_profil/' + id;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Element Reference + Profil
  $('#dataEltPrf').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "visible": false, "targets": 1 },
      { "width": "30px", "targets": 2 },
      { "width": "30px", "targets": 3 },
      { "width": "30px", "targets": 4 }
    ],
    "order": [[0, "desc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(2)', nRow).html(cancel);
      $('td:eq(2)', nRow).click(function () {
        var id = aData[0];
        var id_profil = aData[1];
        window.location.href = '/delete_eltref_for_profil/' + id + '/' + id_profil;
      });
    }
  });
  //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Table Element Reference + Category
  $('#dataEltCtg').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "visible": false, "targets": 1 },
      { "width": "30px", "targets": 2 },
      { "width": "30px", "targets": 3 },
      { "width": "30px", "targets": 4 }
    ],
    "order": [[0, "desc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(2)', nRow).html(cancel);
      $('td:eq(2)', nRow).click(function () {
        var id = aData[0];
        var id_category = aData[1];
        window.location.href = '/delete_eltref_for_category/' + id + '/' + id_category;
      });
    }
  });
});