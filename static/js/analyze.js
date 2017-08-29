const $temps = $('div#temps').empty()
$('.temp').each((i, el) => {
  $('<div>').text($(el).data('temp')).appendTo($temps)
})

// datepicker
$('.dtpick').datepicker({dateFormat: 'yy-mm-dd'})

// plot
const plot = (logs) => {
  // temp
  Plotly.newPlot('temp', [{
    x: logs.map((log) => log.date),
    y: logs.map((log) => log.temp)
  }]
    , {
      xaxis: { title: '時間' },
      yaxis: { title: '温度', range: [-10, 50] },
      margin: { t: 0 }
    })
  // ec
  Plotly.newPlot('ec', [{
    x: logs.map((log) => log.date),
    y: logs.map((log) => log.ec)
  }]
    , {
      xaxis: { title: '時間' },
      yaxis: { title: '電気伝導度 アナログ入力(0-1024)', range: [400, 700] },
    })
}
plot(logs)
