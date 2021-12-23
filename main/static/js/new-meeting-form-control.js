const newAnnouncementBtn = $('#newAnnouncementBtn');
const newMotionBtn = $('#newMotionBtn');
const newExtemporeBtn = $('#newExtemporeBtn');

const announcementSection = $('#pAnnouncement');
const motionSection = $('#pMotion');
const extemporeSection = $('#pExtempore');

newAnnouncementBtn.click(function () {
    // Add an announcement to the meeting
    const announcementElement = '<div class="d-flex mb-2">' +
        '<textarea class="form-control" id="content" rows="2" ' +
        'aria-label="AnnouncementContent" placeholder="內容"></textarea>' +
        '<a href="javascript:void(0)" class="delete-announcement my-auto ms-2">' +
        '<img src="static/images/trash-fill.svg" width="20" alt=""></a></div>';
    announcementSection.append(announcementElement);
});

newMotionBtn.click(function () {
    // Add a motion to the meeting
    motionSection.append();
});

newExtemporeBtn.click(function () {
    // Add an extempore to the meeting
    extemporeSection.append('<textarea class="form-control mb-2" id="content" rows="2"' +
        ' aria-label="ExtemporeContent" placeholder="內容"></textarea>');
});

$('.delete-announcement').on('click', function () {
    console.log('clicked');
})