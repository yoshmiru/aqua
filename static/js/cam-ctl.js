/*const url = `http://${document.domain}:${location.port}`
const socket = io.connect(url)*/
const $controler = $('#cam-move')
const $cursor = $('#cam-move-cursor')
const $posX = $('#cam-pos-x')
const $posY = $('#cam-pos-y')

const deg = (pos, width) => {
  const margin = 0.9
  const full = width / 2
  const delta = pos - full
  return 90 * delta / (full * margin)
}

const update = () => {
  // show initial angle
  const pos = $cursor.position()
  const x = deg(pos.left, $controler.width())
  const y = deg(pos.top, $controler.height())
  $posX.text(x)
  $posY.text(y)
  socket.emit('cam ctl', x, y)
}

const camMv = (ev) => {
  //ev.target.style.cursor = 'grabbing'
  //$(document.body).addClass('dragging')
  //ev.dataTransfer.effectAllowed = "move";
  ev.dataTransfer.setData("text", ev.target.id)
}

const camMvEnd = (ev) => {
  ev.preventDefault()
  const posCtl = $controler.position()
  const offsetX = posCtl.left - window.scrollX
  const offsetY = posCtl.top - window.scrollY
  $cursor.css({'top': ev.clientY - offsetY, 'left': ev.clientX - offsetX})
  // update angle
  update()
}

const allowDrop = (ev) => {
  ev.preventDefault()
}

const addDropEffect = (ev) => {
  //ev.dataTransfer.dropEffect = "move";
}

// initialize
update()