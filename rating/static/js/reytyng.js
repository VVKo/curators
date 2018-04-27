/**
 * Created by vv on 12.04.18.
 */




$('#add-kurator').click(function () {
            $.confirm({
                title: 'Додати куратора',
                theme: 'material',
                content:
                '<form  id="add-res">'+
                '<fieldset>'+
                    '<div class="panel panel-primary panel-heading">'+
                        '<legend><h2>Куратор</h2></legend>'+
                        '<div class="panel-title">Прізвище</div>'+
                        '<input type="text" class="panel-body" name="last_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">Імя</div>'+
                        '<input type="text" class="panel-body" name="first_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">По-батькові</div>'+
                        '<input type="text" class="panel-body" name="middle_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">Група</div>'+
                        '<input type="text" class="panel-body" name="group" value="">'+
                        '<br>'+
                    '</div>'+
                '</fieldset>'+
        '</form>',
                buttons: {
                    'Додати': {

                        action: function () {
                        $.ajax({
                            url: '/add/kurator',
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Куратора додано успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з додаванням');
                                    location.reload();
                                }
                        }
                        });
                    }
                    },
                    'Відмінити': {

                        action: function () {
                        toastr.info('Create Cancelled');
                    }}
                }
            });
  });

$('#add-group').click(function () {
            $.confirm({
                title: 'Додати групу',
                theme: 'material',
                content:
                '<form  id="add-res">'+
                '<fieldset>'+
                    '<div class="panel panel-primary panel-heading">'+
                        '<legend><h2>Група</h2></legend>'+
                        '<div class="panel-title">Назва групи</div>'+
                        '<input type="text" class="panel-body" name="group_name" value="">'+
                        '<br>'+
                    '</div>'+
                '</fieldset>'+
        '</form>',
                buttons: {
                    'Додати': {

                        action: function () {
                        $.ajax({
                            url: '/add/group',
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Групу додано успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з додаванням');
                                    location.reload();
                                }
                        }
                        });
                    }
                    },
                    'Відмінити': {

                        action: function () {
                        toastr.info('Create Cancelled');
                    }}
                }
            });
  });

function local_message() {
    if (localStorage.getItem('result')) {
            switch (localStorage.getItem('result')) {
                case 'true' :
                    toastr.success(localStorage.getItem('message'));
                    break;
                case 'false' :
                    toastr.error(localStorage.getItem('message'));
                    break;
            }
            localStorage.clear();
        }
}

function table_group_detail(url, group) {
    $.ajax({
			url : url,
			type : 'GET',
            dataType: 'json',
			success: function(res){
				var div = $('<div>')
                    .attr('class', 'table-responsive')
                    .append($('<table>')
        .attr('class', 'table table-striped table-sm')
        .append(
            $('<thead>')
                .append(
                    $('<tr>')
                        .append(
                            $('<th>').text('#'),
                            $('<th>').text('ПІП'),
                                $('<th>').text('Група'),
                            $('<th>').text('Різне')
                        )
                ),
            $('<tbody>')

        )
                    );

				var tr = $('<tr>');


				var module = '';
				$.each(res,function(index, value){
					module = $(tr).clone();
                    var studId = value.id;

					$(module).append(
                            $('<td>').text(index+1),
                            $('<td>').append(
                                    $('<a>').attr('href', window.location.pathname + 'student/'+ studId).attr('class', 'student').attr('student-id', studId).text(value.stud)),
                            $('<td>').text(group),
                            $('<td>').append($('<button>').attr('data-feather', 'trash').attr('data-student-id',studId).attr('class', 'delete-student'),
                            $('<button>').attr('data-feather', 'edit').attr('data-student-id', studId).attr('class', 'edit-student'))
                        );
					$(div).find('tbody').append(module);

				});

				$('#studentsDiv').append(div);
				feather.replace()
			},
			error: function(error){
				console.log(error);
			}
		});

}

function add_student(id_button, url, csrf, group) {


    $(id_button).click(function () {
        $.confirm({
            title: 'Додати студента',
            theme: 'material',
            content: function () {
                var self = this;
                return $.ajax({
                    url: url,
                    dataType: 'json',
                    type: 'get'
                }).done(function (res) {
                    console.log(res);
                    var form = $('<form>').attr('id', 'add-res')
                        .append(
                            $('<input>')
                                                .attr('type', 'hidden')
                                                .attr('name', 'csrfmiddlewaretoken')
                                                .attr('value', csrf),
                            $('<fieldset>')
                                .append(
                                    $('<div>').attr('class', 'panel panel-primary panel-heading')
                                        .append(
                                            $('<legend>').append($('<h2>').text('Студент')),
                                            $('<div>').attr('class', 'panel-title').text('Прізвище'),
                                            $('<input>')
                                                .attr('type', 'text')
                                                .attr('class', 'panel-body')
                                                .attr('name', 'last_name')
                                                .prop("required", true),
                                            $('<div>').attr('class', 'panel-title').text("Ім'я"),
                                            $('<input>').attr('type', 'text').attr('class', 'panel-body').attr('name', 'first_name'),
                                            $('<div>').attr('class', 'panel-title').text("По-батькові"),
                                            $('<input>').attr('type', 'text').attr('class', 'panel-body').attr('name', 'middle_name'),
                                            $('<div>').attr('class', 'panel-title').text("Група"),
                                            $('<input>')
                                                .attr('type', 'text')
                                                .attr('class', 'panel-body')
                                                .prop('readonly', true)
                                                .attr('name', 'group').attr('value', group)

                                        )));

                    self.setContent(form);
                }).fail(function () {
                    self.setContent('Something went wrong.');
                });
            },
            buttons: {
                'Додати': {

                    action: function () {
                       // name = $('#add-res').serialize();
                        $.ajax({
                            url: url,
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                                localStorage.setItem('result', response.success);
                                if (response.success) {
                                    localStorage.setItem('message', 'Студента додано успішно');
                                    location.reload();
                                }
                                else {
                                    localStorage.setItem('message', 'Пробеми з додаванням. Можливо не усі поля заповнені');
                                    location.reload();
                                }
                            }
                        });
                    }
                },
                'Відмінити': {

                    action: function () {
                        toastr.info('Create Cancelled');
                    }
                }
            }
        });
    });
}


function delete_student(url) {
    $('#studentsDiv').on('click','.delete-student', function () {
        var student_id = $(this).attr('data-student-id');
            $.confirm({
                title: 'Видалення Студента',
                content: 'Ви впевнені, що хочете видалити?',
                theme: 'material',
                buttons: {
                'Видалити': {
                    action: function () {
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: {'student_id':student_id},
                        success: function (response, data) {
                            console.log('bla-bla', $(this).attr('data-student-id'));
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Студента з бази видалено успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з видаленням');
                                    location.reload();
                                }
                        }
                    });
                }},
                'Відхилити':{
                    action: function () {
                        toastr.info('Delete Cancelled');
                    }
                }

            }
            })
    });


}
/*
function student() {
    $('#studentsDiv').on('click','.student', function () {
        var student_id = $(this).attr('student-id');
        var url = $(this).attr('href');
            $.ajax({
                        url: url,
                        type: 'POST',
                        data: {'student_id':student_id},
                        success: function () {
                            location.href = window.location.pathname + 'student/'+student_id
                        }
                    });
    });


}
*/
