const url = `http://${document.domain}:${location.port}`
const socket = io.connect(url)
const cam = 'http://www.explop.com/goldfish'

$ledCtl = $('#led-ctl')
$('#cam-ctl').click(() => {
    $cam = $('#cam')
    if ($cam.attr('src')) {
	$cam.attr('src', '')
    } else {
	$cam.attr('src', cam)
    }
})

socket.once('connect', () => {
  $ledCtl
    .prop('disabled', false)
    .click(on)
  $('#servo-ctl')
    .prop('disabled', false)
    .click(() => socket.emit('servo ctl'))
  setInterval(() => {
      socket.emit('read temp', (v) => $('#temp').text(v.toFixed(2)))
      socket.emit('read ec', (v) => $('#ec').text(v.toFixed(2)))
  }, 5000)
}).on('alert', (msg) => alert(msg))
  .on('feed info', (now) => $('#last-feed').text(now))

const on = () => {
  $ledCtl
    .unbind('click',on)
    .addClass('on')
    .click(off)
  socket.emit('led ctl', true);
}

const off = () => {
  $ledCtl
    .unbind('click',off)
    .removeClass('on')
    .click(on)
  socket.emit('led ctl', false);
}
