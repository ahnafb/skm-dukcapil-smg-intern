// !CRUD JENIS LAYANAN
$(document).ready(function () {
    $('#serviceForm').submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/add_service',
            data: formData,
            success: function (response) {
                alert(response.message); // Menggunakan alert browser
                $('#message').text(response.message);
                location.reload();
            },
            error: function (xhr, status, error) {
                alert('Error occurred while adding service.'); // Menggunakan alert browser
                $('#message').text('Error occurred while adding service.');
            }
        });
    });

    $('.editBtn').click(function () {
        var serviceItem = $(this).closest('li');
        var serviceName = serviceItem.find('.serviceName').text();
        var editedForm = serviceItem.find('.editForm');
        var editInput = editedForm.find('input[name="edited_name"]');
        editInput.val(serviceName);  // Isi nilai yang sudah ada ke dalam input editForm
        editedForm.show();
    });

    $('.editForm').submit(function (event) {
        event.preventDefault();
        var serviceItem = $(this).closest('li');
        var serviceId = serviceItem.find('.editBtn').data('id');
        var editedName = $(this).find('input[name="edited_name"]').val();
        $.ajax({
            type: 'POST',
            url: '/edit_service',
            data: { service_id: serviceId, new_name: editedName },
            success: function (response) {
                alert(response.message); // Menggunakan alert browser
                $('#message').text(response.message);
                location.reload(); // Reload halaman setelah berhasil disunting
            },
            error: function (xhr, status, error) {
                alert('Error occurred while editing service.'); // Menggunakan alert browser
                $('#message').text('Error occurred while editing service.');
            }
        });
    });

    $('.deleteBtn').click(function () {
        if (confirm("Are you sure you want to delete this service?")) {
            var serviceItem = $(this).closest('li');
            var serviceId = $(this).data('id');
            $.ajax({
                type: 'POST',
                url: '/delete_service',
                data: { service_id: serviceId },
                success: function (response) {
                    alert(response.message); // Menggunakan alert browser
                    $('#message').text(response.message);
                    serviceItem.remove(); // Hapus item layanan dari daftar setelah berhasil dihapus
                },
                error: function (xhr, status, error) {
                    alert('Error occurred while deleting service.'); // Menggunakan alert browser
                    $('#message').text('Error occurred while deleting service.');
                }
            });
        }
    });
});

// !CRUD JENIS KELAMIN
$(document).ready(function () {
    // Menangani submit form untuk menambah jenis kelamin
    $('#genderForm').submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/add_gender',
            data: formData,
            success: function (response) {
                alert(response.message);
                $('#message').text(response.message);
                location.reload();
            },
            error: function (xhr, status, error) {
                alert('Error occurred while adding gender.');
                $('#message').text('Error occurred while adding gender.');
            }
        });
    });

    // Menangani klik tombol edit untuk jenis kelamin
    $('.editGenderBtn').click(function () {
        var genderItem = $(this).closest('li');
        var genderName = genderItem.find('.genderName').text();
        var editedForm = genderItem.find('.editGenderForm');
        var editInput = editedForm.find('input[name="edited_name"]');
        editInput.val(genderName);
        editedForm.show();
    });

    // Menangani submit form edit untuk jenis kelamin
    $('.editGenderForm').submit(function (event) {
        event.preventDefault();
        // var genderItem = $(this).closest('li');
        // var genderId = $(this).find('.editGenderBtn').data('id');
        var genderId = $(this).closest('li').find('.editGenderBtn').data('id');
        var editedName = $(this).find('input[name="edited_name"]').val();
        $.ajax({
            type: 'POST',
            url: '/edit_gender',
            data: { gender_id: genderId, new_name: editedName },
            success: function (response) {
                alert(response.message);
                $('#message').text(response.message);
                location.reload();
            },
            error: function (xhr, status, error) {
                alert('Error occurred while editing gender.');
                $('#message').text('Error occurred while editing gender.');
            }
        });
    });

    // Menangani klik tombol delete untuk jenis kelamin
    $('.deleteGenderBtn').click(function () {
        if (confirm("Are you sure you want to delete this gender?")) {
            var genderItem = $(this).closest('li');
            var genderId = $(this).data('id');
            $.ajax({
                type: 'POST',
                url: '/delete_gender',
                data: { gender_id: genderId },
                success: function (response) {
                    alert(response.message);
                    $('#message').text(response.message);
                    genderItem.remove();
                },
                error: function (xhr, status, error) {
                    alert('Error occurred while deleting gender.');
                    $('#message').text('Error occurred while deleting gender.');
                }
            });
        }
    });
});

// !CRUD USIA
$(document).ready(function () {
    // Menangani submit form untuk menambah usia
    $('#ageForm').submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/add_age',
            data: formData,
            success: function (response) {
                alert(response.message);
                $('#message').text(response.message);
                location.reload();
            },
            error: function (xhr, status, error) {
                alert('Error occurred while adding age.');
                $('#message').text('Error occurred while adding age.');
            }
        });
    });

    // Menangani klik tombol edit untuk usia
    $('.editAgeBtn').click(function () {
        var ageItem = $(this).closest('li');
        var ageRange = ageItem.find('.ageRange').text();
        var editedForm = ageItem.find('.editAgeForm');
        var editInput = editedForm.find('input[name="edited_range"]');
        editInput.val(ageRange);
        editedForm.show();
    });

    // Menangani submit form edit untuk usia
    $('.editAgeForm').submit(function (event) {
        event.preventDefault();
        // var ageItem = $(this).closest('li');
        var ageId = $(this).closest('li').find('.editAgeBtn').data('id');
        var editedRange = $(this).find('input[name="edited_range"]').val();
        $.ajax({
            type: 'POST',
            url: '/edit_age',
            data: { age_id: ageId, new_range: editedRange },
            success: function (response) {
                alert(response.message);
                $('#message').text(response.message);
                location.reload();
            },
            error: function (xhr, status, error) {
                alert('Error occurred while editing age.');
                $('#message').text('Error occurred while editing age.');
            }
        });
    });

    // Menangani klik tombol delete untuk usia
    $('.deleteAgeBtn').click(function () {
        if (confirm("Are you sure you want to delete this age?")) {
            var ageItem = $(this).closest('li');
            var ageId = $(this).data('id');
            $.ajax({
                type: 'POST',
                url: '/delete_age',
                data: { age_id: ageId },
                success: function (response) {
                    alert(response.message);
                    $('#message').text(response.message);
                    ageItem.remove();
                },
                error: function (xhr, status, error) {
                    alert('Error occurred while deleting age.');
                    $('#message').text('Error occurred while deleting age.');
                }
            });
        }
    });
});
