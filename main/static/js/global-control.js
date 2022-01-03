// Toggle the sidebar
$('#sidebarBtn').on('click', function () {
    const sidebar = $('#sidebar');
    if (sidebar.hasClass('d-flex')) {
        sidebar.removeClass('d-flex');
        sidebar.addClass('d-none');
    } else {
        sidebar.removeClass('d-none');
        sidebar.addClass('d-flex');
    }
});