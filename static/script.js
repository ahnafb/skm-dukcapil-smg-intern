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
