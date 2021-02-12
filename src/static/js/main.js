const formRegex = RegExp(`images-(\\d){1}-`,'g')
const totalForms = $('#id_images-TOTAL_FORMS');
const imageForm = $('.image-form');
function previewImage(evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;
    
    const preview = $(this).parent().children('img');
    const to_add_form = $(this).attr('data-add-form');

    const current_input = this;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            $(preview).attr('src', fr.result);
            if(to_add_form) {
                addForm();
                $(current_input).removeAttr('data-add-form')
            }
        }
        fr.readAsDataURL(files[0]);
    }
    else {
        // No preview functionality
    }
}
function inputClick() {
    const inputBtn = $(this).parent().children('input[type="file"]');
    $(inputBtn).click();
}

function addForm() {
    const form_idx = $(totalForms).val();
    const newForm = $(imageForm).last().clone();
    const replaced = $(newForm).html().replace(formRegex, `images-${form_idx}-`)
    $(newForm).html(replaced);
    
    $(newForm).on('change', 'input[type="file"]', previewImage);
    $(newForm).on('click', 'img', inputClick);

    $('#addImageBtn').before(newForm);
    $(totalForms).val(parseInt(form_idx) + 1);
    return newForm;
}

$('.image-form').on('change', 'input[type="file"]', previewImage);
$('.image-form').on('click', 'img', inputClick);
$('#addImageBtn').on('click', function(e) {
    e.preventDefault();
    $('.image-form').last().children('input[type="file"]').attr('data-add-form', true).trigger('click');
});
$('.delete-image-btn').on('click', function(e) {
    e.preventDefault();
    const parent = $(this).parent();
    const delete_checkbox = $(parent).children('input[type="checkbox"]');
    $(delete_checkbox).prop("checked", true);
    $(parent).css('display', 'none');
})