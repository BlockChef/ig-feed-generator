$(document).ready(function() {
    // Initialize the image slideshow
    $('.image-slideshow').slick({
        dots: true,
        infinite: true,
        speed: 500,
        fade: true,
        cssEase: 'linear'
    });

    // Show revision form when Revise button is clicked
    $('#reviseBtn').click(function() {
        $('#revisionForm').toggle();
    });

    // Handle Approve button click
    $('#approveBtn').click(function() {
        $.ajax({
            url: '/approve',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data.status === 'success') {
                    alert(data.message);
                    window.location.href = '/';
                } else {
                    alert('Error: ' + data.message);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });

    // Handle Submit Revision button click
    $('#submitRevision').click(function() {
        var suggestion = $('#suggestionInput').val().trim();
        if (suggestion === '') {
            alert('Please enter a revision suggestion.');
            return;
        }

        $.ajax({
            url: '/revise',
            type: 'POST',
            data: { suggestion: suggestion },
            dataType: 'json',
            success: function(data) {
                if (data.status === 'success') {
                    window.location.href = data.redirect;
                } else {
                    alert('Error: ' + data.message);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });
});