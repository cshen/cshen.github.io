//  An object BibTexEntry and BibTexEntries
   // Copyright (c) 2005 Frank Dellaert
   //
   // modified by Chunhua Shen, 12/2008
   //

var bibtex={}
bibtex.error=function(html)
{return"<div class=\"bibtexError\">"+html+"</div>"}
bibtex.debug=function(str)
{document.write(bibtex.error(str));}
bibtex.inspect=function(obj)
{for(i in obj)bibtex.debug(i)}
bibtex.trim1=function(str)
{var pattern=/^\s*(\S.*\S)\s*$/;var a=pattern.exec(str);var result=str;if(a)
result=a[1];return result;}
bibtex.trim=function(str)
{function trim2(str)
{str=str.replace(/{/g,"");str=str.replace(/}/g,"");str=str.replace(/\s+/g," ");var pattern=/^.*\"(.*)\".*$/;var a=pattern.exec(str);var result=str;if(a)
result=a[1];return result;}
return trim2(bibtex.trim1(str));}
function BibTexEntry(text)
{if(!text)
throw("BibTexEntry: empty text");this.text=text;var i=text.indexOf('{');if(i==-1)throw("BibTexEntry: no { delimiter");var j=text.lastIndexOf('}');if(j==-1)throw("BibTexEntry: no } delimiter");this.type=text.slice(1,i);var inner=text.slice(i+1,j);var pairs=inner.split(',');this.key=pairs[0];if(!this.key)throw("BibTexEntry: no key");this.nrPairs=pairs.length;for(var k in pairs)
{if(k==0)continue;var pair=pairs[k];if(pair.length>2)
{var keyvalue=pair.split('=');if(keyvalue.length<2)
{this[key]+=", "+bibtex.trim(pair);continue;}
var key=bibtex.trim(keyvalue[0]).toLowerCase();var val=bibtex.trim(keyvalue[1]);for(var ln=2;ln<keyvalue.length;ln++)
val+="="+bibtex.trim(keyvalue[ln]);this[key]=val;}
else
{this.nrPairs=this.nrPairs-1;}}
switch(this.type.toLowerCase()){case"person":if(!this.name)throw"BibTexEntry: Person has no name";break;}}
BibTexEntry.prototype.toString=function(){return this.text}
BibTexEntry.prototype.toList=function()
{var string="<ul>";string+="<li>type : "+this.type;string+="<li>key  : "+this.key;string+="<li>author : "+this.author;string+="<li>year   : "+this.year;string+="<li>title  : "+this.title;switch(this.type.toLowerCase()){case"article":string+="<li>journal : "+this.journal;break;case"inproceedings":case"incollection":string+="<li>booktitle : "+this.booktitle;break;case"techreport":string+="<li>institution : "+this.institution;string+="<li>number      : "+this.number;break;}
return string+"</ul>";}
BibTexEntry.prototype.render=function(database)
{var string="<span class="+this.type+">";function expand(author)
{author=bibtex.trim1(author);if(!database)
string+=span("author",author);else
{var key=database.lookupPerson(author);if(!key)
string+=span("author",author);else
string+=database.entry(key).render();}}
function span(id,str)
{if(str==undefined)
return""
else
return"<span class=\""+id+"\">"+str+"</span>"}
function link(cls,url,text)
{return"<a class=\""+cls+"\" href=\""+url+"\">"+text+"</a>"}
function renderTitleAuthors(entry){if(entry.url)
string+=link("title",entry.url,entry.title);else
string+=span("title",entry.title);string+=" <br />";var authors=entry.author.split(" and ");var nrAuthors=authors.length;expand(authors[0]);if(nrAuthors==2){string+=" and ";expand(authors[1]);string+=" <br />";}
else{for(var i=1;i<nrAuthors;i++)
{if(i==nrAuthors-1){string+=", and "}
else{string+=", "}
expand(authors[i])}
string+=" <br />";}};function lookup(entry,database,field)
{var value=entry[field];try
{var entry=database.entry(value);str=entry.name;if(entry.url)
{string+=link(field,entry.url,str);}
else
{string+=span(field,str);}}
catch(err){string+=span(field,value);}}
switch(this.type.toLowerCase()){case"person":var str;if(this.url)
str=link("author",this.url,this.name);else
str=span("author",this.name);string+="<span id=\""+this.key+"\">"+str+"</span>";break;case"article":renderTitleAuthors(this);lookup(this,database,"journal");if(this.volume)
string+=", "+span("volume",this.volume);if(this.number)
string+="("+span("number",this.number)+")";if(this.pages)
string+=", pages "+span("pages",this.pages);if(this.year)
string+=", "+span("month",this.month)+" "+span("year",this.year);if(this.publisher)
string+=". "+span("publisher",this.publisher);break;case"inproceedings":case"incollection":renderTitleAuthors(this);lookup(this,database,"booktitle");if(this.volume)
string+=", volume "+span("volume",this.volume);if(this.number)
string+="("+span("number",this.number)+")";if(this.pages)
string+=", pages "+span("pages",this.pages);if(this.year)
string+=", "+span("month",this.month)+" "+span("year",this.year);if(this.address)
string+=". "+span("address",this.address);if(this.publisher)
string+=". "+span("publisher",this.publisher);break;case"techreport":renderTitleAuthors(this);lookup(this,database,"institution");string+=", "+span("number",this.number);string+=", "+span("year",this.year);break;}
if(this.note)
{string+="<br />"+span("note",this.note);}
if(this.pdf)
{string+="<br />";string+="<a href='"+this.pdf+"' class='pdf'>";string+="[PDF]</a>";}
if(this.arxiv)
{if(!this.pdf)
string+="<br />";else
string+=",&nbsp;&nbsp;";string+="<a href='http://arxiv.org/abs/"+this.arxiv+"' class='arxiv'>";string+="[arXiv]</a>";}
if(this.project)
{if(!this.arxiv)
string+="<br />";else
string+=",&nbsp;&nbsp;";string+="<a href='./"+this.project+"' class='project'>";string+="[Project page]</a>";}
return string+"</span>";}
function Database(strings){this.nrEntries=0;this.entries={};this.person={};for(var i in strings){var text=strings[i];if(text){try{var entry=new BibTexEntry('@'+text);this.entries[entry.key]=entry;this.nrEntries++;if(entry.type=="person"||entry.type=="Person")
this.person[entry.name]=entry.key;}
catch(err){bibtex.debug(err)}}}}
function DatabaseFromString(str)
{var strings=str.split('@');return new Database(strings);}
Database.prototype.entry=function(key){var entry=this.entries[key];if(entry)return entry;else throw"Database.entry: unknown BibTex key: "+key}
Database.prototype.lookupPerson=function(name){return this.person[name];}
Database.prototype.render=function(key){var entry=this.entry(key);return entry.render(this)}
function reverseChronological(d){return function(a,b){var x=d.entry(a).year;var y=d.entry(b).year;return((x>y)?-1:((x<y)?1:0));}}
Database.prototype.search=function(regex,fieldName,keys,compare){if(!fieldName)fieldName="text";fieldName=fieldName.toLowerCase();var result=[];if(!keys){keys=[];for(var key in this.entries){keys[keys.length]=key;}}
for(var i in keys){var key_i=keys[i];var entry=this.entry(key_i);try{var field=entry[fieldName];if(field.search(regex)!=-1)result[result.length]=entry.key;}
catch(err){}}
if(compare)return result.sort(compare(this));else return result.sort(reverseChronological(this));}
Database.prototype.searchQuery=function(query,keys){if(!query)throw"Database.searchQuery: empty search string";var parts=query.split(':');var field,regex;switch(parts.length){case 1:field="text";regex=new RegExp(parts[0],"m");break;case 2:field=bibtex.trim1(parts[0]);try{regex=new RegExp("^"+parts[1],"m");}
catch(err){regex=new RegExp(parts[1]);}
break;otherwise:throw"Database.searchQuery: malformed query";}
return this.search(regex,field,keys);}
Database.prototype.search3=function(str){if(!str)throw"Database.search3: empty search string";var queries=str.split(' ');var keys;for(var i in queries){keys=this.searchQuery(queries[i],keys);}
return keys;}
Database.prototype.keysToList=function(keys)
{var string="";var idx=0;for(var i in keys){try
{idx++;rev=keys.length-idx+1;if(idx%2)
string+="<li class='even' value = "+rev+" >"+this.render(keys[i])+"</li>";else
string+="<li class='odd' value = "+rev+" >"+this.render(keys[i])+"</li>";}
catch(err)
{string+="<li>"+bibtex.error("Entry \""+keys[i]+"\": "+err)+"</li>";}}
return string;}
Database.prototype.keysToUL=function(keys){return"<UL>\n"+this.keysToList(keys)+"</UL\n"}
function getTagText(node)
{if(node.textContent)
return node.textContent;else if(node.innerText)
return node.innerText;else if(node.childNodes[0])
return node.childNodes[0].nodeValue;else
throw"browser not supported";}
function setTagHTML(node,html)
{if(node.innerHTML)
return node.innerHTML=html;else
throw"browser not supported";}
var DatabaseFromDocument=function(){var element=document.getElementById("bibtex");return DatabaseFromString(getTagText(element));}
Database.prototype.replacePubs=function()
{var tags=document.getElementsByName("pub");for(var i=0;i<tags.length;i++){var element=tags[i];setTagHTML(element,this.render(getTagText(tags[i])));}}
Database.prototype.searchToUL=function(regex,field)
{document.write(this.keysToUL(this.search(regex,field)));}
var debug=false;Database.prototype.replaceSearches=function()
{var tags=document.getElementsByName("search");for(var i=0;i<tags.length;i++)
{var element=tags[i];var str=getTagText(element);try
{if(!str)
throw"no search string";var keys=this.search3(str);if(keys.length<=0)throw"null";if(debug)
element.textContent=this.keysToList(keys);else
{setTagHTML(element,this.keysToList(keys));}}
catch(err)
{setTagHTML(element,bibtex.error("search for \""+str+"\": "+err));}}}
Database.prototype.countHits=function()
{var tags=document.getElementsByName("hits");for(var i=0;i<tags.length;i++)
{var element=tags[i];var str=getTagText(element);try
{if(!str)throw"no search string";var keys=this.search3(str);setTagHTML(element,keys.length);}
catch(err)
{setTagHTML(element,bibtex.error("search for \""+str+"\": "+err));}}}
var xmlhttp;function getHTTP(url,callback){if(window.XMLHttpRequest){xmlhttp=new XMLHttpRequest();xmlhttp.onreadystatechange=callback;xmlhttp.open("GET",url,true);xmlhttp.send(null);}
else if(window.ActiveXObject){xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");if(!xmlhttp)throw"Could not access ActiveX object";xmlhttp.onreadystatechange=callback;xmlhttp.open("GET",url,true);xmlhttp.send();}
else throw"Browser does not support reading files";}
function alertContents()
{if(xmlhttp.readyState==4)
{var str=xmlhttp.responseText;var database=DatabaseFromString(str);database.replacePubs();database.replaceSearches();database.countHits();}}
function load(url){try
{getHTTP(url,alertContents);}
catch(err)
{bibtex.error("There seemed to have been an error loading the bibtex file:<br>"+err);}}