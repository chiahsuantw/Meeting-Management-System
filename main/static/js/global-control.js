// Toggle the sidebar
$('#sidebarBtn').on('click', function () {
    const sidebar = $('#sidebar');
    if (sidebar.hasClass('d-md-flex')) {
        sidebar.removeClass('d-md-flex');
        sidebar.addClass('d-none');
    } else {
        sidebar.removeClass('d-none');
        sidebar.addClass('d-md-flex');
    }
});