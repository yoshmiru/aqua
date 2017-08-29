const $temps = $('div#temps').empty()
$('.temp').each((i, el) => {
  $('<div>').text($(el).data('temp')).appendTo($temps)
})

// datepicker
$('.dtpick').datepicker({dateFormat: 'yy-mm-dd'});
