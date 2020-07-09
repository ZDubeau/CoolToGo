var validate = '<img src="/static/image/validate.png" style="height:18px;"/>';
var cancel = '<img src="/static/image/delete.png" style="height:18px;"/>';
var edit = '<img src="/static/image/edit-svgrepo-com.svg" style="height:18px;"/>';
var json = '<img src="/static/image/json.png" style="height:18px;"/>';
var on_off = '<img src="/static/image/toggle.jpeg" style="height:18px;"/>';

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
      { "width": "6px", "targets": 2 },        //id_selection
      { "width": "40px", "targets": 3 },
      { "targets": 4, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" }, //titre
      { "targets": 5, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" }, //profil
      { "width": "40px", "targets": 6 },          //categorie
      { "visible": false, "targets": 7 },         //adresse
      { "visible": false, "targets": 8 },
      { "visible": false, "targets": 9 },       // code_postal
      { "visible": false, "targets": 10 },      //ville
      { "width": "50px", "targets": 11 },       //altitude
      { "visible": false, "targets": 12 },      //latitude
      { "visible": false, "targets": 13 },      //longitude
      { "visible": false, "targets": 14 },      //telephone     
      { "visible": false, "targets": 15 },      //email 
      { "visible": false, "targets": 16 },      //site web
      { "visible": false, "targets": 17 },      //description courte
      { "visible": false, "targets": 18 },      //description détaillée
      { "visible": false, "targets": 19 },      //image
      { "targets": 20, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //publics
      { "targets": 21, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },  //tourisme_adaptes
      { "width": "20", "targets": 22 },         //payant    
      { "targets": 23, "render": $.fn.dataTable.render.ellipsis(19, false), className: "truncate" },  //animaux acceptés
      { "targets": 24, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },  //environnement
      { "targets": 25, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //equipement
      { "targets": 26, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //services
      { "targets": 27, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //periode
      { "targets": 28, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //activites
      { "targets": 29, "render": $.fn.dataTable.render.ellipsis(10, false), className: "truncate" },  //ouverture
      { "targets": 30, "render": $.fn.dataTable.render.ellipsis(9, false), className: "truncate" },  //typology
      { "targets": 31, "render": $.fn.dataTable.render.ellipsis(11, false), className: "truncate" },  //bons_plan
      { "targets": 32, "render": $.fn.dataTable.render.ellipsis(20, false), className: "truncate" },  //dispositions_speciales
      { "targets": 33, "render": $.fn.dataTable.render.ellipsis(15, false), className: "truncate" },  //service_enfants
      { "targets": 34, "render": $.fn.dataTable.render.ellipsis(16, false), className: "truncate" },  //service_cyclistes
      { "targets": 35, "render": $.fn.dataTable.render.ellipsis(12, false), className: "truncate" },  //nouveaute_2020
      { "width": "20px", "targets": 36 }
    ],
    // createdRow: function (row) {
    //   var td = $(row).find(".truncate");
    //   td.attr("title", td.html());
    // },
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(23)', nRow).html(edit);
      $('td:eq(23)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_ctg_profil/' + id;
      });
    }
  });

  $('#dataTableValid').DataTable({
    "sScrollX": "100%",
    "bScrollCollapse": true,
    "fixedHeader": {
      "header": false,
      "footer": false
    },
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "120px", "targets": 1 },
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
      { "width": "280px", "targets": 23 },
      { "width": "80px", "targets": 24 },
      { "width": "80px", "targets": 25 },
      { "width": "20px", "targets": 26 },
      { "width": "20px", "targets": 27 }
    ],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(25)', nRow).html(edit);
      $('td:eq(25)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_lieu_valide/' + id;
      });
      $('td:eq(26)', nRow).html(cancel);
      $('td:eq(26)', nRow).click(function () {
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
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_admin/' + id;
      });
    }
  });

  $('#dataelementreference').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "50px", "targets": 1 },
      { "width": "80px", "targets": 2 },
    ]
  });

  $('#dataTableSelection').DataTable({
    "columnDefs": [
      { "width": "15px", "targets": 0 },
      { "width": "40px", "targets": 1 },
      { "width": "50px", "targets": 2 },
      { "width": "130px", "targets": 3 },
      { "width": "100px", "targets": 4 },
      { "width": "35px", "targets": 5 },
      { "targets": 6, "render": $.fn.dataTable.render.ellipsis(40, false), className: "truncate" }, // CATEGORIES
      { "width": "36px", "targets": 7 },
      { "width": "49px", "targets": 8 }
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

  $('#dataTableProjet').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "50px", "targets": 1 },
      { "width": "60px", "targets": 2 },
      { "width": "25px", "targets": 3 },
      { "width": "25px", "targets": 4 },
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

  $('#dataTableCoolnessValues').DataTable({
    "columnDefs": [
      { "visible": false, "targets": 0 },
      { "width": "100px", "targets": 1 },
      { "width": "60px", "targets": 2 },
      { "width": "15px", "targets": 3 },
      { "width": "15px", "targets": 4 }
    ],
    "order": [[0, "desc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(3)', nRow).html(on_off);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/change_coolness_status/' + id;
      });
    }
  });

  $('#dataTableCategory').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0 },
      { "width": "180px", "targets": 1 },
      { "width": "20px", "targets": 2 },
      { "width": "20px", "targets": 3 }
    ],
    "order": [[0, "desc"]],
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

  $('#dataTableProfil').DataTable({
    "columnDefs": [
      { "width": "10px", "targets": 0 },
      { "width": "180px", "targets": 1 },
      { "width": "30px", "targets": 2 },
      { "width": "30px", "targets": 3 }
    ],
    "order": [[0, "desc"]],
    "fnRowCallback": function (nRow, aData) {
      $('td:eq(2)', nRow).html(edit);
      $('td:eq(2)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/edit_profil/' + id;
      });
      $('td:eq(3)', nRow).html(cancel);
      $('td:eq(3)', nRow).click(function () {
        var id = aData[0];
        window.location.href = '/delete_profil/' + id;
      });
    }
  });

});