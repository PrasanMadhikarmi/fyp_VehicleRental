document.addEventListener('DOMContentLoaded', function () {
    const userDropdown = document.getElementById('userDropdown');
    const userDropdownContent = document.getElementById('userDropdownContent');

    userDropdown.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent the click event from propagating to the document
        // Toggle the visibility of the dropdown content
        if (userDropdownContent.style.display === 'block') {
            userDropdownContent.style.display = 'none';
        } else {
            userDropdownContent.style.display = 'block';
        }
    });

    // Close the dropdown when the user clicks outside of it
    document.addEventListener('click', function () {
        userDropdownContent.style.display = 'none';
    });

    // Prevent the dropdown from closing when clicking inside it
    userDropdownContent.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});
