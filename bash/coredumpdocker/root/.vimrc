set nocompatible        " must be first line
set background=dark     " Assume a dark background
set runtimepath=$HOME/.vim,$VIM/vimfiles,$VIMRUNTIME,$VIM/vimfiles/after,$HOME/.vim/after

" General {
    filetype plugin indent on   " Automatically detect file types.
    syntax on                   " syntax highlighting
    set mouse=a                 " automatically enable mouse usage
    scriptencoding utf-8
    set shortmess+=filmnrxoOtT      " abbrev. of messages (avoids 'hit enter')
    set viewoptions=folds,options,cursor,unix,slash " better unix / windows compatibility
    set virtualedit=onemore         " allow for cursor beyond last character
    set history=1000                " Store a ton of history (default is 20)
    set nospell                       " spell checking on
    set backup                      " backups are nice ...
    " Moved to function at bottom of the file
    set backupdir=$HOME/.vimbackup//  " but not when they clog .
    set directory=$HOME/.vimswap//     " Same for swap files
    set viewdir=$HOME/.vimviews//  " same for view files
    au BufWinLeave * silent! mkview  "make vim save view (state) (folds, cursor, etc)
    au BufWinEnter * silent! loadview "make vim load view (state) (folds, cursor, etc)
" }

" Vim UI {
    if has('gui_running')
        color solarized             " load a colorscheme
    else
        color desert
    endif
    if has('cmdline_info')
        set ruler                   " show the ruler
        set rulerformat=%30(%=\:b%n%y%m%r%w\ %l,%c%V\ %P%) " a ruler on steroids
        set showcmd                 " show partial commands in status line and
                                    " selected characters/lines in visual mode
    endif
    set tabpagemax=15               " only show 15 tabs
    set showmode                    " display the current mode
    set cursorline                  " highlight current line
    set so=7
    hi cursorline guibg=#333333     " highlight bg color of current line
    hi CursorColumn guibg=#333333   " highlight cursor

    set backspace=indent,eol,start  " backspace for dummys
    set linespace=0                 " No extra spaces between rows
    set nu                          " Line numbers on
    set showmatch                   " show matching brackets/parenthesis
    set incsearch                   " find as you type search
    set hlsearch                    " highlight search terms
    set winminheight=0              " windows can be 0 line high
    set ignorecase                  " case insensitive search
    set smartcase                   " case sensitive when uc present
    set wildmenu                    " show list instead of just completing
    set wildmode=list:longest,full  " command <Tab> completion, list matches, then longest common part, then all.
    set whichwrap=b,s,h,l,<,>,[,]   " backspace and cursor keys wrap to
    set scrolljump=5                " lines to scroll when cursor leaves screen
    set scrolloff=3                 " minimum lines to keep above and below cursor
    set foldenable                  " auto fold code
    set gdefault                    " the /g flag on :s substitutions by default
    set list
    set listchars=tab:>.,trail:.,extends:#,nbsp:. " Highlight problematic whitespace

    " No sound on errors
    set noerrorbells
    set novisualbell
    set t_vb=
    set tm=500
" }

set si "Smart indent

" GUI Settings {
    " GVIM- (here instead of .gvimrc)
    if has('gui_running')
        set guioptions-=T           " remove the toolbar
        set t_Co=256
        set lines=60                " 40 lines of text instead of 24,
        set columns=120
    else
        set term=builtin_ansi       " Make arrow and other keys work
        colorscheme mango
        "colorscheme enigma
    endif
" }

" Formatting {
    set nowrap                      " wrap long lines
    set autoindent                  " indent at the same level of the previous line
    set expandtab                   " tabs are spaces, not tabs
    set tabstop=4                   " an indentation every four columns
    set softtabstop=4               " let backspace delete indent
    set shiftwidth=4                " use indents of 4 spaces
    set matchpairs+=<:>                " match, to be used with %
    set pastetoggle=<F12>           " pastetoggle (sane indentation on pastes)
    set comments=sl:/*,mb:*,elx:*/  " auto format comment blocks
    " Remove trailing whitespaces and ^M chars
    " autocmd FileType c,cpp,java,php,js,python,twig,xml,yml autocmd BufWritePre <buffer> :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
" }
:set smartcase

if has('cscope') 
    set cscopetag cscopeverbose

    if has('quickfix')
        set cscopequickfix=s-,c-,d-,i-,t-,e-
    endif

    cnoreabbrev csa cs add
    cnoreabbrev csf cs find
    cnoreabbrev csk cs kill
    cnoreabbrev csr cs reset
    cnoreabbrev css cs show
    cnoreabbrev csh cs help

    """"""""""""" My cscope/vim key mappings
    "
    " The following maps all invoke one of the following cscope search types:
    "
    "   's'   symbol: find all references to the token under cursor
    "   'g'   global: find global definition(s) of the token under cursor
    "   'c'   calls:  find all calls to the function name under cursor
    "   't'   text:   find all instances of the text under cursor
    "   'e'   egrep:  egrep search for the word under cursor
    "   'f'   file:   open the filename under cursor
    "   'i'   includes: find files that include the filename under cursor
    "   'd'   called: find functions that function under cursor calls
    "
    " Below are three sets of the maps: one set that just jumps to your
    " search result, one that splits the existing vim window horizontally and
    " diplays your search result in the new window, and one that does the same
    " thing, but does a vertical split instead (vim 6 only).
    "
    " I've used CTRL-\ and CTRL-@ as the starting keys for these maps, as it's
    " unlikely that you need their default mappings (CTRL-\'s default use is
    " as part of CTRL-\ CTRL-N typemap, which basically just does the same
    " thing as hitting 'escape': CTRL-@ doesn't seem to have any default use).
    " If you don't like using 'CTRL-@' or CTRL-\, , you can change some or all
    " of these maps to use other keys.  One likely candidate is 'CTRL-_'
    " (which also maps to CTRL-/, which is easier to type).  By default it is
    " used to switch between Hebrew and English keyboard mode.
    "
    " All of the maps involving the <cfile> macro use '^<cfile>$': this is so
    " that searches over '#include <time.h>" return only references to
    " 'time.h', and not 'sys/time.h', etc. (by default cscope will return all
    " files that contain 'time.h' as part of their name).


    " To do the first type of search, hit 'CTRL-\', followed by one of the
    " cscope search types above (s,g,c,t,e,f,i,d).  The result of your cscope
    " search will be displayed in the current window.  You can use CTRL-T to
    " go back to where you were before the search.  
    "

    " nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>  
    " nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>  
    " nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>  
    " nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>  
    " nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>  
    " nmap <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>  
    " nmap <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
    " nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>  

    command -nargs=0 Cscope cs add $VIMSRC/src/cscope.out $VIMSRC/src
endif
"set csprg=cscope
"cd ~/Perforce/jbaoTAML/csPrj
"
"set clipboard=unnamedplus
"set paste
" For displaying UTF-8 Characters
set enc=utf-8
set fileencoding=utf-8
set fileencodings=ucs-bom,utf8,prc
"set guifont=Monaco:h11
"set guifontwide=NSimsun:h12
set viminfo='50,<1000,s100,h

