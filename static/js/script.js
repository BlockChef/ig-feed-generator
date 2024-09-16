// Character count for caption
const caption = document.getElementById('caption');
const charCount = document.getElementById('charCount');
caption.addEventListener('input', function() {
    charCount.textContent = `${this.value.length} / 2200 characters`;
});

// Hashtag functionality
const hashtagInput = document.getElementById('hashtagInput');
const addHashtagBtn = document.getElementById('addHashtag');
const hashtagContainer = document.getElementById('hashtagContainer');
const hashtagsInput = document.getElementById('hashtags');
const hashtags = new Set();

function updateHashtags() {
    hashtagsInput.value = Array.from(hashtags).join(',');
    hashtagContainer.innerHTML = Array.from(hashtags).map(tag => 
        `<span class="hashtag">${tag} <button type="button" onclick="removeHashtag('${tag}')">&times;</button></span>`
    ).join('');
}

function addHashtag() {
    const tag = hashtagInput.value.trim().replace(/^#/, '');
    if (tag && !hashtags.has(`#${tag}`)) {
        hashtags.add(`#${tag}`);
        updateHashtags();
        hashtagInput.value = '';
    }
}

function removeHashtag(tag) {
    hashtags.delete(tag);
    updateHashtags();
}

addHashtagBtn.addEventListener('click', addHashtag);
hashtagInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        addHashtag();
    }
});

// Media preview and validation
const mediaInput = document.getElementById('media');
const mediaPreview = document.getElementById('mediaPreview');
const maxFiles = 10;

mediaInput.addEventListener('change', function() {
    if (this.files.length > maxFiles) {
        alert(`You can only upload a maximum of ${maxFiles} files.`);
        this.value = '';
        return;
    }

    mediaPreview.innerHTML = '';
    for (let file of this.files) {
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.height = 100;
            mediaPreview.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.height = 100;
            video.controls = true;
            mediaPreview.appendChild(video);
        }
    }
});

// Initialize Flatpickr for date and time picker
flatpickr("#schedule", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    minDate: "today"
});


$('#postForm').on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    $.ajax({
        url: '/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.status === 'success') {
                window.location.href = response.redirect;
            } else {
                alert('Error: ' + response.message);
            }
        },
        error: function(xhr, status, error) {
            alert('An error occurred: ' + error);
        }
    });
});