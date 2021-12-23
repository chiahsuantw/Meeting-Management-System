const newAnnouncementBtn = $('#newAnnouncementBtn');
const newMotionBtn = $('#newMotionBtn');
const newExtemporeBtn = $('#newExtemporeBtn');

const announcementSection = $('#pAnnouncement');
const motionSection = $('#pMotion');
const extemporeSection = $('#pExtempore');

newAnnouncementBtn.on('click', function () {
    // Add an announcement to the meeting
    const announcementElement = '<div class="d-flex mb-2">' +
        '<textarea class="form-control" rows="2" ' +
        'aria-label="AnnouncementContent" placeholder="內容"></textarea>' +
        '<a href="javascript:void(0)" class="my-auto ms-2">' +
        '<img src="static/images/trash-fill.svg" width="20" alt=""></a></div>';
    announcementSection.append(announcementElement);
});

newMotionBtn.on('click', function () {
    // Add a motion to the meeting
    const motionElement =
        '<div class="d-flex mb-2"><div class="border rounded px-2 flex-fill">' +
        '<div class=my-2>' +
        '<h6>案由</h6><input class=form-control aria-label=MotionDescription>' +
        '</div><div class=mb-2><h6>狀態</h6>' +
        '<select class=selectpicker data-style=bg-white data-width=100% aria-label=MotionStatus>' +
        '<option value=InDiscussion selected>討論中</option>' +
        '<option value=InExecution>執行中</option>' +
        '<option value=Closed>結案</option>' +
        '</select></div>' +
        '<div class=mb-2>' +
        '<h6>內容</h6>' +
        '<textarea type=text class=form-control rows=3 aria-label=MotionContent></textarea></div>' +
        '<div class=mb-2>' +
        '<h6>決策</h6><textarea type=text class=form-control rows=3 aria-label=MotionResolution></textarea>' +
        '</div><div class=mb-2>' +
        '<h6>執行</h6><textarea type=text class=form-control rows=3 aria-label=MotionExecution></textarea>' +
        '</div></div><a href=javascript:void(0) class="my-auto ms-2">' +
        '<img src=static/images/trash-fill.svg width=20 alt=""></a></div>';
    motionSection.append(motionElement);
    $('select').selectpicker();
});

newExtemporeBtn.on('click', function () {
    // Add an extempore to the meeting
    const extemporeElement = '<div class="d-flex mb-2">' +
        '<textarea class="form-control" rows="2" ' +
        'aria-label="ExtemporeContent" placeholder="內容"></textarea>' +
        '<a href="javascript:void(0)" class="my-auto ms-2">' +
        '<img src="static/images/trash-fill.svg" width="20" alt=""></a></div>';
    extemporeSection.append(extemporeElement);
});

announcementSection.on('click', 'div > a', function () {
    // Delete the announcement
    $(this).parent().remove();
})

motionSection.on('click', 'div > a', function () {
    // Delete the announcement
    $(this).parent().remove();
})

extemporeSection.on('click', 'div > a', function () {
    // Delete the announcement
    $(this).parent().remove();
})