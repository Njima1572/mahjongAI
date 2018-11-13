syntax on
set number
set title
set showmatch
set tabstop=2
set number
set virtualedit=onemore
set smartindent
set list listchars=tab:\▸\-
set expandtab
set shiftwidth=2
set hlsearch
set smartindent
set wrapscan
set cursorcolumn
set cursorline
set showmatch
set showcmd
set laststatus=2
set visualbell
set autoindent
set backspace=indent,eol,start
set ruler

filetype on
filetype plugin on
hi SpecialKey guifg=Gray
hi CursorLine cterm=None term=reverse ctermbg=242
hi Special ctermbg=1
hi Normal ctermfg=224 guibg=NONE ctermbg=NONE
hi Constant ctermfg=LightBlue
hi Identifier ctermfg=Red
hi Cursor ctermbg=51
hi PreProc ctermfg=206 cterm=BOLD
hi String ctermfg=41
hi Repeat ctermfg=211 cterm=BOLD
hi SpecialKey ctermfg=208
hi Identifier ctermfg=218
hi pythonComment ctermfg=112 guibg=NONE
hi Comment ctermfg=112 guifg=NONE ctermbg=NONE guibg=NONE
"nnoremap <C-m> i
imap <C-a> <Esc>
imap <CR> <CR>
noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap j gj
noremap k gk
noremap <C-f> :/
noremap <C-r> :s/
noremap <C-w> :w<CR>
noremap <C-g> :
noremap <Right> <Nop>
