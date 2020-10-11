
function loadw(myurl)
{
  var argv = loadw.arguments;
  var argc = argv.length;

  if (argc < 1) 
  {
      myurl = 'bib.txt';
  }

  window.open(myurl,'bibtex','scrollbars=no,menubar=no,height=300,width=660,resizable=yes,toolbar=no,location=no,status=no');
}


