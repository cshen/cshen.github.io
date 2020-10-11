

function changewidth( expand )
{
    var w = screen.width;
    // $("#layout-content").css({width: "80%" });
    var maxw = w * 0.75;
    var minw = 900;
        
    var e = document.getElementById('layout-content'); 
    var divWidth = parseInt(getStyle(e, 'width'));        // get the current width
    var inc = Math.round( w / 10.0);           // get how many pixels is 5 percent
   

    
    if (  expand < 1 && expand > 0  &&  (  divWidth < Math.round(maxw) ) )
    {
        $("#layout-content").css({width: divWidth + expand * inc });
    }


    if (  expand == 1 &&  (  divWidth < Math.round(maxw) ) )
    {
        $("#layout-content").css({width: divWidth + inc });
    }
    
    

    if (  expand == -1 &&  (  divWidth > Math.round( minw ) ) )
    {
        $("#layout-content").css({width: divWidth - inc });
    }
    
}

/***
 * get live runtime value of an element's css style
 *   http://robertnyman.com/2006/04/24/get-the-rendered-style-of-an-element
 *     note: "styleName" is in CSS form (i.e. 'font-size', not 'fontSize').
 ***/
var getStyle = function (e, styleName) {
    var styleValue = "";
    if(document.defaultView && document.defaultView.getComputedStyle) {
        styleValue = document.defaultView.getComputedStyle(e, "").getPropertyValue(styleName);
    }
    else if(e.currentStyle) {
        styleName = styleName.replace(/\-(\w)/g, function (strMatch, p1) {
            return p1.toUpperCase();
        });
        styleValue = e.currentStyle[styleName];
    }
    return styleValue;
}

