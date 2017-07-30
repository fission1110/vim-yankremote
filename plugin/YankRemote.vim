if !has('python') && !has('python3')
	finish
endif

let s:scriptPath = expand('<sfile>:h') . '/../bin/'
let s:clientFile = 'vim/client.py'

if !exists('g:PasteSendIP')
	let g:PasteSendIP = '127.0.0.1'
endif

if !exists('g:PasteSendPort')
	let g:PasteSendPort = '9999'
endif

if !exists('g:PasteSendCert')
	let g:PasteSendCert = s:scriptPath . 'client/server.cert'
endif

if !exists('g:PasteSendClientCert')
	let g:PasteSendClientCert = s:scriptPath . 'client/client.cert'
endif

if !exists('g:PasteSendClientKey')
	let g:PasteSendClientKey = s:scriptPath . 'client/client.key'
endif

let s:python = ''
if has('python3')
	let s:python = '3'
endif

exec 'py'. s:python . 'file ' . s:scriptPath . s:clientFile

function! PasteSend(type, ...)
	let sel_save = &selection
	let &selection = "inclusive"
	echo a:type

	if a:0
		silent exe "normal! gvy"
	elseif a:type == 'line'
		silent exe "normal! '[V']y"
	else
		silent exe "normal! `[v`]y"
	endif

	exec 'python' . s:python . ' ' . 'PySendClipboard()'

	let &selection = sel_save
endfunction

nnoremap <silent> <Plug>PasteSend :set opfunc=PasteSend<CR>g@
xnoremap <silent> <Plug>PasteSend :<C-U>call PasteSend(visualmode(), 1)<CR>
nnoremap <silent> <Plug>PasteSendLine :<C-U>set opfunc=PasteSend<Bar>exec 'norm! 'v:count1.'g@_'<CR>


if !hasmapto('<Plug>PasteSend', 'n') || maparg('<leader>y', 'n') ==# ''
  nmap <leader>y <Plug>PasteSend
endif

if !hasmapto('<Plug>PasteSend', 'v') || maparg('<leader>y', 'v') ==# ''
  xmap <leader>y <Plug>PasteSend
endif

if !hasmapto('<Plug>PasteSendLine', 'n') || maparg('<leader>yy', 'n') ==# ''
  nmap <leader>yy <Plug>PasteSendLine
endif
