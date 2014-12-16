

// Make disabled and active pages not able to be clicked.
$('.blog-pagination .disabled a, .blog-pagination .active a').on('click', function(e) {
    e.preventDefault();
});