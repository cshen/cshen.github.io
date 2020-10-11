
var start_year = 2003;

function takeYear(theDate) 
{
	x = theDate.getYear();
	var y = x % 100;
	y += (y < 38) ? 2000 : 1900;
	return y;
}


function msieversion()
{
   var ua = window.navigator.userAgent
      var msie = ua.indexOf ( "MSIE " )

      if ( msie > 0 )      // If Internet Explorer, return version number
         return parseInt (ua.substring (msie+5, ua.indexOf (".", msie )))
      else                 // If another browser, return 0
         return 0

}


function redirect()
{
    location.href = 'publication_static.html';
}


function supported_browser()
{
   //
   //  if(navigator.appName == "Netscape")
   //

   if(navigator.appName == "Microsoft Internet Explorer" &&  msieversion() < 8 )
   {
      document.write('<p>IE 8.0 is needed! I would recommend Firefox, Chrome or Opera.<\/p>');   
      
      document.write('<p>You will be redirected to the static HTML page in 2 seconds.<\/p>');   

      // redirect to the static publication link
      setTimeout('redirect()', 2000);
      
      return false;
   }

   else
      return true;
}


function paper_bytype()
{
      
      if ( ! supported_browser()) return -1;

      document.write('<h2>Journal (<a name="hits" id="hits" \
               title="number of journal papers">type:article<\/a>)<\/h2>');
      document.write('<ol name="search" id="search">type:article<\/ol>');

      document.write('<h2>Conference (<a name="hits" id="hits" \
               title="number of conference papers">type:inproceedings<\/a>)<\/h2>');
      document.write('<ol name="search" id="search">type:inproceedings<\/ol>');

      if (self.name != '_refreshed1')
      {
         self.name = '_refreshed1';
         self.location.reload(true);
      }
      else self.name = '';

}


function paper_byyear()
{         
      
      var today = new Date;
      cur_year  = takeYear(today);

      
      if ( ! supported_browser()) return -1;

      for (year = cur_year + 1; year >= start_year; --year)
      {
      document.write('<h2>' + year + ' (<a name="hits" id="hits" ');
      document.write('title="number of papers published in the year of ' + year + '">');
      document.write('year:' + year + '<\/a>)<\/h2>');   
      document.write('<ol name="search" id="search">year:' + year + '<\/ol>');
      }

      // reload once
      if (self.name != '_refreshed2')
      {
         self.name = '_refreshed2';
         self.location.reload(true);
      }
      else self.name = '';
}


function paper_byvenue()
{     
      var v = new Array("NIPS",
                        "ICCV",
                        "ECCV",
                        "CVPR",
                        "TPAMI",
                        "TIP",
                        "TNN",
                        "TCSVT",
                        "JASA");

      
      if ( ! supported_browser()) return -1;


      for (i = 0; i < v.length; i++)
      {
      document.write('<h2>' + v[i] + ' (<a name="hits" id="hits" ');
      document.write('title="number of papers published at ' + v[i] + '">');
      document.write('venue:' + v[i] + '<\/a>)<\/h2>');   
      document.write('<ol name="search" id="search">venue:' + v[i] + '<\/ol>');
      }

      // reload once
      if (self.name != '_refreshed3')
      {
         self.name = '_refreshed3';
         self.location.reload(true);
      }
      else self.name = '';

}



