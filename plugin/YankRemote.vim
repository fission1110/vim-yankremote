if !has('python') && !has('python3')
	finish
endif

let s:scriptPath = expand('<sfile>:h') . '/../bin/'
let s:clientFile = 'client.py'

if !exists('g:PasteSendIP')
	let g:PasteSendIP = '127.0.0.1'
endif

if !exists('g:PasteSendPort')
	let g:PasteSendPort = '9999'
endif

if !exists('g:PasteSendCert')
	let g:PasteSendCert = s:scriptPath . 'server.cert'
endif

if !exists('g:PasteSendClientCert')
	let g:PasteSendClientCert = s:scriptPath . 'client.cert'
endif

if !exists('g:PasteSendClientKey')
	let g:PasteSendClientKey = s:scriptPath . 'client.key'
endif

if has('python') && !has('python3')
	let s:pyPrefix = 'py'
	command -range PasteSend python PySendClipboard(<f-line1>,<f-line2>)
endif

if !has('python') && has('python3')
	let s:pyPrefix = 'py3'
	command -range PasteSend python3 PySendClipboard(<f-line1>,<f-line2>)
endif

exec s:pyPrefix . 'file ' . s:scriptPath . s:clientFile


